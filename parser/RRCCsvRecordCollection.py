from parser.BaseRecordCollection import RecordReader
from parser.DataRecord import Record
from parser.CSVDataRecord import CSVRecord
import pandas as pd

class RRCCsvRecordReader(RecordReader):

    def process(self, dataLine):
        try:
            df = pd.DataFrame()

            # Counter keeping track of primary record
            rootCtr = 0

            # Record type is always 01 for csv reader
            recordId = "01"

            # Get record layout based on rec type
            currentLayout = self.layoutCollection.GetRecordLayout(recordId)

            if currentLayout is None:
                Logger.Write(Logger.WARN, "Skipping data line. Unknown layout in " + dataLine, None)
                return False

            currentRecord = CSVRecord(dataLine, currentLayout)
            
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