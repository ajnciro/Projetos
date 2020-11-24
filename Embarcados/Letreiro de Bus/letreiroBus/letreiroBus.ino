/*
Este sketch tem a finalidade de imprimir textos com scroll em uma tela LCD (neste caso)
via bluetooth, de modo a facilitar o eventual trabalho de um motorista ao alterar o
itinerário do veículo.

--
Ciro
(ciro@mail.org)
*/

#include <SoftwareSerial.h>
SoftwareSerial SerialCriada(7, 8);       // RX, TX Adiciona novas portas de comunicação para o caso de se necessitar adquirir ou enviar dados pela porta padrão
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

String rea;

void piscaescreve( String str2)          //função que faz o scroll do texto no display
{
  int n = str2.length();

  String esp = "                ";       //caracteres de espaço a serem concatenados (Prepend) para gerar o scroll
  esp.concat(str2);
  str2 = esp;

  for (int k = 0; k < 8 + n; k++)
  {
    int j = 0;

    while (str2[j] != '\0')             // pula de duas em duas células o texto no display
    {
      str2[j] = str2[j + 2];
      j++;
    }
    str2[j - 1] = ' ';
    str2[j - 2] = ' ';                  // pula de duas em duas células o texto no display

    lcd.setCursor(0, 1);
    lcd.print(str2);
    delay(300);                         // um delay menor pode dificultar a impressão correta do texto
  }
}

void escrevetc( String str)
{
  String ctr;

  if (SerialCriada.available()) { 
    str = SerialCriada.readString();   //Adquire os dados pela porta conectada ao módulo BT

  }

  while (str[0] != ' ')                //marcador para interpretar o início de uma nova mensagem
  {
    if (str[0] != '+')                 //marcador para suprimir sinais booleanos de sucesso da conexão
      ctr = str;

    piscaescreve(ctr);

    if (SerialCriada.available()) {
      str = SerialCriada.readString();
    }
  }
}
//
void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  SerialCriada.begin(9600);
}

void loop()
{
  escrevetc(rea);
}
