/*
Este sketch tem a finalidade de adquirir sinais de tensão não negativas limitadas a 5V
e escrevê-los na comunicação serial padrão, a fim de serem recebidos por um software
gerador de gráficos.

A aquisição de dados se inicia quando um caractere 'C' gatilho é recebido e lido através da
porta serial, e pode ser feita, por exemplo, por uma aplicação como Realterm ou similar.

É recomendado que o arquivo seja gerado com valores separados por tabulação (TSV), e o
diretório adequadamente modificado no notebook Mathematica do osciloscópio para leitura
adequada.


--
Ciro
(ciro@mail.org)
*/

float fanalog0;
int analog0;
byte serialByte;

void setup() 
{
   Serial.begin(9600);
   Serial.println("Oi, povo bonito!");
}

void loop() 
{
  while (Serial.available()>0){  
    serialByte=Serial.read();//Lê o caractere enviado
    if (serialByte=='C')//Se 'C', gatilho da captura
    {        
      while(1)
      {
        analog0=analogRead(0);//Leitura do pino A0
        fanalog0=(analog0)*(5./1023);//Resolução do canal analógico em Volts

        Serial.println(fanalog0,2);//Envio para simular lista de dados
        if (Serial.available()>0)
        {
          serialByte=Serial.read();
          if (serialByte=='F')  break;//Se 'F', fecha captura
        }
      }
    }
  }
}
