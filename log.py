import dropbox
import logging

from time import localtime, strftime
import datetime

class Logger():
    def __init__(self, dropbox_key, title):
        self.title = title
        self.dbx = dropbox.Dropbox(dropbox_key)
        
        # Backup logger
        logging.basicConfig(filename="backup-logger.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
        self.second_logger = logging.getLogger()
        

    def getDate(self):
        return strftime('%Y-%m-%d-%H-%M-%S', localtime())

    def upload(self, data):
        file_name = f"{self.title}-{self.getDate()}.log"
        path = 'logs/' + file_name
    
        try:
            self.dbx.files_upload(
                data, path,
                client_modified=datetime.datetime(*localtime()[:6]), # Jag vet inte vad *localtime()[:6] gör men hoppas det fungerar
                mute=False)
        except dropbox.exceptions.ApiError as err:
            with open(path, 'w+') as f:
                f.write(data)
            
            self.second_logger.error("*** Dropbox API error", err)

    def log(self, content: str):
        self.upload(content)

    
Logger("abc", "log").log("test",)