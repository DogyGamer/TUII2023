import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import struct
import serial.tools.list_ports_osx
import serial
import time

samplerate = 1024

fig, axs= plt.subplots(4)
def current_second_time():
    return round(time.process_time_ns())

print("Available ports: ")
devices = []
i = 0
for port in list(serial.tools.list_ports_osx.comports()):
    devices.append(port.device)
    print(str(i)+": ", port)
    i+=1
    

dev_id = int(input("Write device number: "))

ser = serial.Serial()
ser.port = devices[dev_id]
ser.baudrate = 115200
# ser.timeout = 0.001
# ser.parity = serial.PARITY_EVEN

ser.open()


ser.write(b"start\n")
# ser.read_until(b"\r")

data = [1,2,3,4]
fourier = np.zeros(512)

def animation(i, dat, _):
    byte = ser.read(4)
    if(byte == b"DATA"):
            ser.read(3)
            devid = int.from_bytes(ser.read(1), "little")
            ser.read(8)
            print("SECTION ", devid)
    else:
        # print(int.from_bytes(byte, "big"), str(byte), struct.unpack("f", byte))
        for val in byte:
            # value = int.from_bytes(val.to_bytes(1, "big"), "big", signed=True)
            dat.append(val)
            # print("\t", val, "\t")
    
    dat = dat[-250:]
    
    fft = np.fft.rfft(dat)
    spec = np.abs(fft)
    freq = np.arange(0, samplerate/2,samplerate/2/len(spec))
        
    mask = (freq >= 50) * (freq <= 150)
    ffthat  = fft * mask
    dataHat = np.real(np.fft.irfft(ffthat))
    
    
    axs[3].clear()
    axs[3].plot(ffthat)
    axs[2].clear()
    axs[2].plot(dataHat)
    axs[1].clear()
    axs[1].plot(freq[2:], spec[2:])
    axs[0].clear()
    axs[0].plot(dat)

ani = FuncAnimation(fig, animation, fargs=(data, []), interval=1)

plt.show()

ser.close()
