from .base import TkDevice, SingletonMeta, MockSPI
from .base import PreciseMockTriggerPin, PreciseMockFactory, PreciseMockChargingPin
from gpiozero import Device
from gpiozero.pins.mock import MockPWMPin, MockSPIDevice
from PIL import ImageEnhance, Image, ImageDraw, ImageFont, ImageTk
from tkinter import Tk, Frame, Label, Button, Scale, Canvas, HORIZONTAL, VERTICAL, CENTER
from threading import Thread, Timer
from sys import path, exit
from pathlib import Path
from functools import partial
from math import sqrt
import os
      
      
class TkCircuit(metaclass=SingletonMeta):
    def __init__(self, setup):
        Device.pin_factory = PreciseMockFactory(pin_class=MockPWMPin)
        
        path.insert(0, str(Path(__file__).parent.absolute()))
        
        default_setup = {
            "name": "Virtual GPIO",
            "width": 500, "height": 500,
            "leds":[], "buzzers":[],
            "buttons":[], "toggles": [],
            "lcds":[],
            "motors":[], "servos":[],
            "motion_sensors": [],
            "distance_sensors": [],
            "light_sensors": [],
            "adc": None,
            "infrared_receiver": None, "infrared_emitter": None,
            "labels": [],
        }
        
        default_setup.update(setup)
        setup = default_setup
        
        self._root = Tk()
        self._root.title(setup["name"])
        self._root.geometry("%dx%d" % (setup["width"], setup["height"]))
        self._root.resizable(False, False)
        self._root["background"] = "white"
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._root.tk.call("tk", "scaling", 1.0)
        
        for parameters in setup["labels"]:
            self.add_device(TkLabel, parameters)
        
        self._outputs = []
        self._outputs += [self.add_device(TkLED, parameters) for parameters in setup["leds"]]
        self._outputs += [self.add_device(TkBuzzer, parameters) for parameters in setup["buzzers"]]
        self._outputs += [self.add_device(TkMotor, parameters) for parameters in setup["motors"]]
        self._outputs += [self.add_device(TkServo, parameters) for parameters in setup["servos"]]
        
        self._lcds = [self.add_device(TkLCD, parameters) for parameters in setup["lcds"]]
        
        if setup["adc"] != None:
            spi = TkSPI(setup["adc"]["mcp_chip"])
            for parameters in setup["adc"]["potentiometers"]:
                parameters["tk_spi"] = spi
                self.add_device(TkPotentiometer, parameters)
                
        for parameters in setup["buttons"]:
            self.add_device(TkButton, parameters)
            
        for parameters in setup["toggles"]:
            self.add_device(TkToggle, parameters)
            
        for parameters in setup["distance_sensors"]:
            self.add_device(TkDistanceSensor, parameters)
            
        for parameters in setup["light_sensors"]:
            self.add_device(TkLightSensor, parameters)
            
        for parameters in setup["motion_sensors"]:
            self.add_device(TkMotionSensor, parameters)
        
        if setup["infrared_receiver"] != None:
            self.add_device(TkInfraredReceiver, setup["infrared_receiver"])
             
        if setup["infrared_emitter"] != None:
            self.add_device(TkInfraredEmitter, setup["infrared_emitter"])
            
    def add_device(self, device_class, parameters):
        return device_class(self._root, **parameters)
        
    def run(self, function):
        thread = Thread(target=function, daemon=True)
        thread.start()
        
        self._root.after(10, self._update_outputs)    
        self._root.mainloop()
        
    def _update_outputs(self):
        for output in self._outputs:
            output.update()
            
        self._root.after(10, self._update_outputs)
        
    def update_lcds(self, pins, text):
        for lcds in self._lcds:
            lcds.update_text(pins, text)
            
    def _on_closing(self):
        exit()
  
  
class TkLabel:
    def __init__(self, root, x, y, text="", font_family="Arial", font_size=13, **kwargs):
        default_setup = {
            "text": text,
            "font": (font_family, font_size),
            "background": "white", "foreground": "black",
        }
        
        default_setup.update(kwargs)
        kwargs = default_setup
        
        text_label = Label(root, **kwargs)
        text_label.place(x=x, y=y)
        
        
