from utils.logging import Logger 
from sqlalchemy.ext.automap import AutomapBase
import pandas as pandas
from sqlalchemy import create_engine
from utils.Configuration import Configuration
# For fast write...using SQLAlchemy
class TXRRCDbAccess:
    engine = None
    def __init__(self):
        try:
            connection = Configuration.OBO_SQL_Connection()

            self.engine = create_engine(connection,fast_executemany=True)
        except Exception as ex:
            print(Logger.ERROR,"Error connecting to database",ex)

    # Update database table, given a connection and schema name. 
    def updateDB(self,data_df,tableName,schemaName):
        try:
            data_df.to_sql(tableName, self.engine, if_exists="append", index=None,chunksize=5000,schema=schemaName)
        except Exception as ex:
            print(Logger.ERROR,"Error writing {} data to the DB schema {}".format(tableName,schemaName),ex)




