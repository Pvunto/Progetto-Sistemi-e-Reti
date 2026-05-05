import serial
import serial.tools.list_ports
import threading
import json
import socket
import time

# =========================
# CONFIG
# =========================
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
BAUDRATE = 9600

# =========================
# BUFFER GLOBALI (NO queue)
# =========================
serial_buffer = []
send_buffer = []

serial_lock = threading.Lock()
send_lock = threading.Lock()

# =========================
# LOG
# =========================
def log(msg):
    print(f"[CLIENT] {msg}")

# =========================
# SCOPERTA ARDUINO
# =========================
def find_arduinos():
    ports = serial.tools.list_ports.comports()
    arduino_ports = []

    for p in ports:
        if "USB" in p.description or "Arduino" in p.description or "CH340" in p.description:
            arduino_ports.append(p.device)

    log(f"Trovati {len(arduino_ports)} dispositivi: {arduino_ports}")
    return arduino_ports

# =========================
# THREAD SERIAL READER
# =========================
def serial_reader(port):
    try:
        ser = serial.Serial(port, BAUDRATE, timeout=1)
        log(f"Connesso a {port}")

        while True:
            line = ser.readline().decode(errors='ignore').strip()

            if line:
                log(f"[{port}] RX: {line}")

                try:
                    data = json.loads(line)

                    with serial_lock:
                        serial_buffer.append((port, data))

                except json.JSONDecodeError:
                    log(f"[{port}] JSON non valido")

    except Exception as e:
        log(f"Errore su {port}: {e}")

# =========================
# THREAD AGGREGATOR
# =========================
def aggregator():
    while True:
        time.sleep(0.05)

        with serial_lock:
            if not serial_buffer:
                continue
            local_copy = serial_buffer[:]
            serial_buffer.clear()

        for port, data in local_copy:
            log(f"Aggrego da {port}: {data}")

            payload = {
                "source_port": port,
                "data": data
            }

            with send_lock:
                send_buffer.append(payload)

# =========================
# THREAD SENDER SOCKET
# =========================
def sender():
    while True:
        time.sleep(0.05)

        with send_lock:
            if not send_buffer:
                continue
            local_copy = send_buffer[:]
            send_buffer.clear()

        for payload in local_copy:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((SERVER_IP, SERVER_PORT))

                msg = json.dumps(payload)
                s.sendall(msg.encode())

                log(f"INVIATO: {msg}")

                s.close()

            except Exception as e:
                log(f"Errore socket: {e}")

# =========================
# MAIN
# =========================
def main():
    ports = find_arduinos()

    for port in ports:
        threading.Thread(target=serial_reader, args=(port,), daemon=True).start()

    threading.Thread(target=aggregator, daemon=True).start()
    threading.Thread(target=sender, daemon=True).start()

    log("Client avviato")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