class TkLCD(TkDevice):
    _image = None
    _photo_image = None
    
    def __init__(self, root, x, y, name, pins, columns, lines):
        super().__init__(root, x, y, name)
        self._redraw()
     
        self._pins = pins
        self._columns = columns
        self._lines = lines
            
        self._label = Label(root)
        self._label.place(x=x, y=y)
        
        self.update_text(self._pins, "")
        
    def update_text(self, pins, text):
        MARGIN = 8
        FONT_SIZE = 17
        CHAR_WIDTH = 12
        CHAR_HEIGHT = 16
        CHAR_X_GAP = 3
        CHAR_Y_GAP = 5
        
        image_width = MARGIN * 2 + self._columns * (CHAR_WIDTH) + (self._columns - 1) * CHAR_X_GAP
        image_height = MARGIN * 2 + self._lines * (CHAR_HEIGHT) + (self._lines - 1) * CHAR_Y_GAP
        
        if pins == self._pins:
            image = Image.new('RGB', (image_width, image_height), color="#82E007")
 
            current_folder = os.path.dirname(__file__)
            font_path = os.path.join(current_folder, "resources/fonts/hd44780.ttf")
            font = ImageFont.truetype(font_path, FONT_SIZE)
            d = ImageDraw.Draw(image)
            
            x = MARGIN
            for j in range(0, self._columns):
                y = MARGIN
                for i in range(0, self._lines):
                    d.rectangle((x, y, x+CHAR_WIDTH, y+CHAR_HEIGHT), fill ="#72D000")
                    y += (CHAR_Y_GAP + CHAR_HEIGHT)
                    
                x += (CHAR_X_GAP + CHAR_WIDTH)
                    
            x = MARGIN
            y = MARGIN
            line = 1
            column = 1
            for character in text:
                if character == "\n":
                    y += (CHAR_Y_GAP + CHAR_HEIGHT)
                    x = MARGIN
                    line += 1
                    column = 1
                else:
                    if line <= self._lines and column <= self._columns:
                        d.text((x,y), character, font=font, fill="black")
                        
                    x += (CHAR_X_GAP + CHAR_WIDTH)
                    column += 1
            
            self._photo_image = ImageTk.PhotoImage(image)
            
            self._label.configure(image = self._photo_image)
            self._redraw()
            self._root.update()
        
        
class TkBuzzer(TkDevice):
    SAMPLE_RATE = 44100
    SIGNAL_DURATION = 0.1
    AMPLITUDE = 0.1
    
    try:
        import sounddevice
        import numpy
        _sounddevice = sounddevice
        _numpy = numpy
    except Exception:
        _sounddevice = None
        _numpy = None
    
    def __init__(self, root, x, y, name, pin, frequency=440):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        self._previous_state = None
        
        self._set_image_for_state("buzzer_on.png", "on", (50, 33))
        self._set_image_for_state("buzzer_off.png", "off", (50, 33))
        self._create_main_widget(Label, "off", x_offset=-15)
        
        self._stream = None
        
        if frequency != None and TkBuzzer._numpy != None:
            # adjust the duration to match a multiple of the signal period
            period = 1 / frequency
            duration = TkBuzzer.SIGNAL_DURATION + (period - TkBuzzer.SIGNAL_DURATION % period)
            
            np = TkBuzzer._numpy
            n_samples = int(TkBuzzer.SAMPLE_RATE * duration)
            t = np.linspace(0, duration, n_samples, endpoint=False)
            sine = np.sin(2 * np.pi * frequency * t)
            square_wave = np.sign(sine)
            self._sample_wave = (TkBuzzer.AMPLITUDE / 2 * square_wave.astype(np.int16))
        else:
            self._sample_wave = None
        
    def update(self):
        if self._previous_state != self._pin.state:
            if self._pin.state == True:
                self._change_widget_image("on")
                self._play_sound()
            else:
                self._change_widget_image("off")
                self._stop_sound()
            
            self._previous_state = self._pin.state
            
            self._redraw()
            
    def _play_sound(self):
        if TkBuzzer._sounddevice != None and self._sample_wave is not None:
            self._playback_position = 0
            self._stream = TkBuzzer._sounddevice.OutputStream(
                callback=lambda *args: self._sound_callback(*args),
                channels=1,
                samplerate=TkBuzzer.SAMPLE_RATE
            )
            self._stream.start()
    
    def _stop_sound(self):
        if self._stream != None:
            self._stream.stop()
            
    def _sound_callback(self, outdata, frames, time, status):
        remaining_frames = len(self._sample_wave) - self._playback_position

        if remaining_frames >= frames:
            segment = self._sample_wave[self._playback_position:self._playback_position + frames]
            outdata[:] = segment.reshape(-1, 1)
            self._playback_position += frames
        else:
            # Loop back to the beginning
            segment1 = self._sample_wave[self._playback_position:]
            segment2 = self._sample_wave[0 : frames - remaining_frames]
            segment = TkBuzzer._numpy.concatenate((segment1, segment2))
            outdata[:] = segment.reshape(-1, 1)
            self._playback_position = frames - remaining_frames

            

