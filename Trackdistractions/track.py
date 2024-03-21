import psutil
import time
import sys
import signal
from logger_base import log

class TrackApp:
    #Definir variables de tiempo
    MINUTES = 0
    SECCONDS = 0
    HOURS = 0
    
    #Calculos de procesos
    pid = None
    proc_on = False
    proc_found = False
    
    #Otras variables
    TIME_FILE = "status.txt"
    limit_time = 10 #Mejorar para que se ponga el tiempo en minutos y horas y que el programa lo convierta segundos
    
    def def_handler(sig, frame):
        print("\n\n[!]Saliendo ...\n")
        sys.exit(1)
        
    def __init__(self, name_app):
        self.name_app = name_app
        self.elapsed_time = self.load_time
        self.time_started = time.time() #Captura el tiempo actual desde su ejecución
        
    def save_time(self):
        with open(self.TIME_FILE, "w") as file:
            file.write(str(self.elapsed_time))
            
    def load_time(self):
        try:
            with open(self.TIME_FILE, "r") as file:
                time_save = float(file.read)
                return time_save
        except Exception as e:
            print("Ocurrio un error: {}".format(e))
            return 0.0
            
    
    def track(self):
        
        while True:
            
            signal.signal(signal.SIGINT, TrackApp.def_handler)
            proc_iter = psutil.process_iter(["pid", "name"])
            
            process = [proces.info for proces in proc_iter if '{}.exe'.format(self.name_app) in proces.info['name']] #Practicar lista comprimidas
            
            actual_time = time.time()
            time_past = actual_time - self.time_started

            # Calcular el tiempo que falta para el próximo segundo
            sleep_time = max(1 - (time_past % 1), 0)
            time.sleep(sleep_time) # Entender esta linea de código
            
            if process:
                #print(process[0]['name'])process = psutil.Process(self.pid)
                pid = psutil.Process(process[0]['pid'])
                self.elapsed_time = time_past
                 
                
                if self.elapsed_time >= self.limit_time:
                    self.close_app(pid)
                    log.info("La app se cerro")
                    #break
                else:
                    print("Tiempo transcurrido: {:.1f} segundos".format(time_past))
                    
                self.save_time()
    
    def close_app(self, pid):
        pid.terminate()
        self.proc_on = False
    
if __name__ == "__main__":
    trackLol = TrackApp("Notepad")
    trackLol.track()
