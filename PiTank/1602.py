#!/usr/bin/python
 
from lcd1602 import *
from datetime import *
import commands
 
def get_cpu_temp():
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_gpu_temp():
    tmp = commands.getoutput('vcgencmd measure_temp|awk -F= \'{print $2}\'').replace('\'C','')
    gpu = float(tmp)
    return '{:.2f}'.format( gpu ) + ' C'
 
def get_time_now():
    return datetime.now().strftime('    %H:%M:%S\n   %Y-%m-%d')
 
def get_ip_info():
    return commands.getoutput('ifconfig wlan0|grep inet|awk -Faddr: \'{print $2}\'|awk \'{print $1}\'')
 
def get_mem_info():
    total= commands.getoutput('free -m|grep Mem:|awk \'{print $2}\'')  
    free = commands.getoutput('free -m|grep cache:|awk \'{print $4}\'')
    return 'MEM:\n    ' + free +' / '+ total +' M'
 
lcd = lcd1602()
lcd.clear()
 
if __name__ == '__main__':
 
    while(1):
        lcd.clear()
        lcd.message( get_ip_info() )
        sleep(5)
 
        lcd.clear()
        lcd.message( get_time_now() )
        sleep(5)
 
        lcd.clear()
        lcd.message( get_mem_info() )
        sleep(5)
 
        lcd.clear()
        lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )
        lcd.message( 'GPU: ' + get_gpu_temp() )
        sleep(5)
