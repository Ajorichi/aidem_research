# Get the database using the method we defined in pymongo_test_insert file
from database.connection import get_database

# dbname -> research
def post_pipe(data= dict, srv = dict, database= str) -> None:
    dbname = get_database(usr=srv['user'], pwd=srv['password'], clnt=srv['client_name'])
    collection_name = dbname[database]

    collection_name.insert_many([data])