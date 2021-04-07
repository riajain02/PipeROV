'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
https://www.electronicwings.com/raspberry-pi/gps-module-interfacing-with-raspberry-pi

10/18/2020 -
  -- used GNGGA instead of GPGGA (was not available)
  -- changed the precision to eight decimal places
  -- commented out the webbrowser part

'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

def GPS_Info(NMEA_buff):
    #global NMEA_buff
    #global lat_in_degrees
    #global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GNGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GNGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GNGGA string
    
    #print("NMEA Time: ", nmea_time,'\n')
    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    try:
     lat = float(nmea_latitude)                  #convert string into float for calculation
     lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    except:
     lat_in_degrees = -1
    try:
     longi = float(nmea_longitude)               #convert string into float for calculation
     longi *= -1                                 #convert west to east - perhaps because we are using GNGGA instead as GPGGA
     long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    except:
     long_in_degrees = -1
    
    return lat_in_degrees, long_in_degrees
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.8f" %(position)
    return position
    


gngga_info = "$GNGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GNGGA_buffer = 0
#NMEA_buff = 0
#lat_in_degrees = 0
#long_in_degrees = 0

def mygps_get_coordinates():
    while True:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GNGGA_data_available = received_data.find(gngga_info)   #check for NMEA GNGGA string                 
        if (GNGGA_data_available>-1):
            GNGGA_buffer = received_data.split("$GNGGA,",1)[1]  #store data coming after "$GNGGA," string 
            NMEA_buff = (GNGGA_buffer.split(','))               #store comma separated data in buffer
            return GPS_Info(NMEA_buff)                          #get time, latitude, longitude
