import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoCocinero = threading.Semaphore(0)
semaforoComensal = threading.Semaphore(1)
platosDisponibles = 3

class Cocinero(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Cocinero {numero}'
  
  def run(self):
    global platosDisponibles
    global semaforoCocinero
    global semaforoComensal


    while(True):
      semaforoCocinero.acquire()
      try:
        logging.info(f'Reponiendo los platos')  
        platosDisponibles = 3
      finally:
        semaforoComensal.release()





class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    global semaforoCocinero
    global semaforoComensal

    semaforoComensal.acquire()

    try:
      if(platosDisponibles <= 0):
        semaforoCocinero.release()
        semaforoComensal.acquire()
        platosDisponibles -= 1
        logging.info(f' ¡Que rico! Quedan {platosDisponibles} platos')

      else:
        platosDisponibles -= 1
        logging.info(f' ¡Que rico! Quedan {platosDisponibles} platos')
    
    finally:
      semaforoComensal.release()
  

 
for i in range(2):
  Cocinero(i).start()


for i in range(10):
  Comensal(i).start()

