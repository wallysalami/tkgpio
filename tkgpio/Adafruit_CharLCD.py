from tkgpio import TkCircuit

class Adafruit_CharLCD(object):
    """Class to represent and interact with an HD44780 character LCD display."""
    
    # I'm not using this variable, but it might be useful to someone who is looking for a list of special characters in LCDs
    SPECIAL_CHARACTERS = "→←。「」、・ァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜αäßεµσρq√יּϳˣ¢Ⱡñöpqθ∞ΩüΣπx̄y干九円÷ ▮̄"

    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines, backlight=None,
                    invert_polarity=True,
                    enable_pwm=False,
                    gpio=None,
                    pwm=None,
                    initial_backlight=1.0):
        self._pins = [rs, en, d4, d5, d6, d7]
        self._columns = cols
        self._lines = lines
        self._backlight = backlight
        self._displaymode = "left"
        self.clear()

    def home(self):
        pass

    def clear(self):
        self._text = ""
        
        app = TkCircuit()
        app.update_lcds(self._pins, self._text)

    def set_cursor(self, col, row):
        pass

    def enable_display(self, enable):
        pass

    def show_cursor(self, show):
        pass

    def blink(self, blink):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def set_left_to_right(self):
        self._displaymode = "left"
        pass

    def set_right_to_left(self):
        self._displaymode = "right"
        pass

    def autoscroll(self, autoscroll):
        pass

    def message(self, text):
        text_with_special_characters = ""
        for character in text:
            if character != "\n":
                code = ord(character)
                code = code % 255
                character = chr(code)
                
                if code <= 31 or (code >= 128 and code <= 161):
                    character = " "
                    
            text_with_special_characters += character
        
        self._text += text_with_special_characters
        fixed_text = self._text
        
        
        # limit text to lcd's dimensions (lines and columns)
        lines = self._text.split("\n")
        del lines[self._lines:]
        lines = [line[0:self._columns] for line in lines]
        fixed_text = "\n".join(lines)
        
        app = TkCircuit()
        app.update_lcds(self._pins, fixed_text)

    def set_backlight(self, backlight):
        pass

    def write8(self, value, char_mode=False):
        pass

    def create_char(self, location, pattern):
        pass

    def _delay_microseconds(self, microseconds):
        # Busy wait in loop because delays are generally very short (few microseconds).
        end = time.time() + (microseconds/1000000.0)
        while time.time() < end:
            pass

    def _pulse_enable(self):
        pass

    def _pwm_duty_cycle(self, intensity):
        pass