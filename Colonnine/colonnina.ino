#include <ArduinoJson.h>
#include <LiquidCrystal.h>

#define PIN_POT A0
#define pPOn 3

String id_macchina = "C001";
volatile bool triggerStampa = false;

int valore = 0, percentuale = 0;
char buffer[10];
unsigned long secondiTot = 0;
int ore = 0, minuti = 0, secondi = 0;
int clienti = 0, profitto = 0;
String posizione = "Lat: 45.70, Lon: 12.25";

LiquidCrystal lcd(12, 11, 5, 4, 7, 2);

void onButtonPress() { triggerStampa = true; }

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  pinMode(PIN_POT, INPUT);
  pinMode(pPOn, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pPOn), onButtonPress, FALLING);
}

void loop() {
  valore = analogRead(PIN_POT);
  percentuale = map(valore, 0, 1023, 0, 100);
  clienti = random(0, 50);
  profitto = percentuale * 2;

  if (triggerStampa) {
    triggerStampa = false;
    secondiTot = millis() / 1000;
    ore = secondiTot / 3600;
    minuti = (secondiTot % 3600) / 60;
    secondi = secondiTot % 60;
    sprintf(buffer, "%02d:%02d:%02d", ore, minuti, secondi);

    StaticJsonDocument<200> doc;
    doc["id_macchina"] = id_macchina;
    doc["clienti_day"] = clienti;
    doc["consumo"] = percentuale;
    doc["profitto"] = profitto;
    doc["runtime"] = buffer;
    doc["posizione"] = posizione;

    // USARE serializeJson (senza Pretty) per Python
    serializeJson(doc, Serial);
    Serial.println();

    lcd.clear();
    lcd.print("Inviato!");
  }
}