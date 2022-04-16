# -----------------------------------------------------------------------
# USES the SDL Weather Rack (henceforth 'SDWR') connected via i2c hat on
# an Arduino Uno, which is in turn connected to RPi via USB
# For details: https://www.switchdoc.com/weatherpiarduino-bare-board/
# DHT11 sensor is connected here to the RPi GPIO
# -----------------------------------------------------------------------
# This script prints to terminal and writes to a log, python2+. Also creates
# an error log and tracks the error rate, which is amazingly low for how fast
# it writes (usually only loses ~4 out of the first 10-15 records).
# -sam_r_i, April2022
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# This adafruit Lib is deprecated but works better (for me) than their new one:
# https://github.com/bclittleua/Adafruit_Python_DHT (forked for posterity)
import serial, time, datetime, Adafruit_DHT as dht, RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Read SERIALUSB from Arduino SDL_weatherrack
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)

# Read DHT from sensor connected to GPIO
sensor = dht.DHT11 # DHT22 Compatable
pin = 24 #BCM pin number
humidity, temperature = dht.read_retry(sensor, pin)
temp = temperature #* 1.8 + 32 # uncomment at * to convert C to F
hum = humidity

# Count read cycles for terminal print, starts at zero
iteration = 0
errRate = 0

# Give everything a second to breathe
time.sleep(1)

# then loop it!
while True:
    date = datetime.date.today()       # \
    tstamp = datetime.datetime.now()   #  > All this to format the time
    hour = tstamp.strftime("%H:%M:%S") # /
    input = ser.readline() # read serial output from usb
    output = input.decode("UTF-8", "ignore") # make serial readable for formatting, ignore errors
    iteration += 1 # iterate cycle

    # makin the lawg, makin the lawg!
    logger = open('/home/pi/Desktop/sdwr.log', 'a+') # log file
    errors = open('/home/pi/Desktop/sdwr.error', 'a+') # error logs

    # Generate an erorr if the SDWR output doesn't begin with 'rain',
    # this prevents a cascade of garbled entries in the log file.
    if output.startswith('rain'):
        print("Cycle {5},{0},{4},{1:0.1f},{2:0.1f},{3}\n".format(date, temp, hum, output, hour, iteration))
        logger.write("Cycle {5},{0},{4},{1:0.1f},{2:0.1f},{3}".format(date, temp, hum, output, hour, iteration))
        # FYI: output= rainfall, avg wind speed, wind burst speed, and wind direction
    else:
        # spits out all errors into a separate log for review
        errRate += 1
        print("SDWR.log LINE ERROR on cycle {0}. Errors this session: {1} \n".format(iteration, errRate))
        errors.write("SDWR.log EXCEPTION at {1} Cycle {2} on {0}. Errors this session: {3} \n".format(date, hour, iteration, errRate))
    logger.close()
# -----------------------------------------------------------------------
