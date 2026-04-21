#include <ArduinoJson.h>
#include <LiquidCrystal.h>

#define PIN_POT A0
#define pPOn 3

String id_macchina = "C002";
bool vPOn = false;
int valore = 0;
int percentuale = 0;

LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);

  pinMode(PIN_POT, INPUT);
  pinMode(pPOn, INPUT_PULLUP);  // ✔ corretto
}

void loop() {

  // Lettura potenziometro
  valore = analogRead(PIN_POT);

  // Lettura pulsante (invertita perché pullup)
  vPOn =!digitalRead(pPOn);

  // Percentuale
  percentuale = map(valore, 0, 1023, 0, 100);

  int clienti = random(0, 50);
  int profitto = percentuale * 2;
  int runtime = millis() / 1000;

  StaticJsonDocument<200> doc;

  doc["id_macchina"] = id_macchina;
  doc["clienti_day"] = clienti;
  doc["consumo"] = percentuale;
  doc["profitto"] = profitto;
  doc["runtime"] = runtime;

  if (vPOn) {

    // JSON pulito
    serializeJsonPretty(doc, Serial);
    Serial.println();

    // LCD pulito
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Batteria:");

    lcd.setCursor(0, 1);
    lcd.print(percentuale);
    lcd.print("%");
  }
}