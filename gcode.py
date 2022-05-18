import user_settings


class GCode(object):

    def __init__(self,plate ,x_zero, y_zero, x_steps=49, y_steps=19, pause = user_settings.PAUSA_ENTRE_FOTOS, speed=450):
        self.x_steps = x_steps
        self.y_steps = y_steps
        self.pause = pause
        self.speed = speed
        self.plate = plate
        self.file = open(f"grilla{plate}.gcode", "w")
        self.x_zero = x_zero
        self.y_zero = y_zero
        self.x_start = 0
        self.y_start = 0


    def move_to(self, x, y, speed):
        self.file.write(f"G90 G1 X{x} Y{y} F{speed}\n")
        self.file.write(f"G4 P{self.pause}\n")

        #Mejorar, ahora no esta haciendo nada util
    
    def build_calibration(self):
        print("Comenzando protocolo de calibracion")
        self.move_to(0, 0, self.speed)
        self.move_to(self.x_steps, 0, self.speed)
        self.move_to(self.x_steps, self.y_steps, self.speed)
        self.move_to(0, self.y_steps, self.speed)
        self.file.write(f"G90 G1 X0 Y0\n")
        self.file.close()

    def gcode_header(self):
        self.file.write("$H ; Homming\n")
        self.file.write("G21 ; Set units to mm\n")
        self.file.write("G92 X0 Y0 ; Set Zero\n") #Primero setea 0 en el homming point, luego se mueve hacia la primera celda
        self.file.write(f"G90 G1 X{self.x_zero} Y{self.y_zero} F{self.speed}; Move to start point\n")
        self.file.write(f"G4 P5; Pause\n")
        self.file.write("G92 X0 Y0 ; Set Zero\n") #Segundo seteo de 0, porque ahora comienza el movimiento relativo a la primera celda.

    def build_file(self):
        x_end = self.x_start + self.x_steps
        y_end = self.y_start + self.y_steps
        x_temp = self.x_start
        y_temp = self.y_start
        # self.file.write(f"G4 P{self.pause}\n") # initial picture
        while x_temp < x_end:
            if y_temp == self.y_start:
                while y_temp < y_end:
                    self.move_to(x_temp, y_temp, self.speed)
                    y_temp += 1
                self.move_to(x_temp, y_temp, self.speed)
                x_temp += 1
                while y_temp > self.y_start:
                    self.move_to(x_temp, y_temp, self.speed)
                    y_temp -= 1
                self.move_to(x_temp, y_temp, self.speed)
                x_temp += 1
        # ~ self.file.write(f"G90 G1 X0 Y0 F{self.speed}; Move to start point\n") en el caso de Pulelo, mejor que se quede en esa esquina
        self.file.close()



if __name__ == '__main__':
    CALIBRATION = False

    global_valve = 2
    valve = global_valve - 1

    start = [[4, 4.8],[4, 50.8]] #TODO en algun momento el start_2 va a ser funcion del start_1, solo sumandole x mm al eje y

    
    X_INICIAL = start[valve][0]  # Posicion inicial de la grilla en el eje X
    Y_INICIAL = start[valve][1]  # Posicion inicial de la grilla en el eje Y
    X_STEPS = 50  # Numero de columnas que recorrera. El total de la grilla son 50
    Y_STEPS = 20  # Numero de filas que recorrera. El total de la grilla son 20
    PAUSA_ENTRE_FOTOS = 1.2  # Delay entre fotos, necesario para la captura de la foto, se puede acelerar si la camara lo permite.

    print(f"X_INICIAL {X_INICIAL} y Y_INICIAL {Y_INICIAL}")

    gcode = GCode(X_INICIAL,Y_INICIAL,X_STEPS-1,Y_STEPS-1,PAUSA_ENTRE_FOTOS) #Se puede especificar numero de columnas (X) y numero de filas (Y). (49,19) por dafault
    gcode.gcode_header()
    if CALIBRATION:
        gcode.build_calibration()
    else:
        gcode.build_file()


