from threading import Thread
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import serial.tools.list_ports_osx
import serial.tools.list_ports_windows
import struct
import numpy as np

class SerialReader:
    #Инициализатор класса
    def __init__(self) -> None:
        baudrate = 115200
        port = self.askport()
        self.Thread = None 
        self.data = [0,0,0]
        self.abs_data = [0,0,0]
        self.filt_data = [0,0,0]
        self.isRuining = True
        self.WINDOWLENGTH = 125 
        self.last_data = time.time()*1000
        print('Trying to connect to: ' + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(port, baudrate, timeout=0.02)            
            print('Connected to ' + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        except:
            print("Failed to connect with " + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        
    #Функция для запроса порта к которому необходимо подключится
    def askport(self) -> int:
        print("Available ports: ")
        devices = []
        i = 0
        for port in list(serial.tools.list_ports_windows.comports()):
            devices.append(port.device)
            print(str(i)+": ", port)
            i+=1
        return devices[int(input("Write device number: "))]
    
    #Начало передачи данных и создание потока
    def startThread(self):
        self.serialConnection.write(b"stop\n")
        time.sleep(0.1)
        self.serialConnection.write(b"start\n")
        if(self.Thread == None):
            self.Thread = Thread(target=self.GetData)
            self.Thread.start()
            
    def GetData(self):
        while(self.isRuining):
            if(self.serialConnection.in_waiting >= 16):
                readed = self.serialConnection.read(4)
                if(readed == b"DATA"): #Пропускаем часть не показательных данных
                    self.serialConnection.read(12)
                else:
                    unpacked = struct.unpack("f", readed)[0] #Переводим в float

                    if(np.isnan(unpacked)):
                        continue #Проверяем на число
                    
                    if(unpacked > 3000 or unpacked < -3000): 
                        continue #Фильтруем выбросы

                    current_point = float(unpacked) 
                    self.data.append(current_point)
                    self.abs_data.append(abs(current_point))
                    #Применяем фильтр с плаваюшим окном
                    self.filt_data.append(sum(self.abs_data[-self.WINDOWLENGTH:]) / self.WINDOWLENGTH)
                    #Обрезаем данные до необходимого окна во избежании утечек памяти
                    self.data = self.data[-1024:]
                    self.abs_data = self.abs_data[-1024:]
                    self.filt_data = self.filt_data[-1024:]

                    self.last_data = time.time()*1000
    #Закрытие порта, потока, остановка передачи данных
    def close(self):
        self.isRuining = False
        self.Thread.join()
        self.serialConnection.write(b"stop\n")
        self.serialConnection.close()
        print('Disconnected...')
    #Функция для очистки данных    
    def clear(self):
        self.data = []
        self.abs_data = []
        self.filt_data = []


def getPorogs(reader):
    def getPorog(text1, text2, text3):
        print("Переходим к настройке "+text1+" порога!")
        print("В течении следующих 5 секунд "+text2+" руку.")
        print("Напишите что-ниубдь когда будете готовы")
        input()
        vals = []
        for i in range(5):
            reader.clear()
            time.sleep(1)
            print(i)
            vals.append( (max(reader.filt_data)+min(reader.filt_data)) / 2)
        value = sum(vals) / len(vals)
        print("Готово!")
        print(value, " - "+text3+" значение")
        return value
    
    ans = input("Провести повторную калибровку пороговых значений или загрузить значения из файла?\n1 - Загрузить\n2 - Провести повторно\nОтвет:")
    if(ans == "2"):
        maximum = getPorog("максимального", "максимально напрягите", "Максимальное")
        minimum = getPorog("минимального", "максимально расслабьте", "Минимальное")
        open("porogs.txt", "w").write(str(maximum)+";"+str(minimum))
    else:
        maximum, minimum = list(map(float, open("porogs.txt", "r").readline().split(";")))


    porog1 = minimum + ((maximum-minimum) / 3)
    porog2 = minimum + (((maximum-minimum) / 3)*2)

    return (maximum, minimum, porog1, porog2)