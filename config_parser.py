from backports import configparser

##TODO change this there is no reason to read all the config in the condtructor.
class Config_parser:
    def __init__(self):
        self.twitter_for_developers_config = self.__read_config('TWITTER')
        self.elastic_search_config = self.__read_config('ELASTICSEARCH')

    def __read_config(self, section):
        config_parser = configparser.RawConfigParser()
        ##TODO better to use built in relative path!!!
        config_file_path = r'configuration\configuration.conf'
        config_parser.read(config_file_path)
        return config_parser[section]