class TkLED(TkDevice):
    on_image = None
    
    def __init__(self, root, x, y, name, pin):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        self._previous_state = None
        
        TkLED.on_image = self._set_image_for_state("led_on.png", "on", (19, 30))
        self._set_image_for_state("led_off.png", "off", (19, 30))
        self._create_main_widget(Label, "off")
        
    def update(self):
        if self._previous_state != self._pin.state:
            if isinstance(self._pin.state, float):
                converter = ImageEnhance.Color(TkLED.on_image)
                desaturated_image = converter.enhance(self._pin.state)
                self._change_widget_image(desaturated_image)
            elif self._pin.state == True:
                self._change_widget_image("on")
            else:
                self._change_widget_image("off")
             
            self._previous_state = self._pin.state
            
            self._redraw()
            

class TkMotor(TkDevice):
    _image = None
    
    def __init__(self, root, x, y, name, forward_pin, backward_pin):
        super().__init__(root, x, y, name)
        
        self._forward_pin = Device.pin_factory.pin(forward_pin)
        self._backward_pin = Device.pin_factory.pin(backward_pin)
        
        TkMotor._image = self._set_image_for_state("motor.png", "normal")
        
        self._canvas = Canvas(self._root, width=60, height=60,
                              background="white", borderwidth=0, highlightthickness=0)
        self._canvas.place(x=x, y=y)
        self._canvas_object = None
        
        self._angle = 0
        
    def angle_speed(self):
        if self._forward_pin.state > 0:
            return -self._forward_pin.state * 20
        else:
            return self._backward_pin.state * 20
           
    def update(self):
        if self._canvas_object != None:
            self._canvas.delete(self._canvas_object)
        self._photo_image = ImageTk.PhotoImage(TkMotor._image.rotate(self._angle, resample=Image.BICUBIC))
        self._canvas_object = self._canvas.create_image(30, 30, image=self._photo_image)
        self._canvas.update()
        
        self._angle += self.angle_speed()
        self._angle %= 360
        
        
class TkServo(TkDevice):
    _base_image = None
    _arm_image = None
    
    def __init__(self, root, x, y, name, pin, initial_angle=0, min_angle=-90, max_angle=90, min_pulse_width=1/1000, max_pulse_width=2/1000):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._min_pulse_width = min_pulse_width
        self._max_pulse_width = max_pulse_width
        
        TkServo._base_image = self._set_image_for_state("servo_base.png", "normal", (75, 27))
        TkServo._arm_image = self._set_image_for_state("servo_arm.png", "normal")
        
        self._canvas = Canvas(self._root, width=100, height=90,
                              background="white", borderwidth=0, highlightthickness=0)
        self._canvas.place(x=x, y=y)
        self._canvas_object = None
        
        self._base_photo_image = ImageTk.PhotoImage(TkServo._base_image)
        base_object = self._canvas.create_image(37, 45, image=self._base_photo_image)
        self._canvas.update()
        
        self._angle = initial_angle
        self._previous_angle = None
        self.update()
        
    def _update_angle(self):
        if self._pin._frequency == None:
            return
        pulse_width = self._pin._state * (1 / self._pin._frequency)
        pulse_width = min(self._max_pulse_width, max(pulse_width, self._min_pulse_width))
        
        a = (self._max_angle - self._min_angle) / (self._max_pulse_width - self._min_pulse_width)
        b = self._max_angle - a * self._max_pulse_width
        self._angle = a * pulse_width + b
        
    def update(self):
        self._update_angle()
        
        if self._previous_angle != self._angle:        
            if self._canvas_object != None:
                self._canvas.delete(self._canvas_object)
            rotated_image = TkServo._arm_image.rotate(self._angle, resample=Image.BICUBIC)
            self._arm_photo_image = ImageTk.PhotoImage(rotated_image)
            self._canvas_object = self._canvas.create_image(54, 45, image=self._arm_photo_image)
            self._canvas.update()
            
            self._previous_angle = self._angle
        
        
class TkButton(TkDevice):
    def __init__(self, root, x, y, name, pin):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        self._set_image_for_state("button_pressed.png", "on", (30, 30))
        self._set_image_for_state("button_released.png", "off", (30, 30))
        self._create_main_widget(Button, "off")
        self._widget.config(borderwidth=0,highlightthickness = 0,background="white")
        self._widget.bind("<ButtonPress>", self._on_press)
        self._widget.bind("<ButtonRelease>", self._on_release)
        
    def _on_press(self, botao):
        self._change_widget_image("on")
        
        thread = Thread(target=self._change_pin, daemon=True, args=(True,))
        thread.start()

    def _on_release(self, botao):
        self._change_widget_image("off")
        
        thread = Thread(target=self._change_pin, daemon=True, args=(False,))
        thread.start()
        
    def _change_pin(self, is_press):
        if is_press:
            self._pin.drive_low()
        else:
            self._pin.drive_high()
            

