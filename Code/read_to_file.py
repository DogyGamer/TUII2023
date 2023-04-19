import serial.tools.list_ports_osx
import serial

out_file = open("data.txt", "wb")

print("Available ports: ") #Выводим список доступных портов
devices = []
i = 0
for port in list(serial.tools.list_ports_osx.comports()):
    devices.append(port.device)
    print(str(i)+": ", port)
    i+=1


dev_id = int(input("Write device number: ")) #Спрашиваем номер порта в списке

ser = serial.Serial()
ser.port = devices[dev_id]
ser.baudrate = 115200
ser.open() #Открываем последовательный порт

ser.write(b"start\n") #Начинаем передачу данных

for i in range(10000): #Переберем 10000 байт
    byte = ser.read(1) #Читаем один байт данных из порта
    out_file.write(byte)

ser.write(b"stop\n") #Останавливем передачу
ser.close() #Закрываем порт
out_file.close() #Закрываем файл