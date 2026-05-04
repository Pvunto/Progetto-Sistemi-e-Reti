import threading, socket, json, time

raccolta_dati = []

def leggi_arduino(porta):
    try:
        with open(f'\\\\.\\{porta}', 'r') as f:
            while True:
                riga = f.readline().strip()
                if riga.startswith("{"):
                    try: raccolta_dati.append(json.loads(riga))
                    except: pass
    except: pass

def invia_unificato():
    while True:
        try:
            s = socket.socket()
            s.connect(("localhost", 5000))
            while True:
                if raccolta_dati:
                    pacchetto = list(raccolta_dati)
                    raccolta_dati.clear()
                    s.send((json.dumps(pacchetto) + "\n").encode())
                    print(f"Inviato pacchetto con {len(pacchetto)} record.")
                time.sleep(2)
        except: time.sleep(1)

for i in range(1, 11):
    p = f"COM{i}"
    try:
        t = open(f'\\\\.\\{p}', 'r'); t.close()
        threading.Thread(target=leggi_arduino, args=(p,), daemon=True).start()
    except: pass

threading.Thread(target=invia_unificato, daemon=True).start()
while True: time.sleep(1)