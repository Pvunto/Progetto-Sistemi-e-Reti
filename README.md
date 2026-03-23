# Sistema di Comunicazione Client-Server per Colonnina di Ricarica

## Descrizione del Progetto

Questo progetto implementa un sistema di comunicazione client-server per la gestione di una colonnina di ricarica per veicoli elettrici. Il sistema è progettato per trasmettere dati operativi da un dispositivo embedded (microcontrollore) a un server remoto, utilizzando un socket di comunicazione.

L’obiettivo principale è definire un formato strutturato di trasmissione dei dati e realizzare un meccanismo affidabile per lo scambio delle informazioni tra client e server.

## Contesto Applicativo

Nel contesto delle infrastrutture di ricarica per veicoli elettrici, è necessario monitorare e registrare parametri fondamentali relativi alle sessioni di ricarica. Il sistema descritto consente di inviare tali dati a un server centrale per finalità di controllo, analisi e fatturazione.

## Dati Trasferiti

Il protocollo di comunicazione prevede l’invio dei seguenti campi:

- **Data e ora**: timestamp della sessione di ricarica
- **ID cliente**: identificativo univoco dell’utente
- **Percentuale di carica**: livello di carica della batteria al termine della sessione
- **Energia erogata**: quantità di energia fornita (espressa in kWh)

## Architettura del Sistema

Il sistema è composto da due componenti principali:

### Client

- Simula il comportamento del microcontrollore della colonnina
- Raccoglie i dati della sessione di ricarica
- Serializza i dati secondo un formato definito
- Stabilisce una connessione socket verso il server
- Invia i dati

### Server

- Rimane in ascolto su una porta predefinita
- Accetta connessioni da uno o più client
- Riceve e deserializza i dati
- Esegue eventuali operazioni di logging o elaborazione

## Formato dei Dati

I dati possono essere trasmessi in formato testuale strutturato (ad esempio JSON) oppure in un formato personalizzato. Un esempio in JSON è il seguente:

```
{
  "timestamp": "2026-03-18T10:30:00",
  "id_cliente": "CL12345",
  "percentuale_carica": 85,
  "energia_erogata": 22.5
}
```

## Tecnologie Utilizzate

- Linguaggio di programmazione: a scelta (es. Python, C, Java)
- Comunicazione di rete: socket TCP/IP
- Formato dati: JSON (o equivalente)

## Istruzioni per l’Esecuzione

### Server

1. Avviare il server.

2. Il server rimarrà in ascolto sulla porta configurata.

### Client

1. Configurare i parametri di connessione (indirizzo IP e porta del server)

2. Avviare il client:

3. Il client invierà i dati al server.


## Autore

Progetto sviluppato a scopo didattico per lo studio dei sistemi distribuiti e della comunicazione client-server.
