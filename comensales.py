import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoCocinero = threading.Semaphore(0)
semaforoComensal = threading.Semaphore(3)
platosDisponibles = 3

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'
  
  def run(self):
    global platosDisponibles
    global semaforoCocinero
    global semaforoComensal

    semaforoCocinero.acquire()

    platosDisponibles += 3
    logging.info(f'Reponiendo los platos')  
    semaforoComensal.release()
    semaforoComensal.release()
    semaforoComensal.release()



class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles



    if(platosDisponibles <= 0):
      semaforoCocinero.release()
      semaforoComensal.acquire() 
    else:
      platosDisponibles -= 1
      logging.info(f' ¡Que rico! Quedan {platosDisponibles} platos')
      semaforoComensal.acquire()
  

Cocinero().start()


for i in range(10):
  Comensal(i).start()

