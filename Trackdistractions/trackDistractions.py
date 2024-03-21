#! python 3
import psutil
import time
import sys
import ctypes
import threading
import signal
from logger_base import log

class TrackApp:

    # Definir los tiempos
    SECONDS = 0
    MINUTES = 0
    HOURS = 0

    # Controladores de los procesos
    pid = None
    start_time = 0
    proc_found = False
    proc_on = False

    # Definir los tipos de mensajes
    MB_OK = 0x0
    MB_OKCANCEL = 0x1
    MB_YESNO = 0x4

    # Definir los íconos de mensajes
    MB_ICONERROR = 0x10
    MB_ICONINFORMATION = 0x40
    MB_ICONWARNING = 0x30
    MB_ICONQUESTION = 0x20

        
    def def_handler(sig, frame):
        print("\n\n[!]Saliendo ...\n")
        sys.exit(1)


    def __init__(self, name):
        self._name = name

    
    # Funcion que controla el tipo de reloj del programa
    def stopwatch(self, time):
        self.MINUTES, self.SECONDS = divmod(int(time), 60)
        self.HOURS, self.MINUTES = divmod(self.MINUTES, 60)
        return "{:02d}:{:02d}:{:02d}".format(self.HOURS, self.MINUTES, self.SECONDS)
    
    # Funcion principal, detecta si la aplicacion esta abierta y si su tiempo de uso ya paso la cierra y no deja que esta se vuelva a abrir
    def track(self):
       
        proc_iter = psutil.process_iter(["pid", "name"]) #Captura todos los procesos en ese momento
        aplication_name = "{}.exe".format(self._name) # Al parametro del metodo contructor le pasamos el formato de exe
        
       
        while self.proc_found is False: # Se recorren todos los procesos en busca de la aplicacion deseada
            try:
                proc = next(proc_iter)
                if proc.info["name"] == aplication_name:
                    self.pid = proc.info['pid']
                    process = psutil.Process(self.pid)

                    with open("status.txt", "r") as file_status: # Abrimos el archivo en modo lectura para ver si el proceso ya fue cerrado anteriormente 
                        status = file_status.readline().strip() #El méteodo readline() nos lee la primera linea debido a que el archivo se escribio con un salto de linea hay que 
                        if status == "1": # añadir el método strip() para que se nos elimine a la hora de leerlo.
                            process.terminate()
                            exit()
                            
                    self.start_time = time.time()
                    self.proc_found = True
                    self.proc_on = True

            except StopIteration:
                self.proc_found = True
                

        #if self.pid == None:
            #print("La aplicación {} no este en ejecución".format(self._name))


        while self.proc_on is True: # Si el proceso fue encontrado entonces se temporiza el tiempo
            try:
                psutil.Process(self.pid)
                actual_time = time.time() - self.start_time
                
                #formatted_timme = self.stopwatch(actual_time)#Guarda el tiempo en formato 00:00:00
                #sys.stdout.write("\rTiempo transcurrido: {}".format(formatted_timme))
                #sys.stdout.flush()
                #time.sleep(1)             

                if self.MINUTES == 0 and self.SECONDS == 15: # La apliacion se cierra si el tiempo se termino
                    #print("\nEl proceso tiene que detenerse")
                    process.terminate()
                    message = ctypes.windll.user32.MessageBoxW(0, "Se te acabo el tiempo wachin.", "Cerar Lol", self.MB_OK)
                    self.proc_on = False
                    with open("status.txt", "w") as file_status: # Una vez cerrado el proceso se escribe una señal en un archivo para tener constancia de esto
                        file_status.write("1\n") #Mejorando de manera experimental hay que parsear el documento para detectar la primera linea que es el status
                        file_status.write("0:0:0") # Si hago que se escribe a cada momento el tiepo en un documento esta linea no hara falta
                else:
                    with open ("status.txt", "w") as file_status:
                        file_status.write("0\n" + "{}:{}:{}".format(self.HOURS, self.MINUTES, self.SECONDS))
                        log.info(actual_time)
                        

            except psutil.NoSuchProcess:
                #print("\El timpo total fue de: {}".format(formatted_timme))
                self.proc_on = False


# guardar el tiempo en una variable dentro del propio registro para poder gaurdar el tiempo y que asi se el proceso deja de ejecutarse al volver el tiempo se sume        
# Cuando el proceso se cierra entes de que se acabe el tiempo el contador se reinicia ARREGLAR ESO
#Poner debuguer y arreglar lo del error del archivo (track_time = file_track[1].split(":")) if si tiene contendio el txt entonces
if __name__ == "__main__":
    while True:
        signal.signal(signal.SIGINT, TrackApp.def_handler)
        track = TrackApp("Notepad")
        track.track()
        time.sleep(3)
"""    Track_aplication = TrackApp("Notepad")
    Track_aplication.track()"""