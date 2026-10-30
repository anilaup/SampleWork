from layout.LayoutCollection import LayoutCollection
from utils.Sequence import Sequencer
from utils.logging import Logger
from datetime import datetime 
from dateutil.parser import parse
from parser.DataRecord import Record
import pandas as pd
import re

class TapeDataRecord(Record):

    def getDataFrame(self):
        try:

            # if record length is less than the data line read in , then trim it.
            recordLength = self.currentLayout.record_length
            dataLine = self.dataLine

            if (len(self.dataLine) > recordLength):
                dataLine = self.dataLine[0:recordLength]

            indices = self.currentLayout.offsets
            # indices are "1" based and not "0" based so converting
            if (indices[0] > 0):
                indices[:] = [x - 1 for x in indices]

            # Extract values in to a list
            attribVals1 = [dataLine[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]

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

            # Check if the record has a foreign key reference
            parent = self.currentLayout.parent

            if parent != None and parent != "None":
                fk = Sequencer.GetCurrentRecId(parent)
                self.df.insert(0, self.currentLayout.foreign_key, fk, False)

            # Check if the record needs a root key reference (grand-chald record)
            root = self.currentLayout.root
            if root != None and root != "None":
                rk = Sequencer.GetCurrentRecId(root)
                self.df.insert(0, self.currentLayout.root_key, rk, False)

            # Save primary key
            Sequencer.SetCurrentRecId(self.currentLayout.name, seqNo)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value to appropriate type : " + dataLine + "  " + self.currentLayout.ame, ex)
            self.df = pd.DataFrame()

        return self.df
