from abc import abstractmethod
from layout.LayoutCollection import LayoutCollection
from utils.Sequence import Sequencer
from utils.logging import Logger
from datetime import datetime 
from dateutil.parser import parse
import pandas as pd
import re

class Record():

    dataLine = None
    recordType = None
    currentLayout = None
    df = pd.DataFrame()

    def __init__(self,dataLine, currentLayout):
        if dataLine == None or currentLayout == None :
            return self.df

        self.currentLayout = currentLayout

        if self.currentLayout == None:
            return self.df

        self.dataLine = dataLine

        # set all columns to string

        self.df.astype(str)

    @abstractmethod
    def getDataFrame(self):pass

    def __convertTypes__(self, attribVals):
        returnVals = []
        try:

            if self.currentLayout == None or attribVals == None or len(attribVals) < 1:
                return attribVals

            idx = 0

            for attrib in attribVals:
                val = "" if attrib is None else attrib.strip().replace('\x00', '')
                typ = self.currentLayout.attribute_type[idx].value
                name = self.currentLayout.attributes[idx]

                if "FILLER" in name.upper():
                    val = ""

                if (val == "" or val == None):
                    returnVals.append("")
                elif (typ == "Int"):
                    returnVals.append(self.__convertToInt__(val))
                elif (typ == "float"):
                    returnVals.append(self.__convertToFloat__(val))
                elif (typ == "Str"):
                    if len(val) < 2 and val.strip() == "0":
                        val = None
                    elif val.strip("0") == "" or val.strip("0") == "None" :
                        val = None
                    returnVals.append(val)
                elif (typ == "date1"):
                    returnVals.append(self.__convertToDate__(val))
                elif (typ == "date2"):
                    returnVals.append(self.__convertToDate__(val))
                elif "loc" in typ:
                    returnVals.append(self.__convertToLatLong__(val, typ))
                else:
                    returnVals.append(val)

                idx += 1

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value to appropriate type : ", ex)
            returnVals = []

        return returnVals


    def __convertToInt__(self, intString):
        returnVal = None
        try:

            # Cleanup string
            coordString = re.sub('[^0-9]', '', intString)

            if (intString.upper() == "NA"):
                returnVal = None
            else:
                returnVal = int(intString)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value " + intString + " to Int type: "+self.dataLine ,ex)
            returnVal = None

        return returnVal


    def __convertToFloat__(self, floatString):
        returnVal = None
        try:
            # Special case 
            if (floatString.upper() == 'SURF' or floatString.upper() == 'SURFACE'):
                floatString = "0"

            # Cleanup string
            floatString = re.sub('[^0-9.]', '', floatString)

            returnVal = float(floatString)

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value " + floatString + " to Float type: "+self.dataLine ,ex)

        return returnVal


    def __convertToDate__(self, dateString):
        returnDate = None
        year = None
        month = "01"
        day = "01"
        try:

            dateString = dateString.strip()

            if (dateString.strip('0') == None or dateString.strip('0') == '' or len(dateString.strip('0')) < 4 ):
                return None

            # This should take care of all normal cases
            returnDate = self.__parseDateString__(dateString)

            # Special handling where dates are wrong 
            if returnDate == None:
                returnString = self.__getDate__(dateString)
                if returnString != None:
                    returnDate = datetime.strptime(returnString, '%Y%m%d').date()

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value "+ dateString +" to Date type :  "+self.dataLine , ex)

        return returnDate

    def __isDate__(self,dateString, fuzzy=False):
        """
        Return whether the dateString can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try: 
            parse(dateString, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def __parseDateString__(self,dateString):
        try:
            fmts = ('%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y','%Y%m','%Y%m%d','%d-%b-%y','%d-%b-%y %I.%M.%S','%d-%b-%y %I.%M.%S.%f','%d-%b-%y %I.%M.%S.%f %p')
            retDate = None
            for fmt in fmts:
                try:
                    retDate = datetime.strptime(dateString, fmt)
                    break
                except ValueError as err:
                    pass
        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting value "+ dateString +" to Date type :  "+self.dataLine , ex)
        return retDate

    def __getYear__(self,dateString):
        try:
            #First 4 characters are taken as year
            if (dateString == None or len(dateString) < 4 or int(dateString.strip(' ').strip('0'))<1800):
                Logger.Write(Logger.INFO,"Date string is not valid and/or year determination not possible",None)
                return None
            else:
                yrStr = dateString[0:4]
                return yrStr
        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error finding year value in "+ dateString + " :  "+self.dataLine , ex)
        return None

    def __getMonth__(self,dateString):
        try:
            #1-4 as Year, 4-6 characters are taken as month
            if (dateString == None or len(dateString) < 6 or int(dateString.strip(' ').strip('0'))<1800):
                Logger.Write(Logger.INFO,"Date string in not valid and/or month determination not possible",None)
                return None
            else:
                year = self.__getYear__(dateString)

                month = dateString[4:6]

                if (int(month) > 12):
                    month = year+"12"
                elif (int(month) ==0):
                    month = year+"01"
                else:
                    month = year + month
                return month

        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error finding month value in "+ dateString + " :  "+self.dataLine , ex)

        return None

    def __getDate__(self,dateString):
        try:

            month = self.__getMonth__(dateString)
            if month == None:
                day = None
            else:
                mth = int(month[4:])
                if len(month) == 6:
                    day = "01"

                    if len(dateString) < 7:
                        day = "01"
                    else:
                        day = dateString[6:8]

                    if (int(day)<1):
                        day = month + "01"
                    else:
                        # Handle the 30 day months
                        if (mth in [4, 6, 9, 11]):
                            if (int(day) > 30):
                                day = month + "30"
                            else:
                                day = month + day
                        #Handle leap year
                        elif (mth == 2):
                            if (mth % 4 != 0):
                                if (int(day) > 28):
                                    day = month + "28"
                                else:
                                    day = month + day
                            else:
                                if (int(day) > 29):
                                    day = month + "29"
                                else:
                                    day = month + day
                        #Now all other months
                        else:
                            if (int(day) > 31):
                                day = month + "31"
                            else:
                                day = month + day
                else:
                    day = None

            return day
        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error finding date value in "+ dateString + " :  "+self.dataLine , ex)
        return None


    def __convertToLatLong__(self, coordString, type):
        returnString = None
        try:
            # Cleanup string
            coordString = re.sub('[^0-9]', '', coordString)

            if ((len(coordString) < 2) or (int(coordString[0:9]) < 10)):
                returnString = ""
            else:
                if (type == "loc1"):
                    returnString = float(coordString[0:3] + "." + coordString[3:9])
                elif (type == "loc2"):
                    returnString = float("-" + coordString[0:3] + "." + coordString[3:9])
                elif (type == "loc3"):
                    returnString = float(coordString[0:-2] + "." + coordString[-2:])
                elif (type == "loc4"):
                    returnString = float(coordString[0:-2] + "." + coordString[-2:])
        except Exception as ex:
            Logger.Write(Logger.ERROR, "Error converting date value to appropriate type : "+self.dataLine , ex)
        return returnString



