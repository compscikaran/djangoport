from core.utilities import create_config_file, startup

if __name__ == '__main__':
    name = create_config_file('/home/karan/Projects/dailypress/', 'dailypress', 4)
    startup(name)