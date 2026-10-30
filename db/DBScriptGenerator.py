
import json
from utils.logging import Logger
from layout.LayoutCollection import LayoutCollection

class SqlGenerator:

    allLayouts = None

    @staticmethod
    def createScripts(dataSetType,schemaName):
        try:

            resultDropString = ""
            resultQryString = ""

            if dataSetType != None and schemaName != None:
                lc = LayoutCollection(dataSetType)
                SqlGenerator.allLayouts = lc.layouts

            if (SqlGenerator.allLayouts != None):
                for layout in SqlGenerator.allLayouts:
                    dropString , qryString = SqlGenerator.__generate__(layout,schemaName)
                    resultDropString = dropString + resultDropString
                    resultQryString += qryString
                
                print(resultDropString + resultQryString)

        except Exception as ex:
            Logger.Write(Logger.ERROR,"Error determining layout collection for "+dataSetType,ex)

    def __generate__(layout,schemaName):
        try:
            qryString = ""
            dropString = ""

            cnt = len(layout.attributes)
            table_name = layout.name
            fk = layout.foreign_key
            pk = layout.primary_key
            rk = layout.root_key
            parent = layout.parent
            root = layout.root

            dropString = "Drop table "+schemaName+"."+table_name+"\n\nGO\n\n"

            qryString1 = "Create table "+schemaName+"."+table_name+ "(\n"
            if (rk != None and rk != "None" and rk!=""):
                qryString1 += rk + "\t int FOREIGN KEY REFERENCES "+schemaName+"."+root +"("+rk+"),\n"

            if (fk != None and fk != "None" and fk != ""):
                qryString1 += fk + "\t int FOREIGN KEY REFERENCES "+schemaName+"."+parent +"("+fk+"),\n"

            if (pk != None and pk != "None" and pk != ""):
                qryString1 += pk + "\t int PRIMARY KEY,\n"


            for idx in range(0,cnt):
                attribute = layout.attributes[idx]
                dataType = layout.attribute_type[idx].value
                if (idx == cnt-1):
                    offsetLength = layout.record_length - layout.offsets[idx]
                else:
                    offsetLength = layout.offsets[idx + 1] - layout.offsets[idx]

                #print (attribute + " " + dataType + " " + str(offsetLength))

                qryString1 += "\t"+SqlGenerator.__createString__(attribute,dataType,offsetLength) +"\n"

            qryString = qryString1.strip()[:-1]+")\n\nGO\n\n"
            
            return dropString, qryString

        except Exception as ex:
            Logger.Write(Logger.Error,"Error generatinf script for "+layout.Name,ex)

        return None, None

    def __createString__(attrib,dataType,length):
        try:
            if (dataType == "Str"):
                return attrib + "\tnvarchar("+str(length)+"),"
            elif (dataType == "float"):
                if (length > 32):
                    length = 32
                elif (length < 10):
                    length = 16
                return attrib + "\tnumeric("+str(length)+",2),"
            elif (dataType == "Int"):
                return attrib + "\tint,"
            elif (dataType == "date"):
                return attrib + "\tdate,"
            elif (dataType == "date1"):
                return attrib + "\tdate,"
            elif (dataType == "date2"):
                return attrib + "\tdate,"
            elif (dataType == "loc1"):
                return attrib + "\tnumeric("+str(length+6)+",8),"
            elif (dataType == "loc2"):
                return attrib + "\tnumeric("+str(length+6)+",8),"
            elif (dataType == "loc3"):
                return attrib + "\tnumeric("+str(length+10)+",2),"
            elif (dataType == "loc4"):
                return attrib + "\tnumeric("+str(length+10)+",2),"
            else:
                return attrib + "\tnvarchar("+str(length)+"),"
            
        except Exception as ex:
            Logger.Write(Logger.Error,"Error generatinf script for "+attrib,ex)
