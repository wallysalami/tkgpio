from gpiozero.pins.mock import MockFactory, MockTriggerPin, MockPWMPin, MockChargingPin
from gpiozero.pins.local import SPI
from gpiozero import SPIBadChannel
from gpiozero.devices import GPIOMeta, GPIOBase
from PIL import ImageTk, Image
from time import sleep, perf_counter
from os import path
from tkinter import Label
from math import ceil, log


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    
class SingletonGPIOMeta(SingletonMeta, GPIOMeta):
    pass


class TkDevice():
    _images = {}
    
    def __init__(self, root, x, y, name):
        self._root = root
        self._name = name
        self._x = x
        self._y = y
        self._widget = None
        self._image_states = {}
        
        text_label = Label(root, text=name, background="white", foreground="black", anchor="w", font=("Arial", 13))
        text_label.place(x=x, y=y-20)
        
    def _redraw(self):
        self._root.update()
    
    def _create_main_widget(self, widget_class, initial_state=None, x_offset=0, y_offset=0):
        self._widget = widget_class(self._root, background="white")
        self._widget.place(x=self._x+x_offset, y=self._y+y_offset)
        
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
                image = image.resize(dimensions, Image.LANCZOS)
            
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
        
        
class MockSPI(SPI, metaclass=SingletonGPIOMeta if issubclass(SPI, GPIOBase) else SingletonMeta):
    
    def __init__(self, *args, **kwargs):
        self._values = {}
        self.device_code = 3008
    
    def close(self):
        pass
        
    def _int_to_words(self, pattern):
        if self.device_code in [3001, 3002, 3201, 3301]:
            bits_required = 16
        else:
            bits_required = 24
            
        shifts = range(0, bits_required, self.bits_per_word)[::-1]
        mask = 2 ** self.bits_per_word - 1
        
        return [(pattern >> shift) & mask for shift in shifts]
    
    def _get_channel(self, data):
        if self.device_code in [3001, 3201, 3301]:
            return 0  
        elif self.device_code == 3002:
            return (data[0] >> 4) & 0b0001
        elif self.device_code == 3202:
            return (data[1] >> 6) & 0b0001
        elif self.device_code in [3004, 3008]:
            return (data[1] >> 4) & 0b0111
        elif self.device_code in [3204, 3208]:
            return (data[0] & 1) << 2 | data[1] >> 6
        elif self.device_code in [3302, 3304]:
            return (data[0] & 0b11) << 1 | data[1] >> 7
            
    def _get_bit_resolution(self):
        if self.device_code // 100 == 30:
            return 10
        else:
            return 12
    
    def transfer(self, data):
        channel = self._get_channel(data)
        value = self._values.get(channel, 0)
        bits = self._get_bit_resolution()
        min_value = -(2 ** bits)
        value_range = 2 ** (bits + 1) - 1
        int_value = int( (value + 1) * value_range / 2 + min_value )
        
        if self.device_code == 3001:
            int_value = int_value << 3
        elif self.device_code == 3201:
            int_value = int_value << 1

        return self._int_to_words(int_value)
    
    def set_value_for_channel(self, value, channel):
        max_channel = self.device_code % 10 - 1
        if not isinstance(channel, int) or channel < 0 or channel > max_channel:
            raise SPIBadChannel("channel must be between 0 and %d" % max_channel)
        
        self._values[channel] = value
    
        
class PreciseMockFactory(MockFactory):
    def __init__(self, revision=None, pin_class=None):
        super(PreciseMockFactory, self).__init__(revision=revision, pin_class=pin_class)
        self.spi_classes = {
            ('hardware', 'exclusive'): MockSPI,
            ('hardware', 'shared'):    MockSPI,
            ('software', 'exclusive'): MockSPI,
            ('software', 'shared'):    MockSPI,
        }
        
    def spi(self, **spi_args):
        return MockSPI()
      
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