class TkToggle(TkDevice):
    def __init__(self, root, x, y, name, pin, on_label="ON", off_label="OFF", is_on=False):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        if off_label != "" and off_label != None:
            left_label = Label(root, text=off_label, background="white", foreground="black", anchor="w", font=("Arial", 13))
            left_label.place(x=x, y=y)
            left_label.update()
            switch_x = x + left_label.winfo_width()
        else:
            switch_x = x
        
        self._scale = Scale(root, from_=0, to=1, showvalue=0,
                            orient=HORIZONTAL, command=self._scale_changed, sliderlength=20, length=40,
                            highlightthickness=0, background="white")
        self._scale.place(x=switch_x, y=y)
        self._scale.set(int(is_on))
        self._scale_changed(self._scale.get())
        
        right_label = Label(root, text=on_label, background="white", foreground="black", anchor="w", font=("Arial", 13))
        right_label.place(x=switch_x+50, y=y)

    def _scale_changed(self, value):
        if int(value) == 1:
            self._pin.drive_low()
        else:
            self._pin.drive_high()
          
            
class TkMotionSensor(TkDevice):
    def __init__(self, root, x, y, name, pin, detection_radius=50, delay_duration=5, block_duration=3):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin)
        
        self._detection_radius = detection_radius
        self._delay_duration = delay_duration
        self._block_duration = block_duration
        
        self._motion_timer = None
        self._block_timer = None
        
        self._set_image_for_state("motion_sensor_on.png", "motion", (80, 60))
        self._set_image_for_state("motion_sensor_off.png", "no motion", (80, 60))
        self._set_image_for_state("motion_sensor_wait.png", "wait", (80, 60))
        self._create_main_widget(Label, "no motion")
        
        root.bind('<Motion>', self._motion_detected, add="+")
        
    def _motion_detected(self, event):
        x_pointer = self._root.winfo_pointerx() - self._root.winfo_rootx()
        y_pointer = self._root.winfo_pointery() - self._root.winfo_rooty()
        x_center = self._widget.winfo_x() + self._widget.winfo_width() / 2
        y_center = self._widget.winfo_y() + self._widget.winfo_height() / 2
        distance = sqrt(pow(x_pointer - x_center, 2) + pow(y_pointer - y_center, 2))
        
        if distance < self._detection_radius and self._block_timer == None:
            if self._motion_timer == None:
                self._change_widget_image("motion")
            else:
                self._motion_timer.cancel()
                
            self._pin.drive_high()
                 
            self._motion_timer = Timer(self._delay_duration, self._remove_detection)
            self._motion_timer.start()
            
    def _remove_detection(self):
        self._pin.drive_low()
        self._change_widget_image("wait")
        
        self._motion_timer = None
        
        self._block_timer = Timer(self._block_duration, self._remove_block)
        self._block_timer.start()
    
    def _remove_block(self):
        self._change_widget_image("no motion")
        self._block_timer = None
            
            
class TkDistanceSensor(TkDevice):
    def __init__(self, root, x, y, name, trigger_pin, echo_pin, min_distance=0, max_distance=50):
        super().__init__(root, x, y, name)
        
        self._echo_pin = Device.pin_factory.pin(echo_pin)
        self._trigger_pin = Device.pin_factory.pin(trigger_pin,
            pin_class=PreciseMockTriggerPin, echo_pin=self._echo_pin, echo_time=0.004)
        
        self._echo_pin._bounce = 0
        self._trigger_pin._bounce = 0
        
        self._set_image_for_state("distance_sensor.png", "normal", (83, 50))
        self._create_main_widget(Label, "normal")
        
        self._scale = Scale(root, from_=min_distance, to=max_distance,
            orient=HORIZONTAL, command=self._scale_changed, sliderlength=20, length=150,
                            highlightthickness = 0, background="white", foreground="black")
        self._scale.place(x=x+100, y=y)
        self._scale.set(round((min_distance + max_distance) / 2))
        self._scale_changed(self._scale.get())
        
    def _scale_changed(self, value):
        speed_of_sound = 343.26 # m/s
        distance = float(value) / 100 # cm -> m
        self._trigger_pin.echo_time = distance * 2 / speed_of_sound
      
      
