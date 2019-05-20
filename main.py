from pymongo import MongoClient
from bson.json_util import dumps
import os, json, time
import datetime as dt


# change the current working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


with open('config.json', 'r') as f:
        data = json.load(f)


# if backups dir does not exist, create one
if not os.path.isdir('backups'):
        os.mkdir('backups')


client = MongoClient(data['host'])
db = client[data['database']]


def main():

    collections = db.collection_names(include_system_collections=False) # get all the collections in the database
    time_stamp = dt.datetime.now().strftime("[%a, %d-%m-%Y %H.%M]") # Create a time stamp

    try:
        for collection in collections:
            filename = f"{collection}-{time_stamp}.json"

            counter = 0
            for document in db[collection].find():
                with open(f'backups/{filename}', 'a') as f:
                        f.write(dumps(document) + "\n")
                counter += 1

            print(f'''
{time_stamp}
Backed up {counter} Documents from {collection} in backups/{filename}
''')


    except Exception as e:
        print("Something went wrong")
        raise e


while True:
        main()
        print(f"Sleeping for {data['sleep']} seconds")
        time.sleep(data['sleep'])