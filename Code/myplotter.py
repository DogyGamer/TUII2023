from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import serial.tools.list_ports_osx
import serial.tools.list_ports_windows
import struct
import numpy as np

import requests

def toggle_light():
    endpoint = "https://dogyhome.duckdns.org:8123/"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0MTVjNDMzNjA1YzE0ZDdiYTM0NGI0YTQwMGViYTEwNSIsImlhdCI6MTY4MDM0MzIzMywiZXhwIjoxOTk1NzAzMjMzfQ.RNsTOrm7Jb-42p2W42EYVGuxqQ4ENCp6NUGHsS24cZE",
            "content-type": "application/json",
            }
    data = {"area_id": "spalnia_sasha"}
    requests.post(endpoint+"api/services/light/toggle", headers=headers, json=data)

fig = plt.figure(figsize=(16,9))
ax1 = plt.subplot2grid((12,12), (0,0), 3, 8)
ax2 = plt.subplot2grid((12,12), (4,0), 3, 8)
ax3 = plt.subplot2grid((12,12), (8,0), 4, 8)
ax4 = plt.subplot2grid((12,12), (0,8), 12, 8)
# fig, axs = plt.subplots(3,2, figsize=(16,9))



FS = 256
WINDOW_LENGTH = 100

class SerialReader:
    def __init__(self) -> None:
        baudrate = 115200
        port = self.askport()
        self.Thread = None 
        self.data = [0,0,0]
        self.abs_data = [0,0,0]
        self.filt_data = [0,0,0]


        self.min = np.full(1024, 0)
        self.max = np.full(1024, 0)
        self.porog1 = np.full(1024, 0)
        self.porog2 = np.full(1024, 0)
        
        self.isRuining = True

        self.flag = False

        print('Trying to connect to: ' + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        try:
            # self.serialConnection.open()
            self.serialConnection = serial.Serial(port, baudrate, timeout=0.02)
            # self.serialConnection.write(b"start\n")
            
            print('Connected to ' + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        except:
            print("Failed to connect with " + str(port) + ' at ' + str(baudrate) + ' BAUD.')
        
    def askport(self) -> int:
        print("Available ports: ")
        devices = []
        i = 0
        for port in list(serial.tools.list_ports_windows.comports()):
            devices.append(port.device)
            print(str(i)+": ", port)
            i+=1
        return devices[int(input("Write device number: "))]
    
    
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
                if(readed == b"DATA"):
                    self.serialConnection.read(12)
                else:
                    unpacked = struct.unpack("f", readed)[0]

                    if(np.isnan(unpacked)):
                        continue
                    
                    if(unpacked > 3000 or unpacked < -3000):
                        continue

                    current_point = float(unpacked)

                    self.data.append(current_point)
                    self.abs_data.append(abs(current_point))
                    self.filt_data.append(sum(self.abs_data[-WINDOW_LENGTH:]) / WINDOW_LENGTH)
                    self.data = self.data[-1024:]
                    self.abs_data = self.abs_data[-1024:]
                    self.filt_data = self.filt_data[-1024:]

                    # if(self.filt_data[-1] > self.porog2[0] and self.flag == False):
                    #     toggle_light()
                    #     self.flag == True
                    # elif(self.filt_data[-1] < self.porog1[0] and self.flag):
                    #     self.flag = False

    def close(self):
        self.isRuining = False
        self.Thread.join()
        self.serialConnection.write(b"stop\n")
        self.serialConnection.close()
        print('Disconnected...')
    
    def clear(self):
        self.data = []
        self.abs_data = []
        self.filt_data = []

    def anim(self, _):
        # print("ANI")
        
        ax1.clear()
        ax1.set_title("Сырые данные")
        ax1.plot(self.data)

        ax2.clear()
        ax2.set_title("Abs от сигнала")
        ax2.plot(self.abs_data)

        ax3.clear()
        ax3.set_title("Отфильтрованый сигнал")
        ax3.plot(self.filt_data)
        ax3.plot(self.min, color="g")
        ax3.plot(self.porog1, color="yellow")
        ax3.plot(self.porog2, color="r")
        ax3.plot(self.max, color="r")

        color = "black"
        if(self.filt_data[-1] < self.porog1[0]):
            color = "green"
        elif(self.filt_data[-1] < self.porog2[0] and self.filt_data[-1] > self.porog1[0]):
            color = "yellow"
        elif(self.filt_data[-1] > self.porog2[0]):
            color = "red"


        ax4.clear()
        ax4.plot(self.min[:2], color="g")
        ax4.plot(self.porog1[:2], color="yellow")
        ax4.plot(self.porog2[:2], color="r")
        ax4.plot(self.max[:2], color="r")

        ax4.bar(["Значение: "+ str(self.filt_data[-1])], [self.filt_data[-1]], width = 0.4, color=color )
        if(self.max[0] > self.filt_data[-1]):
            ax4.set_ylim([0,self.max[0]])
        else:
            ax4.set_ylim([0,self.filt_data[-1]])

    

reader = SerialReader()
reader.startThread()

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

reader.max =  np.full(1024,maximum)
reader.min = np.full(1024,minimum)

reader.porog1 = np.full(1024,minimum + ((maximum-minimum) / 3))
reader.porog2 = np.full(1024,minimum + (((maximum-minimum) / 3)*2))

fig.canvas.mpl_connect('close_event', reader.close)
ani = animation.FuncAnimation(fig, reader.anim, fargs=None, interval=50)

plt.show()

reader.close()