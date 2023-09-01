from tkgpio import TkCircuit

configuration = {
    "name": "Analog Control",
    "width": 700,
    "height": 350,
    
    "leds": [
        {"x": 105, "y": 80, "name": "LED", "pin": 21}
    ],
    "motors": [
        {"x": 316, "y": 80, "name": "DC Motor", "forward_pin": 22, "backward_pin": 23}
    ],
    "servos": [
        {"x": 537, "y": 80, "name": "Servomotor", "pin": 24, "min_angle": -90, "max_angle": 90, "initial_angle": 20}
    ],
    
    "adc": {
      "mcp_chip": 3008,
      "potentiometers": [
        {"x": 40,  "y": 200, "name": "Brightness Potentiometer", "channel": 0},
        {"x": 270, "y": 200, "name": "Speed Potentiometer",      "channel": 2},
        {"x": 500, "y": 200, "name": "Angle Potentiometer",      "channel": 6}
      ]  
    },
    "toggles": [
        {"x": 270, "y": 270, "name": "Direction Toggle Switch", "pin": 15, "off_label": "backward", "on_label": "forward", "is_on": False}
    ],
    
    # Labels have the same properties as the ones in TkInter.
    # That means you can use them to write formatted text or draw rectangles below the circuit.
    "labels": [
        {"x": 15,  "y": 35, "width": 25, "height": 18, "borderwidth": 2, "relief": "solid"},
        {"x": 56,  "y": 26, "text": "Brightness Control"},
        
        {"x": 245, "y": 35, "width": 25, "height": 18, "borderwidth": 2, "relief": "solid"},
        {"x": 298, "y": 26, "text": "Speed Control"},
        
        {"x": 475, "y": 35, "width": 25, "height": 18, "borderwidth": 2, "relief": "solid"},
        {"x": 531, "y": 26, "text": "Angle Control"}
    ]
}

def run (main_function):
    circuit = TkCircuit(configuration)
    circuit.run(main_function)
    