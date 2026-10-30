from datetime import datetime
from utils.Configuration import Configuration
import inspect
import os
import logging

class Logger:
    __task_name__ = None
    __date_time__ = None
    log_file_name = None
    INFO = 'INFO '
    WARN = 'WARN '
    ERROR = 'ERROR'
    STATS = 'STATS'
    DEBUG = 'DEBUG'
    COMMENT = 'COMMENT'

    __log_level__ = None
    __log_levels__ = None
    __log_folder__ = None

    @staticmethod
    def __init__():
        try:
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)

            Logger.__date_time__ = datetime.now()
            Logger.__log_level__ = Configuration.Log_level()
            log_file_name = Logger.__date_time__.strftime("%Y%m%d%H%M")+'.log'
            Logger.__log_folder__ = Configuration.LogFolder()
            Logger.log_file_name = Logger.__log_folder__ + log_file_name
            logging.basicConfig(level=Logger.__log_level__,filename=Logger.log_file_name,filemode='w',format='%(asctime)s   %(message)s',datefmt='%m/%d/%Y  %H:%M') # 'w' ensures, each time the process is run, new file is created.

            Logger.__log_levels__ = Configuration.Log_levels().split(',')

        except Exception as ex:
            print('Error initializing logger ')
            print(ex)

    @staticmethod
    def Set_MetalFile(file_name):
        task_name = 'OBO Production Data Update'  #get from meta file later

        if Logger.__task_name__ is None:
            Logger.__init__()

        Logger.__meta_files__.append(file_name)

    @staticmethod
    def Set_DataFile(file_name):
        # the file name has 2 parts; a. data type and b.date of source
        # task name will hold both.
        try:
            if file_name is None:
                raise Exception("Error: Data File is empty")
            task_name =  file_name.lower().replace('.csv','')

            if Logger.__task_name__ is None:
                Logger.__init__()

            Logger.__meta_files__.append(file_name)
        except Exception as ex:
            logging.error("Error: Can not set logger")
            logging.error(str(ex))


    @staticmethod
    def Write(log_status, log_msg,ex):
        try:

            if Logger.log_file_name is None:
                Logger.__init__()

            # Nothing to do if log level is less critical than the set level in the configuration file.
            if (Logger.__log_levels__.index(Logger.__log_level__) < Logger.__log_levels__.index(log_status.strip())):
                return

            ex_msg = None
            if ex is not None:
                ex_msg = getattr(ex, 'message', repr(ex))

            if Logger.__log_level__ == 'DEBUG':
                msg = Logger.__caller_name__() + chr(9) + log_msg
            else:
                msg =  log_msg

            if (log_status == Logger.ERROR):
                logging.error(chr(9) +Logger.ERROR + chr(9) + msg)
                if (ex_msg is not None):
                    logging.error(chr(9) +Logger.ERROR + chr(9) + ex_msg)
            elif (log_status == Logger.INFO):
                logging.info(chr(9) +Logger.INFO + chr(9) + msg)
            elif (log_status == Logger.WARN):
                logging.error(chr(9) +Logger.WARN + chr(9) + msg)
                if (ex_msg is not None):
                    logging.error(chr(9) +Logger.ERROR + chr(9) + ex_msg)
            elif (log_status == Logger.DEBUG):
                logging.debug(chr(9) +Logger.DEBUG + chr(9) + msg)
            else:
                logging.error(chr(9) +log_status + chr(9) + msg)
        except Exception as ex:
            logging.error(str(ex))

    #https://gist.github.com/2151727
    @staticmethod
    def __caller_name__(skip=2):
        """Get a name of a caller in the format module.class.method

           `skip` specifies how many levels of stack to skip while getting caller
           name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

           An empty string is returned if skipped levels exceed stack height
        """
        stack = inspect.stack()
        start = 0 + skip
        if len(stack) < start + 1:
            return ''
        parentframe = stack[start][0]

        name = []
        module = inspect.getmodule(parentframe)
        # `modname` can be None when frame is executed directly in console
        # TODO(techtonik): consider using __main__
        if module:
            #name.append(module.__name__)
            filename = os.path.splitext(os.path.basename(module.__file__))[0]
            name.append(filename+'.'+module.__name__)
        # detect classname
        if 'self' in parentframe.f_locals:
            # I don't know any way to detect call from the object method
            # XXX: there seems to be no way to detect static method call - it will
            #      be just a function call
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':  # top level usually
            name.append(codename)  # function or a method

        ## Avoid circular refs and frame leaks
        #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
        del parentframe, stack

        return ".".join(name)


