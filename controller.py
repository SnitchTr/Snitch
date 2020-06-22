from pyPS4Controller.controller import Controller, Event
from pyfirmata import Arduino, util
board = Arduino('/dev/ttyACM0')
pindretaf = board.get_pin("d:13:o")
pindretab = board.get_pin("d:12:o")
PWMdreta = board.get_pin("d:11:p")
pinesquerraf = board.get_pin("d:8:o")
pinesquerrab = board.get_pin("d:7:o")
PWMesquerra = board.get_pin("d:10:p")
def connect(self):
    self.is_up_arrow_pressed = False
    self.is_down_arrow_pressed = False
    self.is_right_arrow_pressed = False
    self.is_left_arrow_pressed = False
    self.is_R1_pressed = False
    pass


def connect(self):
    self.is_up_arrow_pressed = False
    self.is_down_arrow_pressed = False
    self.is_right_arrow_pressed = False
    self.is_left_arrow_pressed = False
    self.is_R1_pressed = False
    
class State:
    def __init__(self):
        self.PWM = 0
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.is_R1_pressed = False


class MyController(Controller):
    
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def rightmotorf(self):
        pindretaf.write(1)
        pindretab.write(0)
        PWMdreta.write(self.PWM)
    def rightmotorb(self):
        pindretaf.write(0)
        pindretab.write(1)
        PWMdreta.write(self.PWM)
    def rightmotorstop(self):
        pindretaf.write(0)
        pindretab.write(0)
        PWMdreta.write(0)
    def leftmotorf(self):
        pinesquerraf.write(1)
        pinesquerrab.write(0)
        PWMesquerra.write(self.PWM)
    def leftmotorb(self):
        pinesquerraf.write(0)
        pinesquerrab.write(1)
        PWMesquerra.write(self.PWM)
    def leftmotorstop(self):
        pinesquerraf.write(0)
        pinesquerrab.write(0)
        PWMesquerra.write(0)


    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def on_up_arrow_press(self):
        self.is_up_arrow_pressed = True

    def on_down_arrow_press(self):
        self.is_down_arrow_pressed = True

    def on_up_down_arrow_release(self):
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False

    def on_right_arrow_press(self):
        self.is_right_arrow_pressed = True

    def on_left_arrow_press(self):
        self.is_left_arrow_pressed = True

    def on_left_right_arrow_release(self):
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
    def on_L1_press(self):
        self.is_R1_pressed = True
    def on_L1_release(self):
        self.is_R1_pressed = False
    def on_x_press(self):
        self.PWM = 0

    def on_L2_press(self,value):
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.is_R1_pressed = False
        self.PWM = ((((value + 32767)/(32767*2))*145)+60)/255
        if self.is_up_arrow_pressed == True:
            self.rightmotorf()
            self.leftmotorf()
        elif self.is_down_arrow_pressed == True:
            self.rightmotorb()
            self.leftmotorb()
        elif self.is_right_arrow_pressed == True:
            if self.is_R1_pressed == True:
                self.rightmotorb()
                self.leftmotorf()
            else:
                self.rightmotorstop()
                self.leftmotorf()
        elif self.is_left_arrow_pressed == True:
            if self.is_R1_pressed == True:
                self.rightmotorf()
                self.leftmotorb()
            else:
                self.rightmotorf()
                self.leftmotorstop()
        else:
            self.rightmotorstop()
            self.leftmotorstop()
    def on_L2_release(self):
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.is_R1_pressed = False
        self.PWM = 0
    
    def on_share_press(self):
        self.is_up_arrow_pressed = False
        self.is_down_arrow_pressed = False
        self.is_right_arrow_pressed = False
        self.is_left_arrow_pressed = False
        self.is_R1_pressed = False
        self.PWM = 0

    def on_share_release(self):
        exit()





class MyEventDefinition(Event):


    def x_pressed(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 1

    def x_released(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 0

    def circle_pressed(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 1

    def circle_released(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 0

    def triangle_pressed(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 1

    def triangle_released(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 0

    def square_pressed(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 1

    def square_released(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 0


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, event_definition=MyEventDefinition)
controller.listen()

