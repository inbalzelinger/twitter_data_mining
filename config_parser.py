#from backports import configparser
import configparser
##TODO change this there is no reason to read all the config in the condtructor.
##TODO maybe change this to yml file>?
class Config_parser:
    def __init__(self, configuration_file_path = 'configuration.conf'):
        self.file_path = configuration_file_path
        self.twitter_for_developers_config = self.__read_config('TWITTER')

    def __read_config(self, section):
        config_parser = configparser.RawConfigParser()
        ##TODO better to use built in relative path!!!
        config_parser.read(self.file_path)
        return config_parser[section]







