#include <ArduinoJson.h>
#include <LiquidCrystal.h>

#define PIN_POT A0
#define pPOn 3

String id_macchina = "C001";
volatile bool triggerStampa = false;  // flag interrupt

int valore = 0;
int percentuale = 0;

LiquidCrystal lcd(12, 11, 5, 4, 7, 2);

// ISR (deve essere veloce!)
void onButtonPress() {
  triggerStampa = true;
}

void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("Salve");
  pinMode(PIN_POT, INPUT);
  pinMode(pPOn, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(pPOn), onButtonPress, FALLING);
}

void loop() {

  // Lettura potenziometro
  valore = analogRead(PIN_POT);
  percentuale = map(valore, 0, 1023, 0, 100);

  int clienti = random(0, 50);
  int profitto = percentuale * 2;
  int runtime = millis() / 1000;

  // Se interrupt attivato
  if (triggerStampa) {

    triggerStampa = false;  // reset flag

    StaticJsonDocument<200> doc;

    doc["id_macchina"] = id_macchina;
    doc["clienti_day"] = clienti;
    doc["consumo"] = percentuale;
    doc["profitto"] = profitto;
    doc["runtime"] = runtime;

    // JSON
    serializeJsonPretty(doc, Serial);
    Serial.println();

    // LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Batteria:");

    lcd.setCursor(0, 1);
    lcd.print(percentuale);
    lcd.print("%");
  }
}