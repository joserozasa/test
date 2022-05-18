import time
import os
import cv2
import signal
import subprocess
# ~ import user_settings


class Camera():

    def __init__(self, folder_name):
        self.absolute_folder_name = folder_name     
        self.camera_index = self.find_camera_index() #Se cambia con cambio de metodo
        # ~ self.method = 1 #1 con uvccapture y terminal, 2 con cv2. falta implementar este filtro


    def init_camera(self):
        self.cam = cv2.VideoCapture(self.camera_index) #Se cambia con cambio de metodo
        self.cam_settings() #Se cambia con cambio de metodo
        pass

    def grab_image(self, num):
        try:
            ret, img = self.cam.read()
            if ret:
                save = cv2.imwrite(f'{self.absolute_folder_name}/img{num}.jpg', img)
            else:
                print("Error en captura de imagen")    
            
        except:
            print("Camara en otro lado")
        
            
    def grab_image_alt(self, num):
        try:
            img = subprocess.run(['uvccapture', f'-o{self.absolute_folder_name}/img{num}.jpg','-B10','-x2592', '-y1944', '-t0'])   
            # ~ img = subprocess.run(['uvccapture', f'-o{self.absolute_folder_name}/img{num}.jpg','-B10','-x2592', '-y1944','-v', '-t0'])    
            #uvccapture -S40 -C30 -G80 -B10 -x2592 -y1944 -v -t0 -otest.jpg
            if img.returncode == 0:
                # ~ print('foto capturada con exito')
                pass
        except:
            print("Camara en otro lado")

    def deinit_camera(self):
        self.cam.release() #Se cambia con cambio de metodo
        cv2.destroyAllWindows() #Se cambia con cambio de metodo
        pass

    def find_camera_index(self):
        camera_path = "Not Found"
        for i in range(0,3):
            try:
                existe = cv2.VideoCapture(i)
                if existe is None or not existe.isOpened():
                    pass
                else:
                    camera_path = i                
            except:
                pass
        return camera_path


    def cam_settings(self):
		#Propiedades en https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
		#Se puede llamar por indice o nombre de la propiedad
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,2592)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1944)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS,10)



    
        
    def stream(self, num):
        while True:
            ret, frame = self.cam.read()
            cv2.imshow("imagen", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                 break


if __name__ == '__main__':
    path_to_imgs = "imgs_test"
    os.makedirs("imgs_test", exist_ok=True)
    cam = Camera(path_to_imgs)
    # ~ cam.grab_image(2)
    
    try:
        cam.init_camera()
        cam.grab_image(1)
        cam.deinit_camera()
    except KeyboardInterrupt:
        print("Saliendo bien")
        cam.deinit_camera()
        sys.exit(1)  
    
    