class TkLightSensor(TkDevice):
    def __init__(self, root, x, y, name, pin):
        super().__init__(root, x, y, name)
        
        self._pin = Device.pin_factory.pin(pin, pin_class=PreciseMockChargingPin)
        
        self._scale = Scale(root, from_=0, to=90, showvalue=0,
            orient=VERTICAL, command=self._scale_changed, sliderlength=20, length=150, highlightthickness = 0, background="white")
        self._scale.place(x=x+90, y=y)
        self._scale.set(30)
        self._scale_changed(self._scale.get())
        
        self._set_image_for_state("light_sensor.png", "normal", (75, 150))
        self._create_main_widget(Label, "normal")
        
    def _scale_changed(self, value):
        self._pin.charge_time = float(value) / 10000
        
        
class TkSPI(object):
    def __init__(self, device_code):
        self.mock_spi = MockSPI()
        self.mock_spi.device_code = device_code
        
        
class TkPotentiometer(TkDevice):
    def __init__(self, root, x, y, name, tk_spi, channel):
        super().__init__(root, x, y, name)
        
        self._tk_spi = tk_spi
        self._channel = channel
        
        self._scale = Scale(root, from_=0, to=1, resolution=0.01, showvalue=0,
            orient=HORIZONTAL, command=self._scale_changed, sliderlength=20, length=150, highlightthickness = 0, background="white")
        self._scale.place(x=x, y=y)
        self._scale.set(0.5)
        self._scale_changed(self._scale.get())
        
    def _scale_changed(self, value):
        self._tk_spi.mock_spi.set_value_for_channel(float(value), self._channel)
            
            
class TkInfraredReceiver(TkDevice, metaclass=SingletonMeta):

    def __init__(self, root, x, y, name, config, remote_control):
        super().__init__(root, x, y, name)
        
        remote = remote_control
        
        frame = Frame(root, bg = remote["color"], width = remote["width"], height = remote["height"])
        frame.place(x=x, y=y)
        
        self._config = config
        self._key_codes = []
        self._pressed_key_codes = []
        
        for i in range(0, len(remote["key_rows"])):
            row = remote["key_rows"][i]
            for j in range(0, len(row["buttons"])):
                button_setup = row["buttons"][j]
                if button_setup != None:
                    code = button_setup.get("code", "KEY_" + button_setup["name"])
                    self._key_codes.append(code)
                    
                    command = partial(self._key_press, code)
                    
                    button = Button(frame, text=button_setup["name"],
                                    width=remote["key_width"], height=remote["key_height"],
                                    command=command,
                                    justify=CENTER, highlightbackground=remote["color"])
                    button.grid(row=i, column=j, padx=8, pady=8)
        
        frame.configure(width = remote["width"], height = remote["height"])
    
    def config_name(self):
        return self._config
    
    def clear_codes(self):
        self._pressed_key_codes = []
    
    def get_next_code(self):
        if len(self._pressed_key_codes) == 0:
            return []
        else:
            return [self._pressed_key_codes.pop(0)]
    
    def _key_press(self, code):
        self._pressed_key_codes.append(code)
        
        
class TkInfraredEmitter(TkDevice, metaclass=SingletonMeta):
    def __init__(self, root, x, y, name, remote_controls):
        super().__init__(root, x, y, name)
        
        self._set_image_for_state("emitter_on.png", "on", (50, 30))
        self._set_image_for_state("emitter_off.png", "off", (50, 30))
        self._create_main_widget(Label, "off")
        
        self._remote_controls = remote_controls
        
        self._timer = None
        
    def list_remotes(self, remote):
        return self._remote_controls.keys()
    
    def list_codes(self, remote):
        valid_codes = self._remote_controls.get(remote, None)
        
        if valid_codes == None:
             print("\x1b[1;37;41m" + remote + ": INVALID REMOTE CONTROL!" + "\x1b[0m")
             
        return valid_codes
        
    def send_once(self, remote, codes, count):
        valid_codes = self.list_codes(remote)
        if valid_codes == None:
            return
        
        has_valid_code = False
        for code in codes:
            if code in valid_codes:
                print("\x1b[1;37;42m" + code + " of remote \"" + remote + "\" transmitted!" + "\x1b[0m")
                has_valid_code = True
            else:
                print("\x1b[1;37;41m" + code + ": INVALID CODE FOR REMOTE \"" + remote +  "\"!" + "\x1b[0m")
                
        if has_valid_code:
            if self._timer != None:
                self._timer.cancel()
                
            self._change_widget_image("on")
                
            self._timer = Timer(1, self._turn_off_emitter).start()
            
    def _turn_off_emitter(self):
        self._change_widget_image("off")
        self._timer = None
