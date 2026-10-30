from abc import abstractmethod
from layout.LayoutCollection import LayoutCollection
from utils.Sequence import Sequencer
from utils.logging import Logger
from utils.Configuration import Configuration
from datetime import datetime
import pandas as pd
import os
from db.DBUtil import TXRRCDbAccess

from parser.DataRecord import Record

class RecordReader():
    layoutCollection = None
    dataRecords = dict() # to keep all records

    # Called at the beginning of processing just once
    def __init__(self, layoutCollection):
        self.layoutCollection = layoutCollection
        self.__reset__()

    def __reset__(self):
        Sequencer.ResetRecIds()


    @abstractmethod
    def process(self, dataLine):pass

    def addRecord(self, recType, record):
        try:
            df = pd.DataFrame()

            if not record.empty :

                if recType in self.dataRecords:
                    df = self.dataRecords[recType]
                    df = pd.concat([df,record],axis=0)
                    self.dataRecords[recType] = df
                else:
                    df = record
                    self.dataRecords[recType] = df
        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error while adding record to collection "+recType, ex)

               
    #
    #Writing to files
    #
    def flushData(self,dataSetType):
        fileName = None
        try:
            if bool(self.dataRecords):

                folder = Configuration.RootFolder() + "\\_Processed_\\" + dataSetType

                #folder = "C:\\Temp\\RRC_DATA\\_Processed_\\" + dataSetType

                if not os.path.exists(folder):
                    os.makedirs(folder)

                for name,frame in self.dataRecords.items():

                    fileName = folder + "\\" + name + ".txt"

                    if not os.path.exists(fileName):
                        frame.to_csv(fileName, mode='a', index=False, sep="\t",header=True, encoding='utf-8')
                    else:
                        frame.to_csv(fileName, mode='a', index=False, sep="\t", header=False, encoding='utf-8')

                Sequencer.ResetRecIds()
                self.dataRecords = dict()

            else:
                Logger.Write(Logger.WARN, "Recordset was empty. Nothing to append to output file  " + fileName, None)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Exception appending to output file  " + fileName, ex)

    #
    #If deciding to flush in to db directly
    #
    def flushDataToDB(self,dataSetType):
        fileName = None
        try:
            if bool(self.dataRecords):

                #If decising to flush in to db directly
                dba = TXRRCDbAccess()

                schema = self.layoutCollection.schema

                for name,frame in self.dataRecords.items():

                    # Flush in to database directly
                    dba.updateDB(frame,name,schema)

                Sequencer.ResetRecIds()
                self.dataRecords = dict()

            else:
                Logger.Write(Logger.WARN, "Recordset was empty. Nothing to add to DB", None)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Exception inserting rows to DB", ex)