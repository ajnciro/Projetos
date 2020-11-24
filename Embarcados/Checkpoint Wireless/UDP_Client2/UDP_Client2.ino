#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

WiFiUDP udp;

const char* ssid = "NodeMCU";
const char* password = "12345678";
const char* host = "192.168.4.1";

bool x;         //Valor a ser enviado (leitura de presença no checkpoint
//------------------------------------------- 
void setup()
{
    Serial.begin(115200);
    pinMode(D4, INPUT);
    WiFi.mode(WIFI_STA);
}

//-------------------------------------------- 
void loop()
{
    connect();
    send();
}

void connect()  //Verificando conexão com o módulo servidor
{
    if (WiFi.status() != WL_CONNECTED)
    {
        WiFi.begin(ssid, password);   //Conexão com o AP
        delay(5000);                  //Aguarda
        Serial.print('.');
    }
}

void send()   //Envia o valor x da leitura de presença no checkpoint ao módulo servidor se estiver conectado
{
    if (WiFi.status() == WL_CONNECTED)
    {
        x = digitalRead(D4);
        if (trigSens(x)) {

            udp.beginPacket(host, 11111);
            udp.print(x);
            udp.endPacket();

            // Serial.println(x);    //Apenas para controle da leitura
        }
        delay(3);
    }

    //Serial.println(digitalRead(D4)); //Para controle
}

//----------------------------------------------------------
int i = 0;
bool trigSens(bool sign) {        //Gatilho para envio único na detecção de presença para evitar dados redundantes.
                                  //Apesar da natureza não confiável do protocolo UDP, a experiência mostrou
                                  //que, no raio de atuação dos módulos, não há perdas consideráveis de pacotes

    while (sign == 0) {
        i++;

        if (i == 1) {
            return 1;
            break;
        }

        else
            return 0;
    }

    if (sign == 1)
        i = 0;
}
