import os
import json
from layout import LayoutHelper
from genericpath import isfile
from utils.logging import Logger

class LayoutCollection():
    
    layoutConfig = None     #Configuration file path
    layouts = None          #List containing all record layouts
    fileType = None         #
    configName = None       #Name from configuration file
    configType = None
    schema = None
    root_record_key = None #By default '01', but get it for each file

    def __init__(self,fileType):

        try:

            if fileType == None :
                Logger.Write(Logger.ERROR,'No file type specified.',None)
            else:
            
                if (os.path.isfile("settings\\"+fileType+".json")):

                    self.fileType = fileType

                    Logger.Write(Logger.DEBUG,"settings\\"+fileType+".json was found",None)
                    
                    self.layoutConfig = "settings\\"+fileType+".json"
                    # Load record layouts from file
                    self.__loadLayoutCollection__()

                else:
                    Logger.Write(Logger.ERROR,"settings\\"+fileType+".json not found",None)
                    
        except Exception as ex:
            Logger.Write(Logger.ERROR,"Error setting layout configuration",ex)

    # Load all record layouts from the configuration file
    def __loadLayoutCollection__(self):
        try:

            #Read json/configuration file. 
            f = open(self.layoutConfig)
            result =  LayoutHelper.RecordLayouts_from_dict(json.loads(f.read()))
            f.close()

            Logger.Write(Logger.DEBUG,self.layoutConfig + " was read",None)

            self.configName = result.name
            self.configType = result.type
            self.layouts = result.record_layouts
            self.root_record_key = result.root_record_key
            self.bufferSize = result.buffer_size
            self.schema = result.schema

        except Exception as ex:
            Logger.Write(Logger.ERROR,"Error setting layout configuration",ex)

    # Get record layout for a given record type id
    def GetRecordLayout(self,recordId):
        currentLayout = None;
        try:

            if self.layoutConfig == None:
                Logger.Write(Logger.ERROR,'Layout configuration is not known. Please set it first.',None)
            else:
                for layout in self.layouts:
                    if layout.record_key == recordId:
                        currentLayout = layout
                        break

            if currentLayout == None:
                Logger.Write(Logger.ERROR,"Could not determine record layout details from configuration for "+recordId,None)

        except Exception as ex:
            Logger.Write(Logger.ERROR,'Error finding record layout for specified record type',None)

        return currentLayout;

    # Get name of the layout configuration
    def GetType(self):

        return self.configType