import time, smbus
import wiringpi as pi

def read_temp():
    # i2cのチャンネルと、adtのアドレスを決める
    i2c_channel = 1
    adt7410_addr = 0x48

    i2c = smbus. SMBus( i2c_channel )
    # データの読み取り
    data = i2c.read_i2c_block_data(adt7410_addr, 0x00,2)
    # データの整形(Arduinoのときと同じ温度換算)
    temp = ((data[0]<<8|data[1] ) >> 3)/16.0
    return temp



if __name__ == '__main__':
    # GPIO13(PWMができるピン)を指定
    led_pin = 13
    pi.wiringPiSetupGpio()
    # PWMができるように初期設定
    pi.pinMode(led_pin,pi.GPIO.PWM_OUTPUT)
    pi.pwmSetMode(pi.GPIO.PWM_MODE_MS)
    pi.pwmSetClock(500)
    # 明るさ初期値0とする
    pi.pwmWrite(led_pin, 0)
    
    temp = read_temp()

    while True:
        print(temp)
        # 温度読み取り
        temp = read_temp()
        # 読み取った温度を
        pi.pwmWrite(led_pin, int(temp))
        time.sleep(1)

