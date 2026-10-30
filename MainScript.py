import sys
from pathlib import Path
from files.DataFile import DataFile
from files.Scanner import Scanner
from utils.logging import Logger
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:

    Logger.Write(Logger.COMMENT, 'Staring RRC Data Updates', None)
    
    # Get all files (filtered set) from all folders set in the config file.
    Scanner.get_all_data_files()

    # Number of files read
    count = 0

    if Scanner.data_files is None:
        Logger.Write(Logger.COMMENT, 'No Files to process today!!', None)
    else:
        count = len(Scanner.data_files)
        Logger.Write(Logger.STATS, str(count) + ' Files to be processed today!!', None)
        count = 0
        for fileInfo in Scanner.data_files:
            # Once debug complete, remove this line
            if "DRILLING" in fileInfo["File"].upper():
                Logger.Write(Logger.DEBUG, "processing {} file {}".format(fileInfo["Type"], fileInfo["File"]), None)
                df = DataFile(fileInfo)
                df.processFile()
                Logger.Write(Logger.STATS, "processed {} file {}".format(fileInfo["Type"], fileInfo["File"]), None)
            count += 1

    Logger.Write(Logger.STATS, "processed {} files".format(count), None)
    sys.exit()

except Exception as ex:
    Logger.Write(Logger.ERROR, 'Error processing files', ex)
    sys.exit()
