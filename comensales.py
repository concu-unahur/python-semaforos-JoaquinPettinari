import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforo = threading.Semaphore(3)
platosDisponibles = 3

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'
    
  def reponerPlatos(self):
    global platosDisponibles
    global semaforo

    platosDisponibles += 3
    for i in range(3):
      semaforo.release()

    logging.info(f'Reponiendo los platos')



class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles

    if(platosDisponibles <= 0):
      Cocinero.reponerPlatos(Cocinero)
      semaforo.release()

    platosDisponibles -= 1
    semaforo.acquire()
    logging.info(f' ¡Que rico! Quedan {platosDisponibles} platos')    


Cocinero().start()

for i in range(5):
  Comensal(i).start()

