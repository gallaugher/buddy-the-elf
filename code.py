# Buddy the Elf - jack-in-the-box build
# Uses an Adafruit Circuit Playground Bluefruit:
# https://www.adafruit.com/product/4333
# Complete parts list in the build video at:
# https://youtu.be/AHcwQRxTjOY
# By Prof. John Gallaugher
# Like this? Have corrections / suggestions / improvements?
# Let me know! @gallaugher  and  gallaugher.com
#
# Updated for current CircuitPython (9.x / 10.x):
#   - pulseio.PWMOut moved to pwmio.PWMOut back in CircuitPython 7.0
#   - dropped imports the program never used (busio, analogio, simpleio, ColorPacket)
#   - sound files are opened with "with" so each one is closed after it plays
#   - the Bluetooth loop only reads a packet when the app has actually sent one,
#     so the touchpads stay responsive while the phone is connected

import board
import time
import digitalio
import touchio
import pwmio
import random
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile
from adafruit_motor import servo

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# setup bluetooth
ble = BLERadio()
# setup bluetooth
ble = BLERadio()
ble.name = "Buddy the Elf"
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

# enable the speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

# set up touchpads
# A1 is used by wave_servo and TX by lid_servo, so they are not touchpads
pads = [board.A2, board.A3, board.A4, board.A5, board.A6]

# create an empty list named touchpad
touchpad = []

# loop through all elements of pads and create the touchpad list
for i in range(len(pads)):
    touchpad.append(touchio.TouchIn(pads[i]))

# create a PWMOut object on Pin A1.
pwm = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
# Create a servo object, wave_servo.
wave_servo = servo.Servo(pwm)

# create a PWMOut object on Pin TX.
pwm_lid = pwmio.PWMOut(board.TX, duty_cycle=2 ** 15, frequency=50)
# Create a servo object, lid_servo.
# Tested range in REPL & this seemed to work.
lid_servo = servo.Servo(pwm_lid, min_pulse=500, max_pulse=2250)
lid_servo.angle = 115

startAngle = 0
endAngle = 135
wave_servo.angle = startAngle

# define the list of Buddy sound clips
buddySounds = ["my-names-buddy.wav", "christmas-cheer-sing-loud.wav",
    "santas-coming-so-much-to-do.wav", "its-great-to-meet-you.wav",
    "i-just-like-to-smile.wav", "you-sit-on-a-throne-of-lies.wav",
    "you-did-it.wav", "whats-a-christmas-gram.wav", "i-love-you.wav",
    "santa-i-know-him.wav", "santa-must-have-called-you.wav"]

path = "/sounds/"


def moveUp():
    for angle in range(startAngle, 50, 3):  # raise the arm, 3 degrees at a time
        wave_servo.angle = angle
        time.sleep(0.02)

def moveBack():
    for angle in range(49, startAngle, -3):  # lower the arm back to rest
        wave_servo.angle = angle
        time.sleep(0.02)


def move():
    for angle in range(50, endAngle, 3):  # wave out...
        wave_servo.angle = angle
        time.sleep(0.02)
    for angle in range(endAngle, 49, -3):  # ...and back
        wave_servo.angle = angle
        time.sleep(0.02)


def openLid():
    for i in range(116):
        lid_servo.angle = i
        if i > 0:
            time.sleep(0.05)


def playfile(filename):
    # "with open" closes the file when the clip is done
    with open(path + filename, "rb") as wave_file:
        with WaveFile(wave_file) as wave:
            with AudioOut(board.SPEAKER) as audio:
                audio.play(wave)
                moveUp()
                while audio.playing:
                    move()
                moveBack()


def checkTouch():
    for i in range(len(touchpad)):
        if touchpad[i].value:
            print("Touchpad", i, "was touched!")
            if i == 4:
                openLid()
                print("touchpad ", i)
            elif i == 3:
                soundToPlay = random.randint(3, len(buddySounds) - 1)
                print("touchpad ", i, "sound", soundToPlay)
                playfile(buddySounds[soundToPlay])
            else:  # should be 0, 1, or 2
                print("touchpad ", i, "sound", i)
                playfile(buddySounds[i])


while True:
    # set the CPB up so that it can be discovered by the Bluefruit Connect app
    ble.start_advertising(advertisement)
    while not ble.connected:
        checkTouch()
    ble.stop_advertising()

    # Now we're connected
    while ble.connected:
        checkTouch()

        # Only try to read a packet if the app actually sent something.
        # Without this check, from_stream() waits for data on every pass
        # through the loop and the touchpads feel sluggish.
        if uart_server.in_waiting:
            try:
                packet = Packet.from_stream(uart_server)
            except ValueError:
                continue  # bad packet - go around and try again

            if isinstance(packet, ButtonPacket) and packet.pressed:
                if packet.button == ButtonPacket.BUTTON_1:
                    playfile(buddySounds[0])
                elif packet.button == ButtonPacket.BUTTON_2:
                    print("*** 1")
                    playfile(buddySounds[1])
                elif packet.button == ButtonPacket.BUTTON_3:
                    print("*** 2")
                    playfile(buddySounds[2])
                elif packet.button == ButtonPacket.BUTTON_4:
                    print("*** 3")
                    soundToPlay = random.randint(0, len(buddySounds) - 1)
                    playfile(buddySounds[soundToPlay])
                elif packet.button == ButtonPacket.UP:
                    openLid()
                elif packet.button == ButtonPacket.DOWN:
                    playfile(buddySounds[5])
                elif packet.button == ButtonPacket.LEFT:
                    playfile(buddySounds[4])
                elif packet.button == ButtonPacket.RIGHT:
                    # make the touchpads a little less sensitive
                    for i in range(len(touchpad)):
                        print("Before Change: pad", i, "threshold =", touchpad[i].threshold)
                        touchpad[i].threshold = touchpad[i].threshold + 50
                        print("After Change: pad", i, "threshold =", touchpad[i].threshold)
