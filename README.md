# Backup mongoDB
A simple script to backup your MongoDB database and upload it to google Drive

## Usage
You can upload this in your webserver and let it run
* Install the requirements
```
pip install requirements.txt
```
* Open `config.json`, paster your MongoDB Host, Database Name and the stand by time (seconds) in the three fields.
Example:
```
{
    "host" : "localhost",
    "database" : "my_database",
    "sleep" : 3600,
    "GDrive" : false //change this to true if you wanna use Google Drive
}
```
* To enable Google Drive uploads change `"GDrive"` to `true` in `config.json` and copy your client secret in the main files
* Run the `main.py` file
```
python main.py
```

## Note
* if you want the script to run in background rename `main.py` to `main.pyw` and execute it
* if you want the script to run everytime your machine starts up rename it to `main.pyw` and move it to your startup folder
