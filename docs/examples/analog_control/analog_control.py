# This example keeps the setup code in a different file.
# It is useful if you want to hide that complexity from students.

from setup import run

@run
def main():
    
    from gpiozero import PWMLED, Motor, Servo, MCP3008, Button
    from time import sleep


    led = PWMLED(21)
    motor = Motor(22, 23)
    servo = Servo(24)

    potenciometer1 = MCP3008(0)
    potenciometer2 = MCP3008(2)
    potenciometer3 = MCP3008(6)
    switch = Button(15)


    while True:
        led.value = potenciometer1.value

        if switch.is_pressed:
            motor.forward(potenciometer2.value)
        else:
            motor.backward(potenciometer2.value)
          
        servo.value = 1 - 2 * potenciometer3.value


        sleep(0.05)
