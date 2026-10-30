import os
from parser.RecordFactory import ReaderFactory
from parser.BaseRecordCollection import RecordReader
from layout.LayoutCollection import LayoutCollection
from utils.logging import Logger


class DataFile:
    dataSetName = None
    dataSetType = None
    filePath = None
    layoutCollection = None

    def __init__(self, data_file):
        try:
            self.dataSetType = data_file['Type']
            self.filePath = data_file['File']

            if self.dataSetType != None and self.filePath != None:
                self.layoutCollection = LayoutCollection(self.dataSetType)

            if (self.layoutCollection == None):
                Logger.Write(Logger.ERROR, "Could not determine layout configuration", None)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Exception while initializing layout collection", None)

    # Process file
    def processFile(self):
        try:
            
            successReads = 0
            failedReads = 0
            rootRecCount = 0
            checkRoot = True
            rootRecordType = self.layoutCollection.root_record_key

            # Get all the record layouts for the current file type
            
            recordCollection = ReaderFactory.GetReader(self.layoutCollection)

            # Check if root record need to be checked
            if (rootRecordType == None or rootRecordType == ""):
                checkRoot = False

            # Now read the file, line by line
            with open(self.filePath, newline=None) as file:
                for line_terminated in file:

                    dataLine = line_terminated.rstrip('\n').strip()

                    if len(dataLine) > 0:
                        
                        # read lines and return status
                        success = recordCollection.process(dataLine)

                        # dataframe is appended to a file specific for a layout type
                        if success == False:
                            failedReads += 1
                            Logger.Write(Logger.WARN,
                                         "No processed datasets available for output for line " + dataLine + ". Skipping ",
                                         None)
                        else:
                            successReads += 1
                            recType = dataLine[0:2]

                            if checkRoot: 
                                if recType == rootRecordType:
                                    rootRecCount += 1
                                    #Save after every nth root record as specified in the config file
                                    if rootRecCount > self.layoutCollection.bufferSize -1:
                                        recordCollection.flushData(self.dataSetType)
                                        rootRecCount = 0
                            else:
                                # All records are treated like root record. Need to address when another reader is added
                                rootRecCount += 1
                                if rootRecCount > self.layoutCollection.bufferSize - 1:
                                    recordCollection.flushData(self.dataSetType)
                                    rootRecCount = 0
                
                # At the end flush remaining records gathered
                recordCollection.flushData(self.dataSetType)
                rootRecCount = 0

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Exception while processing datafile " + self.filePath, ex)
