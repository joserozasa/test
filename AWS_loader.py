
import boto3
import os
from datetime import time
import local_settings
import shutil
import posixpath
import logging
import subprocess

import user_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class AWS_loader ():

    def __init__(self, access_key_id, secret_access_key, minimum_treshold, origin_dir ,destin_dir = user_settings.sams_id , bucket_name ='retina-image-storage'):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.origin_dir = origin_dir
        self.bucket_name = bucket_name
        self.destin_dir = destin_dir
        self.s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key)
        self.minimum_treshold = minimum_treshold

    def older_no_empty_folder(self):
        older = {'date': 200000000, 'hour': None}
        if self.listdir_nohidden_list(self.origin_dir):
            for dir, a, files in os.walk(self.origin_dir):
                if dir == self.origin_dir and len(a) == 0:
                    return False
                if 'Trash' in dir:
                    continue
                elif len(files) != 0:
                    dir_string = str(dir)
                    try:
                        int(os.path.split(dir)[len(os.path.split(dir))-1][:10].replace('-', ''))
                    except:
                        #print('hay archivos en otro formato)
                        continue
                    folder_date = int(os.path.split(dir)[len(os.path.split(dir))-1][:10].replace('-', ''))
                    #print(folder_date)
                    if folder_date < older['date']:
                        older['date'] = folder_date
            date_string = str(older['date'])
            date = f"{date_string[:4]}-{date_string[4:6]}-{date_string[6:8]}"
            for dir, a, files in os.walk(self.origin_dir):
                if 'Trash' in dir:
                    continue
                elif len(files) != 0:
                    dir_string = str(dir)
                    try:
                        int(os.path.split(dir)[len(os.path.split(dir))-1][:10].replace('-', ''))
                    except:
                        logger.debug('hay archivos en otro formato')
                        continue
                    folder_date = int(os.path.split(dir)[len(os.path.split(dir))-1][:10].replace('-', ''))
                    if folder_date == int(date.replace('-', '')):
                        folder_hour = os.path.split(dir)[1][10:].split('_')
                        hour_time = time(hour=int(folder_hour[0]), minute=int(folder_hour[1]), second=int(folder_hour[2]))
                        if older['hour'] == None:
                            older['hour'] = hour_time
                        elif older['hour'] > hour_time:
                            older['hour'] = hour_time
            hour = f"{str(older['hour'].hour).zfill(2)}_{str(older['hour'].minute).zfill(2)}_{str(older['hour'].second).zfill(2)}"
            name = date + hour
            return name
        else:
            return "empty"

    def listdir_nohidden(self, path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f
    def listdir_nohidden_list(self, path):
        return list(self.listdir_nohidden(path))
        
    def walklevel(self, some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]	

    def upload_folder(self, folder_dir):
        folder_name = ''
        for dir, nada, files in os.walk(self.origin_dir):
            if os.path.split(dir)[len(os.path.split(dir))-1] == folder_dir:
                for file in files:
                    name_store = os.path.join(dir, file)
                    name_up = posixpath.join(self.destin_dir, folder_dir,file)
                    folder_name = dir
                    if not self.debug:
                        self.s3.meta.client.upload_file(name_store, self.bucket_name, name_up)
                    else:
                        logger.debug(f"---DRYRUN---  "
                              f"File {name_store} uploaded to {name_up}")
        logger.info(f'Files from {folder_name} uploaded to AWS S3')

    def sync_with_bucket(self):  #reemplaza a upload_folder. Sincronizar es mejor      
        destin_folder = posixpath.join(self.bucket_name, self.destin_dir)
        if user_settings.LOAD_TO_AWS:
            logger.debug(f'subira desde {self.origin_dir}al bucket s3://{destin_folder}')
            subprocess.Popen(["/usr/bin/aws", "s3", "sync", f"{self.origin_dir}",f"s3://{destin_folder}", "--exclude",".*"])
        else:
            subprocess.Popen(["/usr/bin/aws", "s3", "sync", f"{self.origin_dir}",f"s3://{destin_folder}", "--exclude",".*", "--dryrun"])

    def delete_uploaded_folder(self, folder_dir):
        try:
            if not self.debug:
                shutil.rmtree(os.path.join(self.origin_dir, folder_dir))
            logger.info(f'Carpeta {folder_dir} eliminada')
        except:
            logger.info('Error en el borrado de la ultima carpeta subida')

    def delete_empty_folders(self):
        if self.listdir_nohidden_list(self.origin_dir):
            for dir, folders, files in self.walklevel(self.origin_dir):
                if dir != self.origin_dir and folders == []:
                    if files == [] or files == ['profundidad']:
                        logger.info(f"Carpeta {dir} eliminada por quedar vacia o contener solo profundidad")
                        shutil.rmtree(dir, ignore_errors=True)

    def upload_delete_older_folder(self):
        older_folder = self.older_no_empty_folder()
        if older_folder == "empty":
            logger.info('Carpeta se encuentra vacia, o SD puede no estar montada')
            return False
        ready_to_upload = self.check_if_full(minimun_treshold=self.minimum_treshold, folder_to_check=older_folder)
        if ready_to_upload:
            if self.debug:
                logger.debug(f"DRYRUN -- Carpeta {older_folder} upload")
                logger.debug(f"DRYRUN -- Carpeta {older_folder} eliminada")
            else:
                self.sync_with_bucket()
            return True
        else:
            return False

    def check_if_full(self, minimun_treshold, folder_to_check = ''):
        n_files = len([name for name in os.listdir(os.path.join(self.origin_dir, folder_to_check)) if os.path.isfile(os.path.join(os.path.join(self.origin_dir, folder_to_check), name))])
        if n_files > minimun_treshold:
            logger.debug(f'La carpeta {folder_to_check} ya se puede subir porque tiene {n_files} arcivos')
            return True
        else:
            logger.debug(f'La carpeta {folder_to_check} NO se puede subir porque tiene {n_files} arcivos')
            return False

if __name__ == '__main__':
    AWS_loader = AWS_loader(access_key_id=local_settings.access_key_id, origin_dir=user_settings.LOCAL_STORAGE, 
                           secret_access_key=local_settings.secret_access_key, minimum_treshold=user_settings.MINIMUM_IMAGEN_ON_FOLDER)
    AWS_loader.sync_with_bucket()
