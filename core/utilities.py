import subprocess
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
    f.write('home=' + location + '/venv \n')
    f.write('processes=' + str(num_threads) + '\n')
    new_port = generate_random_socket()
    f.write('socket=0.0.0.0:' + str(new_port) + '.socket \n' )
    f.write('protocol=http')
    f.close()
    return 'configs/' + name_of_app + '.ini'

