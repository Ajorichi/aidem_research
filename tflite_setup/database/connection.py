from pymongo import MongoClient

def get_database(usr = str, pwd = str, clnt = str):
 
    # artriguer100304:100304Jcd&Art
    #client -> mosquito_systems
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{usr}:{pwd}@cluster0.easnlpy.mongodb.net/?retryWrites=true&w=majority"
        
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
        
    return client[clnt]