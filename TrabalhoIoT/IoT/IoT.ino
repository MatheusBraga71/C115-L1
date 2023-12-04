#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define INTERVALO_ENVIO 5000

#define AZUL 14
#define VERMELHO 12

#define DHTPIN 4
#define DHTTYPE DHT11
const int potPin = A0;

DHT dht(DHTPIN, DHTTYPE);

#define DEBUG

// inormações da rede wifi
const char* ssid = "RedeMatheusS20";
const char* password = "vjgc0483";
const char* mqttServer = "broker.emqx.io"; // Endereço IP do seu broker MQTT
const int mqttPort = 1883; // Porta MQTT padrão
const char* mqttTopic = "testeMABP/infos"; // Tópico MQTT para controle do LED

int ultimoEnvioMQTT = 0;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(AZUL, OUTPUT);
  pinMode(VERMELHO, OUTPUT);
  digitalWrite(AZUL, LOW);
  digitalWrite(VERMELHO, LOW);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao Wi-Fi...");
  }
  Serial.println("Conectado ao Wi-Fi");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  if (client.connect("ESP8266Client")) {
    Serial.println("Conectado ao MQTT");
    client.subscribe(mqttTopic);
  } else {
    Serial.print("Falha na conexão, rc=");
    Serial.print(client.state());
  }

  dht.begin(); // inicialização do dht11
}

void callback(char* topic, byte* payload, unsigned int length) {

  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Mensagem recebida no tópico: ");
  Serial.println(topic);
  Serial.print("Conteúdo: ");
  Serial.println(message);

  if (message.equals("umidade")) {
    enviaUmidadeDHT();
  } 
  else if (message.equals("temperatura")) {
    enviaTemperaturaDHT();
  }
  else if(message.equals("carga")){
    carga();
  }
  else if(message.equals("todos")){
    enviaUmidadeDHT();
    enviaTemperaturaDHT();
    carga();
  }
  else if(message.equals("aumentar temp")){
    client.publish("testeMABP/temperatura", "Aumentando a temperatura");
    digitalWrite(VERMELHO, HIGH);
    delay(8000);
    digitalWrite(VERMELHO, LOW);    
  }
  else if(message.equals("diminuir temp")){
    client.publish("testeMABP/temperatura", "Diminuindo a temperatura");
    digitalWrite(AZUL, HIGH);
    delay(8000);
    digitalWrite(AZUL, LOW);      
  }
  
}


void loop() {

/*
  if ((millis() - ultimoEnvioMQTT) > INTERVALO_ENVIO){
    enviaDHT();
    carga();
    ultimoEnvioMQTT = millis();
  }
  */

  if (client.connect("ESP8266Client")) {
    Serial.println("Conectado ao MQTT");
    client.subscribe(mqttTopic);
  } else {
    Serial.print("Falha na conexão, rc=");
    Serial.print(client.state());
  }

  client.loop();
  delay(500);
}

void carga(){
  char msgCargaMQTT[100];

  // Lê o valor do potenciômetro
  float potValue = analogRead(potPin);
  
  // Mapeia o valor lido do potenciômetro para um valor de carga simulado (entre 0 e 100, por exemplo)
  float simulatedLoad = map(potValue, 0, 1023, 0, 100);

  if (isnan(simulatedLoad)){
    #ifdef DEBUG
    Serial.println("Falha na leitura da carga...");
    #endif
  }
  else{
    #ifdef DEBUG
     Serial.print("Carga: ");
    Serial.println(simulatedLoad);
    #endif

    sprintf(msgCargaMQTT, "%f", simulatedLoad);
    client.publish("testeMABP/carga", msgCargaMQTT);

    if (simulatedLoad <= 10.0){
      client.publish("testeMABP/carga", "Atenção com o nível de combustível");
      for (int i = 0; i < 5; i++) {
        digitalWrite(AZUL, HIGH);
        digitalWrite(VERMELHO, LOW);
        delay(1000);
        digitalWrite(AZUL, LOW);
        digitalWrite(VERMELHO, HIGH);
        delay(1000);
      }
      digitalWrite(VERMELHO, LOW);
      digitalWrite(AZUL, LOW);
    }
  }
}

void enviaUmidadeDHT(){
  char msgUmidadeMQTT[100];
  float umidade = dht.readHumidity();

  if (isnan(umidade)){

    #ifdef DEBUG
    Serial.println("Falha na leitura do dht11...");
    #endif
  }
  else{
    #ifdef DEBUG
    Serial.print("Umidade: ");
    Serial.println(umidade);
    #endif

    sprintf(msgUmidadeMQTT, "%f", umidade);
    Serial.print("Umidade mqtt: ");
    Serial.println(msgUmidadeMQTT);
    client.publish("testeMABP/umidade", msgUmidadeMQTT);
  }

}

void enviaTemperaturaDHT(){
  char msgTemperaturaMQTT[100];
  float temperatura = dht.readTemperature();

  if (isnan(temperatura)){

    #ifdef DEBUG
    Serial.println("Falha na leitura do dht11...");
    #endif
  }
  else{
    #ifdef DEBUG
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" ºC");
    #endif

    sprintf(msgTemperaturaMQTT, "%f", temperatura);
    Serial.print("Temperatura mqtt: ");
    Serial.println(msgTemperaturaMQTT);
    client.publish("testeMABP/temperatura", msgTemperaturaMQTT);
  }
}