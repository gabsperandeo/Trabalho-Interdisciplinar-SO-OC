import time
import datetime
from datetime import date
print("Inicio: ")
print("--> Data: ",date.today())
print("--> Horario: ",time.strftime("%H:%M:%S",time.localtime()))

start_time = time.time()
time.sleep(60)
duration = time.time() - start_time

print("-------------------")

print("Fim: ")
print("--> Data: ",date.today())
print("--> Horario: ",time.strftime("%H:%M:%S",time.localtime()))
print("--> Tempo passado: ",str(datetime.timedelta(seconds=round(duration))))