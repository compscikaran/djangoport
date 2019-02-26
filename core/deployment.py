import subprocess
import os 
import random

def generate_random_socket():
    # return a random port to host the web app 
    # currently only supports max of 2000 sockets
    return random.randint(8000,10000)


class Deployment:
    def __init__(self, app_name, repo_url, num_threads):
        self.app_name = app_name
        self.repo_url = repo_url
        self.num_threads = num_threads
        self.port = generate_random_socket()

    def clone_repo(self):
        # clones git repo of django app
        clone = subprocess.run(['git', 'clone', self.repo_url, 'apps/' + self.app_name])
        return './apps/' + self.app_name


    def make_virtual_env(self):
        # creates new virtual environment
        create_env = subprocess.run(['virtualenv', 'envs/' + self.app_name])


    def restore_dependencies(self):
        # installs dependencies in virtual environment using requirements.txt
        restore = subprocess.run(['envs/' + self.app_name + '/bin/python', '-m', 'pip', 
                                'install', '-r', 'apps/' + self.app_name + '/requirements.txt'])


    def create_config(self, location):
    # creates a new config file for app
        f = open('configs/' + self.app_name + '.ini', 'w+')
        f.write('[uwsgi] \n')
        f.write('chdir=' + location + '\n')
        f.write('module=' + self.app_name + '.wsgi:application \n')
        f.write('home=' + os.getcwd() + '/envs/' +  self.app_name + '\n')
        f.write('processes=' + str(self.num_threads) + '\n')
        f.write('socket=0.0.0.0:' + str(self.port) + '.socket \n' )
        f.write('protocol=http')
        f.close()
        return 'configs/' + self.app_name + '.ini'


    def run(self, config):
        #Runs the subprocess which spins up uwsgi server
        completed = subprocess.run(['uwsgi', '--ini', config])
        return 'localhost:' + self.port


    def initialize(self):
        # complete workflow
        repo = self.clone_repo()
        self.make_virtual_env()
        self.restore_dependencies()
        config = self.create_config(repo)
        return config