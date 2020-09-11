from tkgpio import TkCircuit

# initialize the circuit inside the GUI

configuration = {
    "width": 300,
    "height": 200,
    "leds": [
        {"x": 50, "y": 40, "name": "LED 1", "pin": 21},
        {"x": 100, "y": 40, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "Press to toggle LED 2", "pin": 11},
    ]
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    
    # now just write the code you would use in a real Raspberry Pi
    
    from gpiozero import LED, Button
    from time import sleep
    
    
    led1 = LED(21)
    led1.blink()
    
    
    def button_pressed():
        print("button pressed!")
        led2.toggle()
    
    led2 = LED(22)
    button = Button(11)
    button.when_pressed = button_pressed
    
    
    while True:
        sleep(0.1)
