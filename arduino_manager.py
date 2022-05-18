import sys
import os

import serial
import time
import timeit
from datetime import datetime
import logging

#import user_settings


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



class Device:

    def __init__(self, port, baud_rate, protected_commands = []):
        self.port = port
        self.baud_rate = baud_rate
        self.protected_commands = protected_commands
        self.intentos = 0

    def connect_device(self):
        self.device = serial.Serial(self.port, self.baud_rate, timeout=5)
        self.device.write(''.encode())

    def disconnect_device(self):
        self.device.close()

    def send_command(self, command, timeout):
        commandFinished = False
        if command in self.protected_commands:
            timeout = 10000000
        start = timeit.default_timer()  # Empieza un timmer para medir cuando demora
        response = []
        command = "{}\n".format(command).encode()
        try:
            self.device.write(command)
            while not commandFinished:
                data = self.device.readline()[:-2]
                if data:
                    decoded = data.decode("utf-8")
                    response.append(decoded)
                    if decoded == 'ok': #Cuando se envia info al grlb
                        return response
                    elif decoded == 'ready':
                        return response
                    if decoded == 'error:2':
                        print('error', command)
                        return sys.exit()
                time.sleep(0.001)
                if timeit.default_timer() - start > timeout:
                    return response
        except:
            logger.info(f"Problema al enviar comando: {command}, antes se enviava nuevamente, esa parte esta comentada")
 #           self.intentos = self.intentos + 1
 #           if self.intentos < 5:
 #               self.disconnect_device()
 #               time.sleep(2)
 #               self.connect_device()
 #               time.sleep(2)
 #               self.send_command(command, timeout)
 #           else:
 #               logger.info(f"No se pudo conectar el arduino, terminando operacion")
 #               sys.exit()



    def cual(self):
        self.connect_device()
        time.sleep(0.5)
        commands = ['$x','q']
        for i in commands:
            try:
                val = self.send_command(command=i, timeout=1)
                for j in range(0,20):
                    if val[j] == 'nano':
                        self.device.close()
                        return 'nano'
                    elif val[j] == "Grbl 1.1h ['$' for help]" or val[j] == "ok":
                        self.device.close()
                        return 'grlb'
            except:
                pass
        self.device.close()
    
    def hay_corriente(self):
        try:
            val = self.send_command('e', timeout = 1)
            if val[1] == '1':
                print("Hay corriente")
            elif val[1] == '0':
                print("No hay corriente")
        except:
            pass


if __name__ == '__main__':
    arduino = Device(port='/dev/ttyACM0', baud_rate=115200)
    arduino.connect_device()
    arduino.send_command("", timeout=1)
    while True:
        arduino.hay_corriente()
        time.sleep(2)


