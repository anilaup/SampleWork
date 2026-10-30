import shutil
from utils.Configuration import Configuration
from pathlib import Path
import os
import datetime as dt
from utils.logging import Logger


class Scanner:
    data_files = []

    # Method that goes through all folders defined in the config file and determine all data file paths.
    @staticmethod
    def get_all_data_files():
        try:
            Logger.Write(Logger.DEBUG,'Scanning folders finding files for processing',None)
            # Get all well folders ..as a list
            well_folders = Configuration.Folders()
            root_path = Configuration.RootFolder()

            for baseFolder in well_folders.split(';'):   # Split folder names to track
                fldr = root_path+'\\'+baseFolder

                cntr = 0
                # Get just the files that we need to process cvs and txt
                file_set = Scanner.__get_filtered_fileset(fldr)
                if file_set is None:
                    Logger.Write(Logger.WARN, 'No files for processing in ' + fldr, None)
                    continue
                else:
                    for file in file_set :                  
                        data_dict = dict()
                        data_dict['Type'] = baseFolder
                        data_dict['File'] = file

                        Scanner.data_files.append(data_dict)
                        cntr += 1

                Logger.Write(Logger.WARN, 'Found ' + str(cntr)+' files for processing in '+fldr, None)

        except Exception as ex:
            Logger.Write(Logger.ERROR,'Error while determining files for processing',ex)

    # Method to get a filtered set of files based on extension type
    @staticmethod
    def __get_filtered_fileset(fldr):
        filtered_files2 = []
        try:
            # Move this to settings.config.ini later
            fileTypes = 'csv,txt,CSV,TXT'.split(',')
            filtered_files = os.listdir(fldr)
            if filtered_files is None:
                return None
            else:
                # [print(item) for item in filtered_files if (item[-4:].strip('.')) in fileTypes]
                # filtered files with full path
                [filtered_files2.append(os.path.join(fldr, item)) for item in filtered_files if (item[-4:].strip('.')) in fileTypes]
                # Sort based on date so that they get processed in that order
                filtered_files2.sort(key=os.path.getmtime)
        except Exception as ex:
            Logger.Write(Logger.ERROR, 'Error while determining filtered file set for processing', ex)
        return filtered_files2