from machine import UART, Pin, PWM
import time
# Initialize UART for communication (TX=GP0, RX=GP1)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
# Motor control pins
motorpin1 = PWM(Pin(26, Pin.OUT))
motorpin2 = PWM(Pin(27, Pin.OUT))
# Define motor control functions
def left():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(65535)
    motorpin2.duty_u16(0)
def right():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(65535)
def fwd():
    motorpin1.freq(65535)
    motorpin2.freq(65535)
    motorpin1.duty_u16(65535)
    motorpin2.duty_u16(0)
def back():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(65535)
def stop():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(0)
# Function to process received UART commands
def handle_command(command):
    command = command.strip()  # Remove newline or any extra spaces
    if command == "forward":
        fwd()
    elif command == "back":
        back()
    elif command == "left":
        left()
    elif command == "right":
        right()
    elif command == "stop":
        stop()
    else:
        print(f"Unknown command: {command}")
# Main loop to receive and process UART data
while True:
    if uart.any():
        # Read data from UART and handle it
        command = uart.readline().decode('utf-8')
        if command:
            print(f"Received command: {command}")
            handle_command(command)
    time.sleep(0.1)
