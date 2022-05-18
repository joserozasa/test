import time
from datetime import datetime
import os

from gcode import GCode
import user_settings
import arduino_manager
import logging
import globalvars
if user_settings.cam == "Motic":
    from image_moticam_aquicition import Camera
elif user_settings.cam == "Flir":
    from image_flir_aquicition import Camera
   
    
logger = logging.getLogger('main_functions')
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


class Plate:

    def __init__(self, id, x_start, y_start):
        self.id = id
        self.x_start = x_start
        self.y_start =  y_start
        self.decanting_set_time = user_settings.DECANTING_SET_TIME
        self.decanting_start = None
        self.process_step = 0 #Pasos del proceso:0 vacante, 1 cargando, 2 decantanto, 3 fotografiando, 4 Lista
        self.folder_name = ""
        self.water_in_plate = ''


    def start_decanting(self):
        self.decanting_start = time.time()
        logger.info(f"La placa {self.id} comenzo el proceso de decantacion que dura {user_settings.DECANTING_SET_TIME /60} minutos")
        self.process_step = 2

    def check_decanting_time(self):
        delta_decanting_time = time.time() - self.decanting_start
        if delta_decanting_time > self.decanting_set_time:
            logger.info(f"Placa {self.id} decantacion completa")
            self.process_step = 3

    def folder_assignment(self):
        timestamp = datetime.now().replace(microsecond=0)
        timestamp = str(timestamp).replace(" ", "")
        timestamp = str(timestamp).replace(":", "_")
        if os.path.isdir(f"{user_settings.LOCAL_STORAGE}/"):
            try:
                os.makedirs(f'{user_settings.LOCAL_STORAGE}/{str(timestamp)}', exist_ok=True)
            except:
                logger.info(f'Error en la crecion de carpeta, {user_settings.LOCAL_STORAGE}/{str(timestamp)}, no se tiene permiso para crear carpeta en drive')
        file_path = f'{user_settings.LOCAL_STORAGE}/{str(timestamp)}'
        return file_path

def check_time(time_list):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    current_sample = [99,99]
    is_time = False
    for sample_time in time_list:
        if hour == sample_time[0] and minute == sample_time[1]:
            is_time = True
            current_sample = sample_time
    return [is_time, current_sample]

def generate_gcode_file(next_plate):
    #construir el archivo de gcode dependiendo que placa toca recorrer
    if next_plate == '1':
        x_zero = user_settings.X_INICIAL_1
        y_zero = user_settings.Y_INICIAL_1
    elif next_plate == '2':
        x_zero = user_settings.X_INICIAL_2
        y_zero = user_settings.Y_INICIAL_2
    else:
        print("Inicio de grilla no definido")

    #print(f"Next plate: {next_plate} --> x,y = {x_zero}, {y_zero}")

    gcode = GCode(next_plate,x_zero , y_zero, x_steps= user_settings.X_STEPS, y_steps=user_settings.Y_STEPS)
    gcode.gcode_header()
    gcode.build_file()

def start_capturing(plate ,folder_name, load_grbl_settings = False):
    arduino = arduino_manager.Device(port=user_settings.GRLB_DEVICE_PORT, baud_rate=115200)
    arduino.connect_device()
    time.sleep(0.2)
    arduino.send_command('$X', timeout=2)  # Desbloquea el ingreso de comandos
    arduino.send_command('$21=0', timeout=2)
    if load_grbl_settings:
        load_grlb_config(arduino)
        time.sleep(1)
    lines = get_gcode(plate)
    counter = 0
    pic_count = 0
    camera = Camera(folder_name)
    camera.init_camera()
    #arduino.send_command('$21=0', timeout=2)
    try:
        for line in lines:
            command = line.strip()
            counter += 1
            arduino.send_command(command, timeout=2)
            if command == f'G4 P{user_settings.PAUSA_ENTRE_FOTOS}':
                time.sleep(0.7)
                pic_count += 1
                camera.grab_image(pic_count)
                logger.debug(f"Imagen {pic_count} guardada en {folder_name}")
            else:
                logger.debug(command)
            time.sleep(0.5)
#        arduino.send_command('$21=1', timeout=2)
        arduino.disconnect_device()
        camera.deinit_camera()
        logger.info(f"Folder :{folder_name} Complete")
    except KeyboardInterrupt:
        camera.deinit_camera()
 #       arduino.send_command('$21=1', timeout=2)
        arduino.disconnect_device()

def light_state(arduino, on):
    arduino.send_command('', timeout=5)
    if on is True:
        arduino.send_command('n', timeout=5) #n prende la luz en el codigo arduino
    elif on is False:
        arduino.send_command('m', timeout=5) #m apaga la luz en el codigo arduino

def load_grlb_config(arduino):
    f = open("grlb.conf", "r")
    content = f.readlines()
    for line in content:
        arduino.send_command(line, timeout=1, is_setup=True)
        print(f"initial setup ---->{line}")
    f.close()

def get_gcode(plate):
    f = open(f"grilla{plate.id}.gcode", "r")
    content = f.readlines()
    f.close()
    return content

def sample_from_depth(depth_plate, arduino_cal, folder_path):
    depth = depth_plate[0]
    plate = depth_plate[1]
    with open(f'{folder_path}/profundidad', 'w+') as f:
        f.write(depth)
    arduino_cal.send_command('', timeout=1)
    arduino_cal.send_command(depth_plate, timeout=2)
    
def check_current(arduino):
    arduino.send_command('', timeout=2)
    val = arduino.send_command(command='e', timeout=1)
    if val[1]=='0':
        # ~ logger.info("Se corto la energia")
        wait_to_die(arduino, val)
    # ~ elif val[1]=='1':
        # ~ logger.debug("Si hay corriente")
    # ~ print(val)
    
def wait_to_die(arduino, val):
	# ~ unmount sd card
    while val[1] == '0':
        logger.info("Sin energia")
        time.sleep(300)
        val = arduino.send_command(command='e', timeout=1)
    # ~ montar SD
    logger.info("Se reconecto la energia")
        
        
    
def clean_exit():
    print(f'Terminando bien el programadewsde funcion clean_exit')



if __name__ == '__main__':
    p1 = Plate('1', user_settings.X_INICIAL_1, user_settings.Y_INICIAL_1)
    p1.folder_name = p1.folder_assignment()
    start_capturing(p1, '/home/sams4/Desktop/test')
    # ~ depth_palte = globalvars.next_depth + p1.id
    # ~ sample_from_depth(depth_palte, 'arduino', p1.folder_name)
    # ~ arduino_cal = arduino_manager.Device(port=user_settings.CALIBRATION_DEVICE_PORT, baud_rate=115200, protected_commands=user_settings.PROTECTED_ARDUINO_CAL_COMMANDS)
    # ~ arduino_cal.connect_device()
    # ~ for i in range(10):
        # ~ print(f"vuelta n {i}")
        # ~ check_current(arduino_cal)
