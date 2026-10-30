import layout
from parser.RRCTapeRecordCollection import RRCTapeRecordReader
from parser.RRCCsvRecordCollection import RRCCsvRecordReader
from utils.logging import Logger

class ReaderFactory():

    @staticmethod
    def GetReader(layoutCollection):
        try:
            layoutConfigName = layoutCollection.GetType()
            if layoutConfigName != None:
                if ("FULL_WELLBORE" in layoutConfigName.upper()):
                    return RRCTapeRecordReader(layoutCollection)
                elif ("UIC" in layoutConfigName.upper()):
                    return RRCTapeRecordReader(layoutCollection)
                elif ("DRILLING" in layoutConfigName.upper()):
                    return RRCTapeRecordReader(layoutCollection)
                elif ("QUERY" in layoutConfigName.upper()):
                    return RRCCsvRecordReader(layoutCollection)
            else:
                Logger.Write(Logger.WARN, "Error determining record layout for the file", None)
        except Exception as ex:
             Logger.Write(Logger.ERROR, "Error determining the right reader for the file", ex)