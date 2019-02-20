import subprocess
import os 
import random

def generate_random_socket():
    # return a random port to host the web app 
    # currently only supports 2000 apps
    return random.randint(8000,10000)

def startup(config):
    #Runs the subprocess which spins up uwsgi server
    completed = subprocess.run(['uwsgi', '--ini', config])

def create_config_file(location, name_of_app, num_threads):
    # creates a new config file for app
    f = open('configs/' + name_of_app + '.ini', 'w+')
    f.write('[uwsgi] \n')
    f.write('chdir=' + location + '\n')
    f.write('module=' + name_of_app + '.wsgi:application \n')
    f.write('home=' + os.getcwd() + '/envs/' +  name_of_app + '\n')
    f.write('processes=' + str(num_threads) + '\n')
    new_port = generate_random_socket()
    f.write('socket=0.0.0.0:' + str(new_port) + '.socket \n' )
    f.write('protocol=http')
    f.close()
    return 'configs/' + name_of_app + '.ini'

def clone_repo(repo_url, app_name):
    # clones git repo of django app
    clone = subprocess.run(['git', 'clone', repo_url, 'apps/' + app_name])
    return './apps/' + app_name


def make_virtual_env(app_name):
    # creates new virtual environment
    create_env = subprocess.run(['virtualenv', 'envs/' + app_name])

def restore_dependencies(app_name):
    # installs dependencies in virtual environment using requirements.txt
    restore = subprocess.run(['pip3', 'install', '-r', 'apps/'+ app_name + '/requirements.txt'])

def workflow(repo_url, app_name, num_threads):
    # complete workflow
    make_virtual_env(app_name)
    config = create_config_file('apps/dailypress', app_name, num_threads)
    startup(config)