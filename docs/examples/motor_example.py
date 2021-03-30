# Version: 1.0
# Date: 3.30.21
# Author: Greg

from tkgpio import TkCircuit

# initialize the circuit inside the GUI

configuration = {
    "width": 400,
    "height": 400,
    "leds": [
    ],
    "buttons": [
        {"x": 50, "y": 100, "name": "Forward", "pin": 11},
        {"x": 50, "y": 200, "name": "Stop", "pin": 12},
        {"x": 50, "y": 300, "name": "Backwards", "pin": 13},
    ],
    "motors": [
        {"x": 200, "y": 150, "name": "Motor 1", "pin": [16, 18]}
    ]
}

circuit = TkCircuit(configuration)

@circuit.run
def main():
    from gpiozero import Button, Motor
    from time import sleep

    Motor1 = Motor(16, 18)

    def button_pressed_forward():
        print("Moving forwards")
        Motor1.forward(1)

    def button_pressed_backward():
        print("Moving backwards")
        Motor1.backward(1)

    def button_pressed_stop():
        print("Stopped")
        Motor1.stop()

    button_forward = Button(11)
    button_stop = Button(12)
    button_backward = Button(13)

    button_forward.when_pressed = button_pressed_forward
    button_stop.when_pressed = button_pressed_stop
    button_backward.when_pressed = button_pressed_backward

    while True:
        sleep(0.1)
