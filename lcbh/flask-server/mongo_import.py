from pymongo import MongoClient
import pandas as pd

def get_df_from_mongodb(c_string):
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   #CONNECTION_STRING = "mongodb+srv://jackdaenzer2024:eZUnYSdbNJuzvH9U@csx-lcbh.us3nupa.mongodb.net/csx-lcbh"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(c_string)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   my_db = client['csxdb']
   my_col = my_db["CS_X LCBH Database"]
   df = pd.DataFrame(list(my_col.find()))
   return df

#my_col = get_database()["CS_X LCBH Database"]


#df = pd.DataFrame(list(my_col.find()))
#print(get_df_from_mongodb("mongodb+srv://jackdaenzer2024:eZUnYSdbNJuzvH9U@csx-lcbh.us3nupa.mongodb.net/csx-lcbh")["Inquiry"])