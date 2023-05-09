import struct
import matplotlib.pyplot as plt

#Заводим массивы для хранения данных
int_le_unsig = []
int_be_unsig = []
int_le_sig = []
int_be_sig = []
floats = []

with open("3ds.txt", "rb") as ds:
    while True:
        data = ds.read(4) #Читаем 4 байта из фалйа
        if(data ==  b""): #Определяем конец файла
            break
        elif(data == b"DATA"):
            ds.read(12) #Убираем лишние данные
            continue
        
        value = float(struct.unpack("f", data)[0]) #Фильтруем выбросы
        if(value > 1000 or value < -1000):
                continue
        #Добавляем данные в массив
        floats.append(value)
        int_be_unsig.append(int.from_bytes(data, "big", signed=False))
        int_be_sig.append(int.from_bytes(data, "big", signed=True))
        int_le_sig.append(int.from_bytes(data, "little", signed=True))
        int_le_unsig.append(int.from_bytes(data, "little", signed=False))
        
    
fig, axs = plt.subplots(3,2) #Создаем графики
#Устанавливем соотношение сторон окна
fig.set_figheight(6)
fig.set_figwidth(15)

axs[0,0].plot(floats)
axs[0,0].set_title("FLOAT")
axs[0,1].plot(int_be_sig)
axs[0,1].set_title("int big endian signed")
axs[1,0].plot(int_be_unsig)
axs[1,0].set_title("int big endian unsigned")
axs[1,1].plot(int_le_sig)
axs[1,1].set_title("int little endian signed")
axs[2,0].plot(int_le_unsig)
axs[2,0].set_title("int little endian unsigned")

plt.show()    