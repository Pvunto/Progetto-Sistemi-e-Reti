import socket
import json
import pymysql

# =========================
# CONFIG
# =========================
HOST = "0.0.0.0"
PORT = 5000

# =========================
# DB
# =========================
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ricarica_colonnine",
        cursorclass=pymysql.cursors.DictCursor
    )

# =========================
# SAVE DB
# =========================
def salva_db(d):
    db = get_db()
    try:
        with db.cursor() as c:
            c.execute("""
                INSERT INTO informazioni_colonnine
                (id_macchina, clienti_day, consumo, profitto, runtime, posizione)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    clienti_day=VALUES(clienti_day),
                    consumo=VALUES(consumo),
                    profitto=VALUES(profitto),
                    runtime=VALUES(runtime),
                    posizione=VALUES(posizione)
            """, (
                d["id_macchina"],
                d["clienti_day"],
                d["consumo"],
                d["profitto"],
                d["runtime"],
                d["posizione"]
            ))
        db.commit()
    finally:
        db.close()

# =========================
# SOCKET HANDLER
# =========================
def handle_client(conn, addr):
    print(f"\n[+] Client connesso: {addr}")

    buffer = ""

    while True:
        data = conn.recv(4096)

        if not data:
            print("[-] Client disconnesso")
            break

        decoded = data.decode(errors="ignore")
        print("\n📡 RAW:", decoded)

        buffer += decoded
        print("🧱 BUFFER:", buffer)

        # =========================
        # FIX: parsing diretto JSON
        # =========================
        try:
            d = json.loads(buffer)

            print("\n🧠 JSON PARSATO:", d)

            inner = d.get("data", {})

            payload = {
                "id_macchina": inner.get("id_macchina"),
                "clienti_day": inner.get("clienti_day", 0),
                "consumo": inner.get("consumo", 0),
                "profitto": inner.get("profitto", 0),
                "runtime": inner.get("runtime", ""),
                "posizione": inner.get("posizione", "")
            }

            print("📦 PAYLOAD:", payload)

            salva_db(payload)

            print("💾 SALVATO SU DB")

            buffer = ""  # reset dopo successo

        except json.JSONDecodeError:
            # JSON non completo ancora → aspetta altro chunk
            pass

    conn.close()
    print("[x] Connessione chiusa")

# =========================
# SERVER
# =========================
def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    print(f"[SERVER] In ascolto su {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)

# =========================
if __name__ == "__main__":
    start()
