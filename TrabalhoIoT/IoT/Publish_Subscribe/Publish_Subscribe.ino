#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Gabriela_Matheus"; // Nome da sua rede Wi-Fi
const char* password = "corno2019"; // Senha da sua rede Wi-Fi
const char* mqttServer = "broker.emqx.io"; // Endereço IP do seu broker MQTT
const int mqttPort = 1883; // Porta MQTT padrão
const char* mqttTopic = "esp8266/led"; // Tópico MQTT para controle do LED

WiFiClient espClient;
PubSubClient client(espClient);
int contL = 0;
int contD = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT); // Configura o LED embutido como saída
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
}

void loop() {
  client.loop();
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

  if (message.equals("liga")) {
    contL++;
    char counterLStr[10];
    sprintf(counterLStr, "%d", contL); // Converte o contador para string
    client.publish("esp8266/teste", counterLStr);
  } else if (message.equals("desliga")) {
    contD++;
    char counterDStr[10];
    sprintf(counterDStr, "%d", contD);
    client.publish("esp8266/teste", counterDStr);
  }
  else if(message.equals("reset liga")){
    contL = 0;
    client.publish("esp8266/teste", "Resetando contagem do liga");
  }
  else if(message.equals("reset desliga")){
    contD = 0;
    client.publish("esp8266/teste", "Resetando contagem do desliga");
  }
}