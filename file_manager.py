



import subprocess
from datetime import time
import logging
import os
import user_settings

logger = logging.getLogger('file_manager')
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

class Sd_card():

    def __init__(self, origin_dir, lower_memory_limit = 5000):
        self.origin_dir = origin_dir
        self.lower_memory_limit = lower_memory_limit

    def check_SD_empty_space(self): #size limit es en MB
        a = subprocess.run(['df', '-h', self.origin_dir,'--block-size=MB','--output=avail'], stdout=subprocess.PIPE )
        size = ''
        for l in str(a.stdout):
            if l.isnumeric():
                size = size + l
        try:
            if int(size)<self.lower_memory_limit:
                return False
            else:
                return True
        except ValueError:
            logger.error(f'Tarjeta se reconoce tarjeta de memoria')

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
                        #logger.debug('hay archivos en otro formato')
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


    def delete_older(self):
        folder_to_delete = self.older_no_empty_folder()
        subprocess.run(['rm','-rf', f'{self.origin_dir}/{folder_to_delete}'], stdout=subprocess.PIPE)
        return folder_to_delete
        #except:
         #   logger.debug('Error en el borrado de la ultima carpeta de la memoria, puede haber problemas de espacio')

    def is_space(self): #verifica que haya espacio disponible,
        if os.path.isdir(self.origin_dir):
            if self.check_SD_empty_space(): #SI hay mas de {} memoria disponible, se puede guardad
                logger.debug(f'Hay mas de {self.lower_memory_limit} MB de memoria en la SD, se puede guardar sin borrar')
            else:
                while not self.check_SD_empty_space():
                    logger.info(f'No hay {self.lower_memory_limit} MB disponibles, se procede a borrar {self.delete_older()}')
        else:
            logger.info(f'La tarjeta de memoria no esta montada, temporalmente cambiado a Desktop')
            os.makedirs("../temp", exist_ok=True)
            user_settings.LOCAL_STORAGE = "../temp"


if __name__ == '__main__':
    sd_card = Sd_card(origin_dir = user_settings.LOCAL_STORAGE, lower_memory_limit = 6000)
    sd_card.is_space()
