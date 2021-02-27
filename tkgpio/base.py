from gpiozero.pins.mock import MockFactory, MockTriggerPin, MockPWMPin, MockChargingPin
from PIL import ImageTk, Image
from time import sleep, perf_counter
from os import path
from tkinter import Label

class TkDevice():
    _images = {}
    
    def __init__(self, root, x, y, name):
        self._root = root
        self._name = name
        self._x = x
        self._y = y
        self._widget = None
        self._image_states = {}
        
        text_label = Label(root, text=name, background="white", anchor="w", font=("Arial", 13))
        text_label.place(x=x, y=y-20)
        
    def _redraw(self):
        self._root.update()
    
    def _create_main_widget(self, widget_class, initial_state=None):
        self._widget = widget_class(self._root, background="white")
        self._widget.place(x=self._x, y=self._y)
        
        if initial_state != None:
            self._change_widget_image(initial_state)
        
        return self._widget
    
    def _set_image_for_state(self, image_file_name, state, dimensions=None):
        if image_file_name in TkDevice._images:
            image = TkDevice._images[image_file_name]
        else:
            current_folder = path.dirname(__file__)
            file_path = path.join(current_folder, "resources/images/" + image_file_name)

            image = Image.open(file_path)
            if dimensions != None:
                image = image.resize(dimensions, Image.ANTIALIAS)
            
            TkDevice._images[image_file_name] = image
            
        self._image_states[state] = image
        
        return image
        
    def _change_widget_image(self, image_or_state):
        if self._widget != None:
            if isinstance(image_or_state, str):
                state = image_or_state
                image = self._image_states[state]
            else:
                image = image_or_state
        
            self._photo_image = ImageTk.PhotoImage(image)
            self._widget.configure(image=self._photo_image)
        
            self._redraw()


class PreciseMockTriggerPin(MockTriggerPin, MockPWMPin):
    def _echo(self):
        sleep(0.001)
        self.echo_pin.drive_high()
        
        # sleep(), time() and monotonic() dont have enough precision!
        init_time = perf_counter()
        while True:
            if perf_counter() - init_time >= self.echo_time:
                break
        
        self.echo_pin.drive_low()
        
        
class PreciseMockFactory(MockFactory):
    @staticmethod
    def ticks():
        # time() and monotonic() dont have enough precision!
        return perf_counter()
    

class PreciseMockChargingPin(MockChargingPin, MockPWMPin):
    
    def _charge(self):
        init_time = perf_counter()
        while True:
            if perf_counter() - init_time >= self.charge_time:
                break
        
        try:
            self.drive_high()
        except AssertionError:
            pass
    pass
    

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
