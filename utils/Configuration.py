import logging
import os
from configparser import SafeConfigParser

logging.basicConfig(level=logging.NOTSET, )

class Configuration:

    config = None
    #
    # read configuration
    #
    @staticmethod
    def __init__():
        try:
            Configuration.config = SafeConfigParser(os.environ,comment_prefixes="#")
            Configuration.config.read('.\settings\config.ini')
        except Exception as ex:
            Logger.Write(Logger.ERROR,'Error initializzing configurationh',ex)

    @staticmethod
    def RootFolder():
        return Configuration.__get_config__('Paths','root_dir')

    @staticmethod
    def MoveToFolder():
        return Configuration.__get_config__('Paths','move_to')

    @staticmethod
    def RejectToFolder():
        return Configuration.__get_config__('Paths','reject_to')

    @staticmethod
    def LogFolder():
        return Configuration.__get_config__('Paths','logging')

    @staticmethod
    def Folders():
        return Configuration.__get_config__('Paths','folders')

    @staticmethod
    def Log_level():
        return Configuration.__get_config__('Log','log_level')

    @staticmethod
    def Log_levels():
        return Configuration.__get_config__('Log', 'log_levels')

    @staticmethod
    def OBO_SQL_Connection():
        return Configuration.__get_config__('SQLAlchemy','sql_conn')

    @staticmethod
    def OBO_Well_Sql2():
        return Configuration.__get_config__('Query', 'obo_well_sql')

    @staticmethod
    def __get_config__(section,property):
        if Configuration.config is None:
            Configuration.__init__()
        return Configuration.config[section][property]