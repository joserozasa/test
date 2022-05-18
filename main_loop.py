
import user_settings
import main_functions
import globalvars
from gcode import GCode
import arduino_manager
import logging
import AWS_loader
import local_settings
from file_manager import Sd_card
import os
import time

logger = logging.getLogger('main')
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


#Loop permanente que espera hora u otro gatillante para correr main_app
def loop():
    running = True
    mode = user_settings.MODE
    logger.debug(f'Modo: {mode} con {user_settings.n_plate} placas')
    logger.debug(f'En sams4 sincroniza al iniciar el programa para subier fotos el dia anterior')
    s3_loader = AWS_loader.AWS_loader(access_key_id=local_settings.access_key_id, secret_access_key=local_settings.secret_access_key, origin_dir=user_settings.LOCAL_STORAGE , minimum_treshold=user_settings.MINIMUM_IMAGEN_ON_FOLDER)
    s3_loader.sync_with_bucket()
    if mode == "timer":
        logger.info(f'Esperando a una hora dentro de {user_settings.SAMPLING_HOURS} para comenzar muestreo')
        last_time = []
        while running:
            if main_functions.check_time(user_settings.SAMPLING_HOURS)[0] and last_time != main_functions.check_time(user_settings.SAMPLING_HOURS)[1]:
                last_time = main_functions.check_time(user_settings.SAMPLING_HOURS)[1]
                main_app(globalvars.next_plate, 6)
                #logger.info("Jetson se reiniciara en 240 minutos")
                #os.system("sudo shutdown +240 -r") #se reiniciara despues de x MINUTOS para dar tiempo a aws a subir las fotos
            time.sleep(2)
    elif mode == "continuous":
        target = user_settings.CONTINUOUS_TARGET_SAMPLE
        logger.info(f'Comenzando muestreo continuado por {target} antes de reiniciar')
        main_app(globalvars.next_plate, target)
        time.sleep(5)
        logger.info("Reiniciando sistema en 1 minutos")
        os.system("sudo shutdown +1 -r ") #se reiniciara despues de x MINUTOS para dar tiempo a aws a subir las fotos
        

def main_app_test(next_plate, target):
	for i in range(target):
		print(f'Sample {i}')
		time.sleep(10)	


def main_app(next_plate, target):
    logger.info("----------------------------Process started--------------------------")
    s3_loader = AWS_loader.AWS_loader(access_key_id=local_settings.access_key_id, secret_access_key=local_settings.secret_access_key, origin_dir=user_settings.LOCAL_STORAGE , minimum_treshold=user_settings.MINIMUM_IMAGEN_ON_FOLDER)
    p1 = main_functions.Plate('1', user_settings.X_INICIAL_1, user_settings.Y_INICIAL_1)
    if user_settings.n_plate == 2:
        print("cacho que activo la segunda placa")
        p2 = main_functions.Plate('2', user_settings.X_INICIAL_2, user_settings.Y_INICIAL_2)
    count_sampled = 0
    target = target
    arduino_cal = arduino_manager.Device(port=user_settings.CALIBRATION_DEVICE_PORT, baud_rate=115200, protected_commands=user_settings.PROTECTED_ARDUINO_CAL_COMMANDS)
    sd_card = Sd_card(origin_dir = user_settings.LOCAL_STORAGE, lower_memory_limit = 5000)
    arduino_cal.connect_device()
    while True:
        if count_sampled >= target:
            arduino_cal.disconnect_device()
            s3_loader.delete_empty_folders()
            logger.info("----------------------------Process finished--------------------------")
            break
		
        if p1.process_step == 0:
            sd_card.is_space()
            main_functions.generate_gcode_file(p1.id)
            depth_palte = globalvars.next_depth + p1.id
            p1.folder_name = p1.folder_assignment()
            if user_settings.CURRENT_SENSOR:
                main_functions.check_current(arduino_cal)
            logger.debug("Comenzando proceso de carga de muestra placa 1")
            main_functions.sample_from_depth(depth_palte, arduino_cal, p1.folder_name)
            p1.water_in_plate = globalvars.next_depth
            logger.info(f"Se cargo agua de {globalvars.next_depth} en la placa 1 que se guardara en carpeta {p1.folder_name}")
            globalvars.update_depth()
            p1.start_decanting()

        if user_settings.n_plate == 2:
            if p2.process_step == 0:
                sd_card.is_space()
                main_functions.generate_gcode_file(p2.id)
                depth_palte = globalvars.next_depth + p2.id
                p2.folder_name = p2.folder_assignment()
                if user_settings.CURRENT_SENSOR:
                    main_functions.check_current(arduino_cal)
                logger.debug("Comenzando proceso de carga de muestra placa 2")
                main_functions.sample_from_depth(depth_palte, arduino_cal, p2.folder_name)
                p2.water_in_plate = globalvars.next_depth
                logger.info(f"Se cargo agua de {globalvars.next_depth} en la placa 2 que se guardara en carpeta {p2.folder_name}")
                globalvars.update_depth()
                p2.start_decanting()

        p1.check_decanting_time()
        if user_settings.n_plate == 2:
            p2.check_decanting_time()

        if p1.process_step == 3: #Comienza a fotografiar
            logger.info(f"comienzo captura en placa 1 de profundidad {p1.water_in_plate} que sera guardad en carpeta {p1.folder_name}")
            main_functions.light_state(arduino_cal, on=True)
            main_functions.start_capturing(p1,p1.folder_name)
            main_functions.light_state(arduino_cal, on=False)
            logger.info(f"Escaneada la muestra numero:{count_sampled}")
            p1.process_step = 0
            s3_loader.sync_with_bucket()
            count_sampled = count_sampled + 1

        if user_settings.n_plate == 2:
            if p2.process_step == 3: #Comienza a fotografiar
                logger.info(f"comienzo captura en placa 2 de profundidad {p2.water_in_plate} que sera guardad en carpeta {p2.folder_name}")
                main_functions.light_state(arduino_cal, on=True)
                main_functions.start_capturing(p2,p2.folder_name)
                main_functions.light_state(arduino_cal, on=False)
                logger.info(f"Escaneada la muestra numero:{count_sampled}")
                p2.process_step = 0
                s3_loader.sync_with_bucket()
                count_sampled = count_sampled + 1

        

if __name__ == '__main__':
    
    #main_functions.start_capturing(p1, 'imgs/test_folder')
    if user_settings.PORTS_READY:
        logger.info(f'Puertos listos, comenzando programa')
        try:
            loop()
        except KeyboardInterrupt:
            main_functions.clean_exit()
            logger.error('Interrumpido manualmente')
        except SystemError as e:
            logger.error(str(e))
        except SystemExit as e:
            logger.error(str(e))    
    else:
        logger.info("Puertos no se conectaron correctamente, fin del programa")    
		

    #main_app(globalvars.next_plate)
