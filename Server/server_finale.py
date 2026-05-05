import socket, json, mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "tua_password",
    "database": "nome_db"
}

s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)
print("Server pronto...")

while True:
    conn, addr = s.accept()
    f = conn.makefile('r')
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        for riga in f:
            try:
                pacchetto = json.loads(riga)
                for d in pacchetto:
                    sql = "INSERT INTO colonnine_ricarica (id_macchina, clienti, consumo, profitto, runtime, posizione) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (d.get("id_macchina"), d.get("clienti_day"), d.get("consumo"), d.get("profitto"), d.get("runtime"), d.get("posizione"))
                    cursor.execute(sql, val)
                db.commit()
                print(f"Inserito pacchetto da {len(pacchetto)} record.")
            except: pass
        cursor.close(); db.close()
    except: pass
    conn.close()
