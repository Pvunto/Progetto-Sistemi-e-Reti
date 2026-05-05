import socket, json, sqlite3

DB_FILE = "dati_colonnine.db"

def inizializza_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # id_macchina diventa PRIMARY KEY per permettere la sovrascrittura
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS colonnine_ricarica (
            id_macchina TEXT PRIMARY KEY,
            clienti INTEGER,
            consumo INTEGER,
            profitto INTEGER,
            runtime TEXT,
            posizione TEXT
        )
    ''')
    conn.commit()
    conn.close()

inizializza_db()

s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)
print("Server pronto (Sovrascrittura attiva)...")

while True:
    conn, addr = s.accept()
    f = conn.makefile('r', encoding='utf-8')
    try:
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()
        for riga in f:
            try:
                pacchetto = json.loads(riga)
                if not isinstance(pacchetto, list): pacchetto = [pacchetto]
                
                for d in pacchetto:
                    # INSERT OR REPLACE sovrascrive i dati se id_macchina esiste già
                    sql = "INSERT OR REPLACE INTO colonnine_ricarica (id_macchina, clienti, consumo, profitto, runtime, posizione) VALUES (?, ?, ?, ?, ?, ?)"
                    val = (d.get("id_macchina"), d.get("clienti_day"), d.get("consumo"), d.get("profitto"), d.get("runtime"), d.get("posizione"))
                    cursor.execute(sql, val)
                
                db.commit()
                print(f"Aggiornato pacchetto da {len(pacchetto)} record.")
            except: pass
        db.close()
    except: pass
    conn.close()
