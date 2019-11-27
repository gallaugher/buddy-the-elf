import board
import neopixel
import time
import digitalio
import touchio
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile
import busio
import analogio
import simpleio
import pulseio
from adafruit_motor import servo
import random

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# setup bluetooth
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

# enable the speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

# sets up 10 lights on the CPXb board and names them pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.3, auto_write=True)

# name colors so you don't need to refer to numbers
RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 165, 0)
LIGHT_GREEN = (165, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
INDIGO = (50, 0, 255)
VIOLET = (75, 0, 130)
PINK = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# an array of colors
colors = [RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN, CYAN, BLUE, INDIGO, VIOLET, PINK]

pixels.fill(BLACK)

# define buttons A + B
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)

button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# set up touchpads
# removed board.TX for lid_servo
pads = [board.A2, board.A3, board.A4, board.A5, board.A6]

# create an empty list named touchpad
touchpad = []

# loop through all elements of pads and create the touchpad list
for i in range(len(pads)):
    touchpad.append(touchio.TouchIn(pads[i]))

armed = False

# create a PWMOut object on Pin A1.
pwm = pulseio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
# Create a servo object, wave_servo.
wave_servo = servo.Servo(pwm)

# create a PWMOut object on Pin TX.
pwm_lid = pulseio.PWMOut(board.TX, duty_cycle=2 ** 15, frequency=50)
# Create a servo object, lid_servo.
# Tested range in REPL & this seemed to work.
lid_servo = servo.Servo(pwm_lid, min_pulse  = 500, max_pulse = 2250)
lid_servo.angle = 115

# define the drumsamples list
buddySounds = ["my-names-buddy.wav", "christmas-cheer-sing-loud.wav", 
    "santas-coming-so-much-to-do.wav", "its-great-to-meet-you.wav", 
    "i-just-like-to-smile.wav", "you-sit-on-a-throne-of-lies.wav", 
    "you-did-it.wav", "whats-a-christmas-gram.wav", "i-love-you.wav", "santa-i-know-him.wav", 
    "santa-must-have-called-you.wav"]

startAngle = 0
endAngle = 135
wave_servo.angle = startAngle

def playfile(filename):
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            moveUp()
            while audio.playing:
                move()
            moveBack()

def moveUp():
    # print("*** MOVE UP! ***")
    for angle in range(startAngle, 50, 3):  # 0 - 180 degrees, 5 degrees at a time.
        wave_servo.angle = angle
        # print(angle)
        time.sleep(0.02)

def moveBack():
    # print("*** MOVE BACK! ***")
    for angle in range(49, startAngle, -3):  # 0 - 180 degrees, 5 degrees at a time.
        wave_servo.angle = angle
        # print(angle)
        time.sleep(0.02)

def move():
    # for i in range(2):
    for angle in range(50, endAngle, 3):  # 0 - 180 degrees, 5 degrees at a time.
        wave_servo.angle = angle
        # print(angle)
        time.sleep(0.02)
    for angle in range(endAngle, 49, -3): # 180 - 0 degrees, 5 degrees at a time.
        wave_servo.angle = angle
        # print(angle)
        time.sleep(0.02)
    # print("*** DONE ***")
    # wave_servo.angle = startAngle
    print(startAngle)

def checkTouch():
    for i in range(len(touchpad)):
        if touchpad[i].value:
            print("Touchpad", i ,"was touched!")
            if i == 4:
                openLid()
                print("touchpad ", i)
            elif i == 3:
                soundToPlay = random.randint(3, len(buddySounds) - 1)
                print("touchpad ", i, "sound", soundToPlay)
                playfile(buddySounds[soundToPlay])
            else: # should be 0, 1, or 2
                print("touchpad ", i, "sound", i)
                playfile(buddySounds[i])
                # if i == 4:
                    # playfile(buddySounds[2])
                

def openLid():
    for i in range(116):
        lid_servo.angle = i
        print(i)
        if i > 10:
            time.sleep(0.05)


while True:
    # set CPXb up so that it can be discovered by the app
    ble.start_advertising(advertisement)
    while not ble.connected:
        checkTouch()
    ble.stop_advertising()

    # Now we're connected

    while ble.connected:
        checkTouch()
        try:
            packet = Packet.from_stream(uart_server)
        except ValueError:
            continue # or pass. This will start the next iteration of the loop and try to get a valid packet again.

        if isinstance(packet, ButtonPacket):
            if packet.pressed:
                if packet.button == ButtonPacket.BUTTON_1:
                    playfile(buddySounds[0])
                if packet.button == ButtonPacket.BUTTON_2:
                    print("*** 1")
                    playfile(buddySounds[1])
                if packet.button == ButtonPacket.BUTTON_3:
                    print("*** 2")
                    playfile(buddySounds[2])
                if packet.button == ButtonPacket.BUTTON_4:
                    print("*** 3")
                    soundToPlay = random.randint(0, len(buddySounds) - 1)
                    playfile(buddySounds[soundToPlay])
                if packet.button == ButtonPacket.UP:
                    openLid()
                if packet.button == ButtonPacket.DOWN:
                    playfile(buddySounds[5])
                if packet.button == ButtonPacket.LEFT:
                    playfile(buddySounds[4])
                if packet.button == ButtonPacket.RIGHT:
                    for i in range(len(touchpad)):
                        print("Before Change: pad", i, "threshold = ", touchpad[i].threshold)
                        touchpad[i].threshold = touchpad[i].threshold + 50
                    for i in range(len(touchpad)):
                        print("After Change: pad", i, "threshold = ", touchpad[i].threshold)
                        touchpad[i].threshold = touchpad[i].threshold + 50
