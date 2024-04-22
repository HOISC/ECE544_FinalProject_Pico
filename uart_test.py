from machine import UART, Pin, PWM
import time
import select
import sys

uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
led = Pin(25, Pin.OUT)
pwmSteer = PWM(Pin(16))
pwmSpeed = PWM(Pin(20))

pwmSteer.freq(100)
pwmSpeed.freq(100)


speed = 0
Angle = 0
buffer = ''
angleKey = ''
speedKey = ''
steerSpeedDoneFlag = 0
poll_object = select.poll()
poll_object.register(sys.stdin,1)
count = 0

#pwmSpeed.duty_u16(13107)
#time.sleep_ms(20)
pwmSpeed.duty_u16(6553)
time.sleep_ms(20)
pwmSpeed.duty_u16(13107)
time.sleep_ms(20)
pwmSpeed.duty_u16(9830)
time.sleep_ms(600)

while True:
    pwmSpeed.duty_u16(10354)
    #if uart1.any() > 0:
    if poll_object.poll(0):
        led.on()
        #print('H')
        #incoming_byte = uart1.read(1).decode()
        #print(incoming_byte)
        ch = sys.stdin.read(1)
        #print(ch)
        if steerSpeedDoneFlag == 2:
            #steeringPWM_Duty = ((13107 - 6553.5)/180)*angle + 6553.5
            if angle <= 30:
                steeringPWM_Duty = 6553.5
            elif angle >= 150:
                steeringPWM_Duty = 13107
            else:
                steeringPWM_Duty = ((13107 - 6553.5)/120)*angle + 4915.125           
            #steeringPWM_Duty = 6553
            pwmSteer.duty_u16(int(steeringPWM_Duty))
            #pwmSpeed.duty_u16(int(speed*(50/100)))
            print('Done')
        
        if ch == '$':
            steerSpeedDoneFlag = 0
            continue
        elif ch == ',':
            steerSpeedDoneFlag = 1
            angle = float(buffer)
            print(angleKey + ' ' + str(angle))
            buffer = ''
            continue
        elif ch == '@':
            steerSpeedDoneFlag = 2
            speed = float(buffer)
            print(speedKey + ' ' + str(speed))
            buffer = ''
            continue            
                
        if ((ch >= 'A') and (ch <= 'Z')):
            if steerSpeedDoneFlag == 0:
                angleKey = ch
                print('angleKey: ' + angleKey)
            elif steerSpeedDoneFlag == 1:
                speedKey = ch
                print('speedKey: ' + speedKey)
        elif ((ch == '.') or ((ch >= '0') and (ch <= '9'))):
            buffer = buffer + ch