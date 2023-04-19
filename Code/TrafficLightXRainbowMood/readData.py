import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct
import math 
fig, axs = plt.subplots(3)

data = []
absdata = []
winfiltdata = []

sectionCount = 834
float_count = 21664
FS = 256 # =)

plt.ion()
plt.show()

counter = 0

WINDOWLENGTH = 50



with open("3ds.txt", "rb") as f:
    while (bytes := f.read(4)):
        if(bytes == b"DATA"):
            f.read(3)
            section_id = f.read(1)
            print("SECTION", int.from_bytes(section_id, "little"))
            f.read(8)
        else:
            counter +=1
            value = round(struct.unpack("f", bytes)[0])
            if(value > 1000 or value < -1000):
                continue
            data.append(value)
            absdata.append(abs(value))
            print(value)
            # for val in bytes:
            #     data.append(val)

            winfiltdata.append(sum(absdata[-WINDOWLENGTH:]) / WINDOWLENGTH)
            data = data[-1024:]
            absdata = absdata[-1024:]
            winfiltdata = winfiltdata[-1024:]
            if(counter >= 26):
                counter = 0
                axs[0].clear()
                axs[0].set_title("RAW SIGNAL")
                axs[0].plot(data)

                axs[1].clear()
                axs[1].set_title("ABS SIGNAL")
                axs[1].plot(absdata)


                # spec = np.abs(np.fft.rfft(data)) # получаем коэффициенты включения различных гармонических колебаний с частотами от 0hz до FS/2 с шагом 2FS/N
                # freq = np.arange(0,FS/2,FS/2/len(spec))

                axs[2].clear()
                axs[2].set_title("Filtred")
                axs[2].plot(winfiltdata)
                fig.canvas.draw()
                fig.canvas.flush_events()

        
plt.ioff()
plt.show()
