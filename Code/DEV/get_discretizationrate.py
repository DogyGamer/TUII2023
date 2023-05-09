from DEV.KomsibUNIORReader import SerialReader
import time

reader = SerialReader()
reader.startThread()
time.sleep(10)
FS = len(reader.data) / 10
print(FS)
