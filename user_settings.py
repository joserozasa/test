import local_settings


#DEBUG Setting
DEBUG_MODE = local_settings.debug

#Plate Number
n_plate = local_settings.n_plate

#MANUAL Settings
MODE_ALT = ["timer","continuous"]
MODE = MODE_ALT[local_settings.mode]

#Current Sensor Available
CURRENT_SENSOR = local_settings.CURRENT_SENSOR

#SAMS -> para PATHs
sams_id = local_settings.sams_id

#Camara
cam = local_settings.cam

##Timer
SAMPLING_HOURS = local_settings.sampling_hours #Tiene que haber 3 horas de diferencia entre cada una. Horas del dia donde se requiere muestra [horas, minuto]. 
    

if DEBUG_MODE:
    ##Continuos
    CONTINUOUS_TARGET_SAMPLE = 2

    X_STEPS = 4 #Numero de columnas que recorrera. El total de la grilla son 50 (49 contanto 0)
    Y_STEPS = 4  #Numero de filas que recorrera. El total de la grilla son 20 (19 contando 0)

    LOAD_TO_AWS = True

    ##IMAGE Settings
    DECANTING_SET_TIME = 1 *1  #Compara en segundos. 60 segundos * 60 minutos -> decantando 1 hora
    MINIMUM_IMAGEN_ON_FOLDER = 800
    PAUSA_ENTRE_FOTOS = 0.1 #Delay entre fotos, necesario para la captura de la foto

    LOAD_GRBL_SETTING = False  # solo necesario cargar cada vez que halla una actualizacion en los settings
else:
    ##Continuos
    CONTINUOUS_TARGET_SAMPLE = 20
    
    X_STEPS = 49 #Numero de columnas que recorrera. El total de la grilla son 50 (49 contanto 0)
    Y_STEPS = 19 #Numero de filas que recorrera. El total de la grilla son 20 (19 contando 0)

    LOAD_TO_AWS = True

    ##IMAGE Settings
    DECANTING_SET_TIME =  30*60  #Compara en segundos. 60 segundos * 60 minutos -> decantando 1 hora
    MINIMUM_IMAGEN_ON_FOLDER = 800
    PAUSA_ENTRE_FOTOS = 0.1 #Delay entre fotos, necesario para la captura de la foto

    LOAD_GRBL_SETTING = False  # solo necesario cargar cada vez que halla una actualizacion en los settings

    
ULTIMA_PLACA_REVISADA = 2 #Para que al iniciar siempre comience con la 1.

##Settings comunes entre debug y normal

X_INICIAL_1 = local_settings.x1_start
Y_INICIAL_1 = local_settings.y1_start

X_INICIAL_2 = local_settings.x2_start #Posicion X inicial de la placa 2, solo en 2 placas
Y_INICIAL_2 = local_settings.y2_start #Posicion Y inicial de la placa 2, solo en 2 placas


#CONFIGURACION INICIAL:
PROTECTED_ARDUINO_CAL_COMMANDS = ['a1', 'b1', 'a2', 'b2', 'c1', 'c2']



import os
import logging
import arduino_manager
import subprocess
import platform

logger = logging.getLogger('User_settings')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# puede ser ubuntu, mac o mendel




def cual_maquina():
    if platform.uname().system == "Linux":
        MAQUINA = "jetson"
    elif platform.uname().system == "Windows" :
        MAQUINA = "Windows"
    return MAQUINA


def storage_path(maquina):
    local_storage = 'imgs'
    if MAQUINA == 'jetson':
        local_storage = f'/media/{sams_id}/UNTITLED'
    elif MAQUINA == 'Windows':
        local_storage = 'imgs'
    elif MAQUINA == 'prueba':
        local_storage = '/mnt/SD'
    return local_storage

def arduinos_path(maquina):
    nano = 'no'
    grlb = 'no'
    nano_state = False
    grlb_state = False
    if maquina == "Windows":
        nano = 'COM4'
        grlb = 'COM5'
        return nano, grlb
    elif maquina == 'jetson':
        prefix=['/dev/ttyUSB','/dev/ttyACM']
    for i in range(0,6):
        try:
            arduino_test_grlb = arduino_manager.Device(port=f'{prefix[1]}{i}', baud_rate=115200)
            arduino_test_nano = arduino_manager.Device(port=f'{prefix[1]}{i}', baud_rate=115200)
            if arduino_test_nano.cual() == 'nano':
                nano = f'{prefix[1]}{i}'
                nano_state = True
            if arduino_test_grlb.cual() == 'grlb':
                grlb = f'{prefix[1]}{i}'
                grlb_state = True
            if grlb_state and nano_state:
                break
        except:
            pass
    return nano, grlb



# #Paths
logger.debug("Detectando variables locales...")
MAQUINA = cual_maquina()
CALIBRATION_DEVICE_PORT, GRLB_DEVICE_PORT = arduinos_path(MAQUINA)
LOCAL_STORAGE = storage_path(MAQUINA)
# ~ LOCAL_STORAGE = '/home/sams3/Desktop/temp'


PORTS_READY = True
#Si no encuentra uno, detiene el programa
intento = 0
while CALIBRATION_DEVICE_PORT == "no" or GRLB_DEVICE_PORT =="no":
    CALIBRATION_DEVICE_PORT, GRLB_DEVICE_PORT = arduinos_path(MAQUINA)
    if CALIBRATION_DEVICE_PORT != "no" and GRLB_DEVICE_PORT != "no":
        logger.info(f'Luego de {intento} intentos se conectaron los puertos de ambos arduinos, se correra el programa')
        break
    intento = intento + 1
    if intento >= 3:
        PORTS_READY = False
        logger.info(f'Luego de {intento} intentos no se pudo conectar los puertos correctamente')
        break
        

logger.info(f"Maquina: {MAQUINA}")
logger.info(f"Calibration device port: {CALIBRATION_DEVICE_PORT}")
logger.info(f"Grlb device port: {GRLB_DEVICE_PORT}")
logger.info(f"Local storage path: {LOCAL_STORAGE}")





if __name__ == '__main__':
    print(CALIBRATION_DEVICE_PORT, GRLB_DEVICE_PORT)

