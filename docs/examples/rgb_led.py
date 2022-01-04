from tkgpio import TkCircuit

configuration = {
    "width": 300,
    "height": 250,
    "rgb_leds": [
        {"x": 50, "y": 40, "name": "LED 1", "red_pin": 21, "green_pin": 22, "blue_pin": 23},
        {"x": 100, "y": 40, "name": "LED 2", "red_pin": 16, "green_pin": 17, "blue_pin": 18}
    ],
    "adc": {
      "mcp_chip": 3008,
      "potenciometers": [
        {"x": 50,  "y": 120, "name": "Red", "channel": 0},
        {"x": 50, "y": 160, "name": "Green", "channel": 1},
        {"x": 50, "y": 200, "name": "Blue", "channel": 2}
      ]  
    },
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    
    from gpiozero import RGBLED, MCP3008
    from time import sleep
    
    led1 = RGBLED(21, 22, 23)
    led1.blink()
    
    led2 = RGBLED(16, 17, 18)
    
    potenciometer1 = MCP3008(0)
    potenciometer2 = MCP3008(1)
    potenciometer3 = MCP3008(2)
    
    while True:
        led2.red = potenciometer1.value
        led2.green = potenciometer2.value
        led2.blue = potenciometer3.value
        sleep(0.1)
