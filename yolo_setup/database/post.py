# Get the database using the method we defined in pymongo_test_insert file
from database.connection import get_database

# dbname -> research
def post_pipe(data= dict, srv = dict) -> None:
    dbname = get_database(usr=srv['user'], pwd=srv['password'], database=srv['database'])
    collection_name = dbname[srv['clnt']]

    collection_name.insert_many([data])