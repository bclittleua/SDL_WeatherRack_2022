# -----------------------------------------------------------------------
# USES the SDL Weather Rack (henceforth 'SDWR') connected via i2c hat on
# an Arduino Uno, which is in turn connected to RPi via USB
# For details: https://www.switchdoc.com/weatherpiarduino-bare-board/
# DHT11 sensor is connected here to the RPi GPIO
# -----------------------------------------------------------------------
# This script only prints to terminal and keeps no logs, python2+
# -sam_r_i, April2022
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# This adafruit Lib is deprecated but works better than their new one:
# https://github.com/bclittleua/Adafruit_Python_DHT (forked for posterity)
import serial, time, datetime, Adafruit_DHT as dht, RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Read SERIALUSB from Arduino SDL_weatherrack
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)

# Read DHT from sensor connected to GPIO
sensor = dht.DHT11
pin = 24 #BCM pin number
humidity, temperature = dht.read_retry(sensor, pin)
temp = temperature #* 1.8 + 32 #uncomment at * to convert C to F
hum = humidity

# Count read cycles for terminal print, starts at zero
iteration = 0

# Give everything a few seconds to breathe
time.sleep(2)

# Loop it!
while True:
    date = datetime.date.today()       #
    tstamp = datetime.datetime.now()   # All this to format time
    time = tstamp.strftime("%H:%M:%S") #
    input = ser.readline() # read serial output over usb
    output = input.decode("UTF-8") # make serial readable for formatting
    iteration += 1 #iterate cycle
    
    # Generate an erorr if the SDWR output doesn't begin with 'rain',
    # to prevent garbled entries into an eventual log
    if output.startswith('rain'):
        print('Cycle{0}'.format(iteration))
        print("{0},{4},{1:0.1f}C,{2:0.1f}%,{3}".format(date, temp, hum, output, time))
        # FYI: output= rainfall, avg wind speed, wind burst speed, and wind direction
    else:
        print('Cycle{0}'.format(iteration))
        print("LINE ERROR\n")
# -----------------------------------------------------------------------
