 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################


class DB:

    def __init__(self,Config):

        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from bson.objectid import ObjectId  
       
      
        self.Config                         = Config
        self.getcwd                         = getcwd
        self.join                           = join 
        self.floor                      	= floor 
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump  
        self.datetime                       = datetime
        self.ObjectId                       = ObjectId 
        self.server			                = Config.DB_SERVER or "localhost"
        self.port			                = str(Config.DB_PORT or "27017")
        self.db_name                        = getattr(Config, "DB_NAME", "ELET2415") or "ELET2415"
        raw_user                            = getattr(Config, "DB_USERNAME", None)
        raw_pass                            = getattr(Config, "DB_PASSWORD", None)

        if isinstance(raw_user, str):
            raw_user = raw_user.strip() or None
        if isinstance(raw_pass, str):
            raw_pass = raw_pass.strip() or None

        raw_authsource                      = getattr(Config, "DB_AUTHSOURCE", None)
        if isinstance(raw_authsource, str):
            raw_authsource = raw_authsource.strip() or None

        self.allow_noauth                   = str(getattr(Config, "ALLOW_NOAUTH_DB", "0")).strip() == "1"
        self.auth_source                    = raw_authsource or self.db_name
        self.username                   	= parse.quote_plus(raw_user) if raw_user else None
        self.password                   	= parse.quote_plus(raw_pass) if raw_pass else None
        self.tls                            = str(getattr(Config, "DB_TLS", "0")).strip().lower() in ("1", "true", "yes")
        print(f"[DB] server={self.server} port={self.port} noauth={self.allow_noauth} user_set={bool(self.username)} tls={self.tls} authSource={self.auth_source}")
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError  


    def __del__(self):
            # Delete class instance to free resources
            pass

    def _mongo_uri(self):
        # Use auth only if both creds exist
        if self.username and self.password:
            return "mongodb://%s:%s@%s:%s/%s?authSource=%s" % (
                self.username, self.password, self.server, self.port, self.db_name, self.auth_source
            )

        # Default to open local Mongo (or when explicitly allowed)
        if self.server in ("localhost", "127.0.0.1") or getattr(self, "allow_noauth", False):
            return "mongodb://%s:%s/%s" % (self.server, self.port, self.db_name)

        raise RuntimeError(
            "Mongo credentials missing for non-local server. Set DB_USERNAME/DB_PASSWORD, "
            "or use localhost/127.0.0.1 for open local Mongo."
        )
 


    ####################
    # LAB 2 DATABASE UTIL FUNCTIONS  #
    ####################
    
    def addUpdate(self,data):
        '''ADD A NEW STORAGE LOCATION TO COLLECTION'''
        try:
            uri = self._mongo_uri()
            remotedb 	= self.remoteMongo(uri, tls=self.tls)
            print("DB: URI =", uri)
            try:
                print("DB: databases =", remotedb.list_database_names())
            except Exception as e:
                print("DB: list_database_names failed ->", repr(e))

            result      = remotedb.ELET2415.climo.insert_one(data)
            print("DB: insert OK ->", result.inserted_id)
        except Exception as e:
            print("DB: insert FAILED ->", repr(e))
            return False
        else:                  
            return True
        
       

    def getAllInRange(self,start, end):
        '''RETURNS A LIST OF OBJECTS. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            remotedb 	= self.remoteMongo(self._mongo_uri(), tls=self.tls)
            result      = list(remotedb.ELET2415.climo.find({"timestamp": {"$gte": start, "$lte": end}}, {"_id": 0}))
        except Exception as e:
            msg = str(e)
            print("getAllInRange error ",msg)            
        else:                  
            return result
        

    def humidityMMAR(self,start, end):
        '''RETURNS MIN, MAX, AVG AND RANGE FOR HUMIDITY. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start, "$lte": end}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "min": {"$min": "$humidity"},
                    "max": {"$max": "$humidity"},
                    "avg": {"$avg": "$humidity"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "min": 1,
                    "max": 1,
                    "avg": 1,
                    "range": {"$subtract": ["$max", "$min"]}
                }
            }
        ]
        try:
            remotedb 	= self.remoteMongo(self._mongo_uri(), tls=self.tls)
            result      = list(remotedb.ELET2415.climo.aggregate(pipeline))
        except Exception as e:
            msg = str(e)
            print("humidityMMAS error ",msg)            
        else:                  
            return result[0] if result else None
        
    def temperatureMMAR(self,start, end):
        '''RETURNS MIN, MAX, AVG AND RANGE FOR TEMPERATURE. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start, "$lte": end}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "min": {"$min": "$temperature"},
                    "max": {"$max": "$temperature"},
                    "avg": {"$avg": "$temperature"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "min": 1,
                    "max": 1,
                    "avg": 1,
                    "range": {"$subtract": ["$max", "$min"]}
                }
            }
        ]
        try:
            remotedb 	= self.remoteMongo(self._mongo_uri(), tls=self.tls)
            result      = list(remotedb.ELET2415.climo.aggregate(pipeline))
        except Exception as e:
            msg = str(e)
            print("temperatureMMAS error ",msg)            
        else:                  
            return result[0] if result else None


    def frequencyDistro(self,variable,start, end):
        '''RETURNS THE FREQUENCY DISTROBUTION FOR A SPECIFIED VARIABLE WITHIN THE START AND END DATE RANGE'''
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start, "$lte": end}
                }
            },
            {
                "$group": {
                    "_id": f"${variable}",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    variable: "$_id",
                    "count": 1
                }
            }
        ]
        try:
            remotedb 	= self.remoteMongo(self._mongo_uri(), tls=self.tls)
            result      = list(remotedb.ELET2415.climo.aggregate(pipeline))
        except Exception as e:
            msg = str(e)
            print("frequencyDistro error ",msg)            
        else:                  
            return result
        
 



def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    one = DB(Config)
 
 
    start = time() 
    end = time()
    print(f"completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()


    
