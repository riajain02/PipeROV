import RPi.GPIO as GPIO

class Motor:
    def __init__(self, channel, frequency):
        self.channel = channel
        self.frequency = frequency
        GPIO.setmode(GPIO.BOARD)
        update_gpio(self.channel, self.frequency)
    
    def get_channel(self):
        return self.channel

    def get_frequency(self):
        return self.frequency
    
    def update_gpio(self, channel, frequency):
        GPIO.setup(channel, GPIO.OUT)   
        self.gpio = GPIO.PWM(self.channel, self.frequency)

    def set_channel(self, channel):
        self.channel = channel
        update_gpio(self.channel, self.frequency)
    
    def set_frequency(self, frequency):
        self.frequency = frequency
        update_gpio(self.channel, self.frequency)
    
    def change_speed(self, speed):
        self.gpio.ChangeDutyCycle(speed)
        
        
        