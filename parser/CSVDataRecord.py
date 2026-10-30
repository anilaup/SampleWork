from layout.LayoutCollection import LayoutCollection
from utils.Sequence import Sequencer
from utils.logging import Logger
from datetime import datetime
from parser.DataRecord import Record
import pandas as pd
import re

class CSVRecord(Record):

    def getDataFrame(self):
        try:

            # if record length is less than the data line read in , then trim it.
            recordLength = self.currentLayout.record_length
            dataLine = self.dataLine

            # In the case of CSV files, default record length is 0 - ignore this param.
            # BUT if defined, respect the value
            if (recordLength > 0 and len(self.dataLine) > recordLength):
                dataLine = self.dataLine[0:recordLength]

            indices = self.currentLayout.offsets
            # indices are "1" based and not "0" based so converting
            if (indices[0] > 0):
                indices[:] = [x - 1 for x in indices]

            # Cleanup dataline 
            dataLine = dataLine.replace('\t','').replace("\"","")

            # Extract values in to a list
            attribVals1 = dataLine.split(",")

            # Convert to appropriate types
            attribVals = self.__convertTypes__(attribVals1)

            if (len(attribVals) ==0 or len(attribVals) != len(indices)):
                Logger.Write(Logger.ERROR, "Values and offsets do not match, skipping line " + dataLine, None)

            # Convert to a dataframe
            if (self.df.empty):
                self.df = pd.DataFrame(attribVals).T
                # Set column headers
                self.df.columns = self.currentLayout.attributes
            else:
                self.df.loc[len(self.df)] = attribVals

            # Add primary key/id
            seqNo = Sequencer.NextVal()
            l = []
            l.append(seqNo)

            self.df.insert(0, self.currentLayout.primary_key, seqNo, False)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value to appropriate type : " + dataLine + "  " + self.currentLayout.ame, ex)
            self.df = pd.DataFrame()

        return self.df



