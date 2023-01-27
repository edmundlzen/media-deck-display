import pyfirmata
import time

port = '/dev/ttyACM0'
board = pyfirmata.ArduinoMega(port)
it = pyfirmata.util.Iterator(board)
it.start()
for i in range(2, 11):
    board.digital[i].mode = pyfirmata.INPUT
board.digital[22].mode = pyfirmata.INPUT
board.analog[0].enable_reporting()

while True:
    print("\033[2J")
    for i in range(2, 30):
        if board.analog[0].read() != 0:
            print("Analog 0 value:", board.analog[0].read())
        if board.digital[i].read() is True:
            # Clear lines for better readability
            print("Button", i-1, "pressed")
    time.sleep(0.1)