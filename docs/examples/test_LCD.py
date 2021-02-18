from tkgpio import TkCircuit

# initialize the circuit inside the GUI

configuration = {
    "width": 300,
    "height": 200,
    "lcds": [
        {"x": 30, "y": 40, "name": "LCD", "pins":[2, 3, 4, 5, 6, 7], "columns": 16, "lines": 2}
    ],
    "buttons": [
        {"x": 30, "y": 130, "name": "Press to toggle LED 2", "pin": 11},
    ]
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    
    # now just write the code you would use in a real Raspberry Pi
    
    from gpiozero import LED, Button
    from time import sleep
    from Adafruit_CharLCD import Adafruit_CharLCD
    
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
    global count
    count = 0
    
    
    def show_next_characters():
        global count
        
        print(f"Showing characters from code {count} to {count+31}")
        
        string = ""
        for i in range(0, 32):
            string += chr(count)
            if i == 15:
                string += "\n"
            count += 1
        
        lcd.clear()
        lcd.message(string)
    
    button = Button(11)
    button.when_pressed = show_next_characters
    
    show_next_characters()
    
    
    while True:
        sleep(0.1)
