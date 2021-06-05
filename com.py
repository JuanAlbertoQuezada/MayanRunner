import serial, time


mando = serial.Serial('COM9', 9600);
time.sleep(2)
_dataRec = mando.readline()
print(_dateRec)
mando.close()
