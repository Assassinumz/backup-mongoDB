from pymongo import MongoClient
from bson.json_util import dumps
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os, json, time
import datetime as dt


# change the current working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


with open('config.json', 'r') as f:
        data = json.load(f)


if data['GDrive']:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

        folderid = None
        for folder in file_list:
                if folder['title'] == 'backups':
                        folderid = folder['id']

        if folderid is None:

                folder_metadata = {'title' : 'backups', 'mimeType' : 'application/vnd.google-apps.folder'}
                folder = drive.CreateFile(folder_metadata)
                folder.Upload()
                folderid = folder['id']


# if backups dir does not exist, create one
if not os.path.isdir('backups'):
        os.mkdir('backups')


client = MongoClient(data['host'])
db = client[data['database']]


def main():

    collections = db.collection_names(include_system_collections=False) # get all the collections in the database
    time_stamp = dt.datetime.now().strftime("[%a, %d-%m-%Y %H.%M]") # Create a time stamp


    for collection in collections:
        filename = f"{collection}-{time_stamp}.json"

        counter = 0
        for document in db[collection].find():
            with open(f'backups/{filename}', 'a') as f:
                    f.write(dumps(document) + "\n")
            counter += 1

        if data['GDrive']:

            file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}], "title" : f"{filename}"})
            file.SetContentFile(f'backups/{filename}')
            file.Upload()

        
        print(f'''
{time_stamp}
Backed up {counter} Documents from {collection} in backups/{filename}
''')


while True:
        main()
        print(f"Sleeping for {data['sleep']} seconds")
        time.sleep(data['sleep'])