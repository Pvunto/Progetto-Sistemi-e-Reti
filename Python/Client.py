import json
import urllib.request

url = "http://192.168.1.100/server.php"  # IP del server

# Esempio 1: nuovo codiceID
dati1 = {
    "codiceID": "A123",
    "nome": "Luca",
    "eta": 25,
    "citta": "Pordenone"
}

# Esempio 2: stesso codiceID → aggiunge
dati2 = {
    "codiceID": "A123",
    "nome": "Anna",
    "eta": 30,
    "citta": "Udine"
}

for dati in [dati1, dati2]:
    json_data = json.dumps(dati).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=json_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())