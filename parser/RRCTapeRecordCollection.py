from parser.MFTapeDataRecord import TapeDataRecord
from utils.logging import Logger
import pandas as pd
from parser.BaseRecordCollection import RecordReader
from parser.MFTapeDataRecord import TapeDataRecord

class RRCTapeRecordReader(RecordReader):

    def process(self, dataLine):
        try:
            df = pd.DataFrame()

            # Counter keeping track of primary record
            rootCtr = 0

            # First 2 characters determine record type 
            recordId = dataLine[0:2]

            # Get record layout based on rec type
            currentLayout = self.layoutCollection.GetRecordLayout(recordId)

            if currentLayout is None:
                Logger.Write(Logger.WARN, "Skipping data line. Unknown layout in " + dataLine, None)
                return False

            # When a new set of records is enountered, write out and reset variables
            if recordId == self.layoutCollection.root_record_key:
                self.__reset__()

            currentRecord = TapeDataRecord(dataLine, currentLayout)
            
            if currentRecord is None:
                return False

            df = currentRecord.getDataFrame()

            if df.empty:
                return False
            else:
                self.addRecord(currentLayout.name,df)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error while processing data lines " + dataLine, ex)
            return False

        return True