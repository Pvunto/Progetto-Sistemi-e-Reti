# threaded_serial_json.py Progetto sistemi e reti

import threading
import queue
import serial
import socket
import json
import time
import sys

# Configurazione della porta seriale e del server
SERIAL_PORT = '/dev/ttyUSB0'  # Modifica se necessario
BAUDRATE = 9600
SERVER_IP = '127.0.0.1'  # Indirizzo IP del server
SERVER_PORT = 5000         # Porta del server
SEND_INTERVAL = 5          # Intervallo di invio in secondi

# Coda per comunicazione tra thread e lock per accesso concorrente al JSON

serial_queue = queue.Queue()
json_lock = threading.Lock()
merged_json = {}

# Evento globale per la terminazione ordinata
stop_event = threading.Event()

def serial_reader():
    
    """
    Thread 1: Legge dati dalla seriale e li inserisce nella coda serial_queue.
    Ogni riga letta viene considerata come una stringa JSON.
    """

    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    except Exception as e:
        print(f"Errore apertura seriale: {e}")
        return
    while not stop_event.is_set():
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                serial_queue.put(line)  # Inserisce la riga nella coda
        time.sleep(0.1)
    ser.close()

def json_processor():
    
    """
    Thread 2: Prende i dati dalla coda, li elabora e li unifica in un unico JSON.
    Se il dato non è un JSON valido, lo ignora.
    """

    global merged_json
    while not stop_event.is_set():
        try:
            data = serial_queue.get(timeout=1)
            try:
                json_data = json.loads(data)
                with json_lock:
                    merged_json.update(json_data)
            except json.JSONDecodeError:
                pass
        except queue.Empty:
            continue

def json_sender():
    
    """
    Thread 3: Invia periodicamente il JSON unificato al server specificato.
    Dopo l'invio, svuota il JSON unificato.
    """

    global merged_json
    while not stop_event.is_set():
        time.sleep(SEND_INTERVAL)
        with json_lock:
            if merged_json:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((SERVER_IP, SERVER_PORT))
                    s.sendall(json.dumps(merged_json).encode())
                    s.close()
                    merged_json.clear()
                except Exception as e:
                    print(f'Errore invio dati: {e}')


def main():
    """

    Avvia i tre thread e mantiene il programma attivo.
    Se l'utente digita 'fine' nel terminale, chiude tutto ordinatamente.
    """

    t1 = threading.Thread(target=serial_reader)
    t2 = threading.Thread(target=json_processor)
    t3 = threading.Thread(target=json_sender)
    t1.start()
    t2.start()
    t3.start()
    print("Digita 'fine' e premi Invio per terminare il programma.")
    try:
        while not stop_event.is_set():
            user_input = sys.stdin.readline().strip().lower()
            if user_input == 'fine':
                print("Chiusura in corso...")
                stop_event.set()
                break
    except KeyboardInterrupt:
        stop_event.set()
    # Attendi la chiusura dei thread
    t1.join()
    t2.join()
    t3.join()
    print("Programma terminato.")

if __name__ == '__main__':
    main()
