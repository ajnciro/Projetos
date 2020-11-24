#include <SoftwareSerial.h>
SoftwareSerial SerialCriada(7, 8); // RX, TX          // Libera a comunicação serial caso queira adquirir dados por outro sensor através de USB

#include <Stepper.h>                                  //Inclui biblioteca para controle de motor de passo
const int stepsPerRevolution = 64;                    // motor de 64 pulsos por volta
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 6);   // inicializa a biblioteca utilizando as portas de 8 a 11 (6) para ligação do motor (precisei trocar a 11 por 6)


void setup()
{
  myStepper.setSpeed(350);                            //Determina a velocidade do motor
  Serial.begin(9600);
  SerialCriada.begin(9600);
}
String str, str2;
float pass = 0;

void loop()
{
  if (SerialCriada.available() > 0)
  {
    str2 = SerialCriada.readString();                 // Faz a leitura do sinal vindo via BT

    if (str2[0] != '+')
    {
      str = str2;
      pass = 2048 * (180 / 360.);                     //2048 é uma volta completa
    }
  }

  myStepper.step(pass);                               // Dá 1024/2048 volta no motor no sentido horário [ou (180/360)*2048 = 2048/2]

  delay(1000 * (str).toInt());
  myStepper.step(pass * (-1));                        //gira em sentido anti-horário. Pode também acrescentar uma linha de delay caso queira que ele espere antes de voltar
}
