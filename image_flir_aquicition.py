import time
import os
import user_settings

if user_settings.MAQUINA == 'Windows':
    from pyspin import PySpin
else:
    import PySpin

class Camera():

    def __init__(self, folder_name):
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam = self.cam_list[0]
        self.folder_name = folder_name


    def init_camera(self):
        self.cam.Init()
        self.node_setting()
       
    def grab_image(self, num):

        self.cam.BeginAcquisition()
        #self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        #exposure_time_to_set = 17996
        #self.cam.ExposureTime.SetValue(5750)

        image_result = self.cam.GetNextImage()
        if image_result.IsIncomplete():
            print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
        else:
            image_converted = image_result.Convert(PySpin.PixelFormat_RGB8, PySpin.HQ_LINEAR)
            filename = f'{self.folder_name}/img{num}.jpg'
            if not os.path.isdir(self.folder_name):
                print(f'Creando {self.folder_name} para guardar fotos')
                os.makedirs('imgs')

            image_converted.Save(filename)
            image_result.Release()
        self.cam.EndAcquisition()



    def deinit_camera(self):
        self.cam.DeInit()
        del self.cam
        try:
            self.cam_list.Clear()
            self.system.ReleaseInstance()
        except:
            print("Problema con la camara, ")
            pass

    def print_with_indent(self, level, text):
        """
        Helper function for printing a string prefix with a specifc number of indents.
        :param level: Number of indents to generate
        :type level: int
        :param text: String to print after indent
        :type text: str
        """
        ind = ''
        for i in range(level):
            ind += '    '
        print('%s%s' % (ind, text))


    def node_setting(self):
        nodemap_applayer = self.cam.GetNodeMap()
        nodemap_applayer.GetNode('')

        enum_settings = {'AcquisitionMode': 'Continuous',
                         'ExposureAuto': 'Continuous',
                         'PixelFormat': 'BayerRG8',
                         'GainAuto': 'Continuous'
                         }
        float_settings = {'AutoExposureExposureTimeUpperLimit': 50000,
                          'AutoExposureExposureTimeLowerLimit': 10,
                          }
        # node_pixel_format_mono8 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono8'))

        for name, value in enum_settings.items():
            node = PySpin.CEnumerationPtr(nodemap_applayer.GetNode(name))
            node_format = PySpin.CEnumEntryPtr(node.GetEntryByName(value))
            era = node.GetCurrentEntry().GetSymbolic()
            node.SetIntValue(node_format.GetValue())

            print(f' El nodo {name} estaba con valor: {era} y quedo con valor: {node.GetCurrentEntry().GetSymbolic()}')

        for name, value in float_settings.items():
            node = PySpin.CFloatPtr(nodemap_applayer.GetNode(name))
            era = node.GetValue()
            node.SetValue(value)
            print(f' El nodo {name} tenia un valor: {era} y quedo con valor: {node.GetValue()}')



        # Get and print display name
        #display_name = node_category.GetDisplayName()
        #self.print_with_indent(level, display_name)


    



if __name__ == '__main__':
    path_to_imgs = "imgs_test"
    os.makedirs("imgs_test", exist_ok=True)
    cam = Camera(path_to_imgs)
    cam.init_camera()
    cam.grab_image('test')
    #cam.node_setting('AcquisitionMode', 2)
    cam.deinit_camera()
