import threading, socket, json, time
import serial
import serial.tools.list_ports
import sys

raccolta_dati = []
raccolta_dati_lock = threading.Lock()

def leggi_arduino(porta, baud_rate=9600):
    """
    Legge i dati dalla porta seriale usando pyserial.
    """
    try:
        ser = serial.Serial(porta, baud_rate, timeout=1)
        print(f"Connesso alla porta seriale {porta}")
        while True:
            try:
                riga = ser.readline().decode("utf-8").strip()
                if riga.startswith("{") and riga.endswith("}"):
                    try:
                        dati = json.loads(riga)
                        with raccolta_dati_lock:
                            raccolta_dati.append(dati)
                    except json.JSONDecodeError:
                        # Ignora righe non JSON valide o incomplete
                        pass
            except serial.SerialException as e:
                print(f"Errore di lettura dalla porta {porta}: {e}")
                break # Esci dal ciclo di lettura in caso di errore grave
            except UnicodeDecodeError:
                # Ignora errori di decodifica se la riga non è UTF-8 valida
                pass
            time.sleep(0.01) # Piccola pausa per non sovraccaricare la CPU
    except serial.SerialException as e:
        print(f"Impossibile aprire la porta seriale {porta}: {e}")
    except Exception as e:
        print(f"Errore generico nel thread di lettura per {porta}: {e}")

def invia_unificato():
    global raccolta_dati
    while True:
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 5000))
            print("Connesso al server socket.")
            while True:
                pacchetto = []
                with raccolta_dati_lock:
                    if raccolta_dati:
                        pacchetto = raccolta_dati[:]
                        raccolta_dati.clear()
                
                if pacchetto:
                    # Invia i dati come stringa JSON seguita da newline
                    s.sendall((json.dumps(pacchetto) + "\n").encode("utf-8"))
                    print(f"Inviato pacchetto con {len(pacchetto)} record.")
                time.sleep(2)
        except ConnectionRefusedError:
            print("Connessione al server socket rifiutata. Riprovo...")
            time.sleep(5) # Attendi di più prima di riprovare la connessione
        except socket.error as e:
            print(f"Errore socket: {e}. Riconnessione in corso...")
            time.sleep(5) # Attendi di più prima di riprovare la connessione
        except Exception as e:
            print(f"Errore generico nel thread di invio: {e}")
            time.sleep(5)
        finally:
            if s:
                s.close()

# Scansione porte COM/tty e avvio thread di lettura
ports = serial.tools.list_ports.comports()
found_ports = []
for p in ports:
    found_ports.append(p.device)

if not found_ports:
    print("Nessuna porta seriale trovata. Assicurati che Arduino sia connesso.")

for p in found_ports:
    threading.Thread(target=leggi_arduino, args=(p,), daemon=True).start()
    print(f"Avviato thread per {p}")

# Avvio thread di invio e attesa
threading.Thread(target=invia_unificato, daemon=True).start()

print("Script avviato. Digita 'exit' per terminare.")

while True:
    try:
        user_input = input("\nStato (digita 'exit' per terminare): ")
        if user_input.lower() == 'exit':
            print("Terminazione dello script...")
            break
        else:
            with raccolta_dati_lock:
                print(f"Record in attesa di invio: {len(raccolta_dati)}")
    except EOFError:
        # Gestisce la chiusura dell'input (es. Ctrl+D)
        print("EOF ricevuto, terminazione dello script...")
        break
    except KeyboardInterrupt:
        # Gestisce Ctrl+C
        print("Interruzione da tastiera, terminazione dello script...")
        break
    except Exception as e:
        print(f"Errore nel ciclo principale: {e}")
        time.sleep(1)

sys.exit(0)
