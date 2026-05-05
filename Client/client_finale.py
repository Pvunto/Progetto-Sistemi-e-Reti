import threading, socket, json, time

raccolta_dati = []

def leggi_arduino(porta):
    """
    Legge i dati dalla porta seriale usando le funzioni di base di Python.
    Su Windows, le porte COM possono essere aperte come file, ma richiedono
    una gestione specifica per evitare blocchi.
    """
    try:
        # L'uso del prefisso \\.\ è corretto per Windows per accedere alle porte COM > 9
        with open(f'\\\\.\\{porta}', 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                riga = f.readline().strip()
                if riga.startswith("{"):
                    try:
                        dati = json.loads(riga)
                        raccolta_dati.append(dati)
                    except:
                        pass
                time.sleep(0.1)
    except:
        pass

def invia_unificato():
    global raccolta_dati
    while True:
        try:
            s = socket.socket()
            s.connect(("localhost", 5000))
            print("Connesso al server.")
            while True:
                if raccolta_dati:
                    # Copia e svuota la lista in modo semplice
                    pacchetto = raccolta_dati[:]
                    raccolta_dati.clear()
                    
                    # Invia i dati come stringa JSON seguita da newline
                    s.send((json.dumps(pacchetto) + "\n").encode())
                    print(f"Inviato pacchetto con {len(pacchetto)} record.")
                time.sleep(2)
        except:
            time.sleep(1)

# Scansione porte COM (1-10) e avvio thread di lettura
for i in range(1, 11):
    p = f"COM{i}"
    # Tentativo di apertura veloce per vedere se la porta esiste
    try:
        # Nota: l'apertura come file 'r' può fallire se il baud rate non è pre-configurato
        # o se la porta è già occupata. In un ambiente senza pyserial, 
        # si assume che la porta sia già configurata dal sistema (es. tramite terminale).
        f = open(f'\\\\.\\{p}', 'r'); f.close()
        threading.Thread(target=leggi_arduino, args=(p,), daemon=True).start()
        print(f"Avviato thread per {p}")
    except:
        pass

# Avvio thread di invio e attesa
threading.Thread(target=invia_unificato, daemon=True).start()

while True:
    time.sleep(1)
