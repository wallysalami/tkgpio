from tkgpio import TkCircuit
from json import load

# initialize the circuit inside the GUI
with open("circuit_configuration.json", "r") as file:
    configuration = load(file)
    
circuit = TkCircuit(configuration)
@circuit.run
def main():
    
    # now just write the code you would use in a real Raspberry Pi
    
    from Adafruit_CharLCD import Adafruit_CharLCD
    from gpiozero import Buzzer, LED, PWMLED, Button, DistanceSensor, LightSensor, MotionSensor
    from lirc import init, nextcode
    from py_irsend.irsend import send_once
    from time import sleep
    
    def show_sensor_values():
        lcd.clear()
        lcd.message(
            "Distance: %.2fm\nLight: %d%%" % (distance_sensor.distance, light_sensor.value * 100)
        )
        
    def send_infrared():
        send_once("TV", ["KEY_4", "KEY_2", "KEY_OK"])
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    buzzer = Buzzer(16)
    led1 = LED(21)
    led2 = LED(22)
    led3 = LED(23)
    led4 = LED(24)
    led5 = PWMLED(25)
    led5.pulse()
    button1 = Button(11)
    button2 = Button(12)
    button3 = Button(13)
    button4 = Button(14)
    button1.when_pressed = led1.toggle
    button2.when_pressed = buzzer.on
    button2.when_released = buzzer.off
    button3.when_pressed = show_sensor_values
    button4.when_pressed = send_infrared
    distance_sensor = DistanceSensor(trigger=17, echo=18)
    light_sensor = LightSensor(8)
    motion_sensor = MotionSensor(27)
    motion_sensor.when_motion = led2.on
    motion_sensor.when_no_motion = led2.off
    
    init("default")
    
    while True:
        code = nextcode()
        if code != []:
            key = code[0]
            lcd.clear()
            lcd.message(key + "\nwas pressed!")
            
        sleep(0.2)
