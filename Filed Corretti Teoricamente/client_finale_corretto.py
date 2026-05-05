import threading, socket, json, time, serial

raccolta_dati = []

def leggi_arduino(porta):
    try:
        # Uso di pyserial per garantire il corretto baud rate (9600)
        with serial.Serial(porta, 9600, timeout=1) as ser:
            while True:
                riga = ser.readline().decode('utf-8', errors='ignore').strip()
                if riga.startswith("{"):
                    try: raccolta_dati.append(json.loads(riga))
                    except: pass
    except: pass

def invia_unificato():
    global raccolta_dati
    while True:
        try:
            s = socket.socket()
            s.connect(("localhost", 5000))
            while True:
                if raccolta_dati:
                    # Assegnazione atomica per evitare race condition senza lock complessi
                    pacchetto = raccolta_dati
                    raccolta_dati = []
                    # sendall garantisce l'invio dell'intero payload
                    s.sendall((json.dumps(pacchetto) + "\n").encode())
                    print(f"Inviato pacchetto con {len(pacchetto)} record.")
                time.sleep(2)
        except: time.sleep(1)

# Il thread principale lancia i thread di lettura
for i in range(1, 11):
    p = f"COM{i}"
    try:
        # Verifica se la porta esiste prima di lanciare il thread
        t = serial.Serial(p); t.close()
        threading.Thread(target=leggi_arduino, args=(p,), daemon=True).start()
    except: pass

# Il thread principale gestisce l'invio (come richiesto)
invia_unificato()
