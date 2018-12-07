import time, smbus

def read_temp():
    i2c_channel = 1
    adt7410_addr = 0x48
    i2c = smbus. SMBus( i2c_channel )
    # データの読み取り
    data = i2c.read_i2c_block_data(adt7410_addr, 0x00, 2)
     # データの整形(Arduinoのときと同じ温度換算)
    temp = ((data[0]<<8|data[1] ) >> 3)//16.0
    return temp

if __name__ == '__main__':
    temp = read_temp()
    while True:
        print(temp)
        temp = read_temp()
        time.sleep(1)
