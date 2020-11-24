#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <SoftwareSerial.h>
SoftwareSerial BT(D4, D3);    //Caso se deseje leituras via USB

WiFiUDP udp;

String req, dados = "";

//-----------------------------------------------------
void setup()
{
    BT.begin(9600);
    Serial.begin(115200);

    while (1) {
        if (BT.available() > 0)
            dados = BT.readString();
        if (dados[0] == '$' || Serial.read() == '$') {
            BT.println("Comecando...");
            Serial.println("Comecando...");
            break;
        }
    }

    pinMode(D1, INPUT);
    WiFi.mode(WIFI_AP);
    WiFi.softAP("NodeMCU", "12345678");     //Inicia o AP com ssid e senha
    delay(2000);
}

//---------------------------------------------------
bool s0 = 0;
int lap = 0;
unsigned long t0 = 0, tn = 0, dtn = 0, dtt = 0;
//---------------------------------------------------
void loop()
{
    listen();
}

void listen()                               //verifica se o módulo cliente está tentando enviar dados
{
    s0 = trigSens(digitalRead(D1));         //disparo da contagem pelo sensor acoplado ao módulo servidor e envia valor ao dispositivo BT
    if (s0) {
        BT.println(0.0);
        Serial.println("0.0");
        t0 = millis();
        s0 = 0;
        lap++;
        udp.begin(11111);
    }

    while (lap > 0) {
        if (udp.parsePacket() > 0)          //verifica se o módulo cliente está tentando enviar dados
        {
            req = "";
            while (udp.available() > 0)     //Enquanto houver dados a serem lidos, o canal de comunicação estará aberto
            {
                char z = udp.read();
                req += z;
            }

            //-------------------------------------------
            //Contabiliza a contagem do intervalo nos checkpoints remotos e envia ao dispositivo bluetooth
            
            if (req == "0") {
                tn = millis();
                dtn = tn - t0;
                BT.printf("Tp: %.2f\n", dtn / 1000.);
                Serial.printf("Tp: %.2f\n", dtn / 1000.);
            }
            //-------------------------------------------
            delay(1);
        }

        s0 = trigSens(digitalRead(D1));         //Acusa uma volta completa e envia ao BT
        if (s0) {
            dtt = millis() - t0;
            BT.printf("Tt: %.2f\n", dtt / 1000.);
            Serial.printf("Tt: %.2f\n", dtt / 1000.);
            lap++;
            delay(1);
            break;
        }

        if (BT.available() > 0) {               //Encerra a contagem de voltas pelo dispositivo bluetooth
            dados = BT.readString();
            if (dados[0] == '&') {
                lap = 0;
                delay(1);
                BT.println("parando...");
                Serial.println("parando...");
                break;
            }
        }
    }
}

//-------------------------------------------------
//Equivalente ao gatilho do módulo cliente
int i = 0;
bool trigSens(bool sign) {
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
