from m5stack import lcd, speaker
from machine import I2C
import time

i2c = I2C(freq=400000, sda=21, scl=22)
while True:
    temp_byte = i2c.readfrom(72, 2)             # アドレス72番から2byte読み込み
    temp = int.from_bytes(temp_byte,"big")/128  # 温度換算
    print(temp)
    if temp > 30: 
        lcd.clear(lcd.RED)
        lcd.setColor(lcd.WHITE, lcd.RED)
        lcd.text(lcd.CENTER,lcd.CENTER, str(temp))
        speaker.volume(1)
        speaker.tone(freq=1000, duration=200)   # 30℃以上で
    else:
        lcd.clear(lcd.BLUE)
        lcd.setColor(lcd.WHITE, lcd.BLUE)
        lcd.text(lcd.CENTER,lcd.CENTER, str(temp))
    time.sleep(5)

