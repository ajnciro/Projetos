#define nDentes 46                                 //Numero de dentes da coroa

int dt = 0;
long t1 = 0, t2 = 0;
byte x[2] = {0, 0}, y1[2] = {0, 0}, y2[2] = {0, 0}, y3[2] = {0, 0}, y4[2] = {0, 0};

float freq = 0, rpm = 0., T = 0., Pot = 0.;

void setup() {
  Serial.begin(57600);
  pinMode(A0, INPUT);                             //Sensor IR de obstáculo que detecta os dentes da coroa
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(6, OUTPUT);
}

void loop() {


  float v=0.;

  for(int n =0; n<10;n++)
  {
    v=v+(float)analogRead(A5);                     //Entrada analógica do sinal do torquímetro
  }
  float torque = (0.2084) * (v/10.);              //substitui pelos coeficientes da regressão linear de calibração


  bool r1 = 0, r2 = 0, r3 = 0, r4 = 0;
  bool p1 = digitalRead(A1), p2 = digitalRead(A2), 
  p3 = digitalRead(A3), p4 = digitalRead(A4);     //Sensores IR de proximidade para a posição do pedivela


 //---------------------------------------------------------
 //Condições para disparo pontual de cronômetro, anulando efeito de corpo extenso, para cada um dos sensores p descritos acima
 
  if (p1 == LOW && (y1[0] == 0 && y1[1] == 0))
    r1 = 0;
  if (p1 == HIGH && (y1[0] == 0 && y1[1] == 0))
  {
    y1[1] = 1;
    r1 = 1;
  }
  if (p1 == HIGH && (y1[0] == 0 && y1[1] == 1))
  {
    y1[0] = 1;
  }
  if (p1 == LOW && (y1[0] == 1 && y1[1] == 1))
  {
    y1[1] = 0;
    y1[0] = 0;
  }

  //---------------------
  if (p2 == LOW && (y2[0] == 0 && y2[1] == 0))
    r2 = 0;
  if (p2 == HIGH && (y2[0] == 0 && y2[1] == 0))
  {
    y2[1] = 1;
    r2 = 1;
  }
  if (p2 == HIGH && (y2[0] == 0 && y2[1] == 1))
  {
    y2[0] = 1;
  }
  if (p2 == LOW && (y2[0] == 1 && y2[1] == 1))
  {
    y2[1] = 0;
    y2[0] = 0;
  }

  //---------------------
  if (p3 == LOW && (y3[0] == 0 && y3[1] == 0))
    r3 = 0;
  if (p3 == HIGH && (y3[0] == 0 && y3[1] == 0))
  {
    y3[1] = 1;
    r3 = 1;
  }
  if (p3 == HIGH && (y3[0] == 0 && y3[1] == 1))
  {
    y3[0] = 1;
  }
  if (p3 == LOW && (y3[0] == 1 && y3[1] == 1))
  {
    y3[1] = 0;
    y3[0] = 0;
  }

  //---------------------
  if (p4 == LOW && (y4[0] == 0 && y4[1] == 0))
    r4 = 0;
  if (p4 == HIGH && (y4[0] == 0 && y4[1] == 0))
  {
    y4[1] = 1;
    r4 = 1;
  }
  if (p4 == HIGH && (y4[0] == 0 && y4[1] == 1))
  {
    y4[0] = 1;
  }
  if (p4 == LOW && (y4[0] == 1 && y4[1] == 1))
  {
    y4[1] = 0;
    y4[0] = 0;
  }

  //---------------------------------------------------------
  //Condições para disparo pontual de cronômetro, anulando efeito de corpo extenso, para o sensor da coroa
  if (digitalRead(A0) == LOW && x[0] == 0 && x[1] == 0)
  {
    x[1] = 1;
    t1 = millis();
  }

  if (digitalRead(A0) == HIGH && x[0] == 0 && x[1] == 1)
    x[0] = 1;

  if (digitalRead(A0) == LOW && x[0] == 1 && x[1] == 1)
  {
    x[1] = 0;
    t2 = millis();
    dt = (t2 - t1);
  }

  if (digitalRead(A0) == HIGH && x[0] == 1 && x[1] == 0)
    x[0] = 0;
  //---------------------------------
 T = ((dt / 1000.) * nDentes);                          // periodo dt é o tempo em milisegundos entre dois dentes
//T = ((dt / 1000.) * nDentes);
  if (dt > 0) {
    freq = (2 * 3.1415 / T);                            // velocidade angular
    rpm = 60./ T ;                                      // rotação = 60 *f
    Pot = torque * freq;                                //Potência da pedalada
  }

//Imprime os dados coletados a cada posição estabelecida
  if ((dt > 0) && r1)
  {
    Serial.print("POSICAO\t|\tRPM\t|\tPOTENCIA (W)\t|\tTORQUE (N.m)\t|\tTEMPO (s)\n");
    Serial.print("DI"); Serial.print("\t|\t"); Serial.print(2.2*rpm, 3); Serial.print("\t|\t"); Serial.print(Pot, 3); Serial.print("\t\t|\t"); Serial.print(torque/2.2, 3); Serial.print("\t\t|\t");Serial.print(t2/1000.,3);Serial.print("\n\n");
  }

  if ((dt > 0) && r2)
  {
    Serial.print("POSICAO\t|\tRPM\t|\tPOTENCIA (W)\t|\tTORQUE (N.m)\t|\tTEMPO (s)\n");
    Serial.print("DP"); Serial.print("\t|\t"); Serial.print(2.2*rpm, 3); Serial.print("\t|\t"); Serial.print(Pot, 3); Serial.print("\t\t|\t"); Serial.print(torque/2.2, 3); Serial.print("\t\t|\t");Serial.print(t2/1000.,3);Serial.print("\n\n");
  }
  if ((dt > 0) && r3)
  {
    Serial.print("POSICAO\t|\tRPM\t|\tPOTENCIA (W)\t|\tTORQUE (N.m)\t|\tTEMPO (s)\n");
    Serial.print("EI"); Serial.print("\t|\t"); Serial.print(2.2*rpm, 3); Serial.print("\t|\t"); Serial.print(Pot, 3); Serial.print("\t\t|\t"); Serial.print(torque/2.2, 3); Serial.print("\t\t|\t");Serial.print(t2/1000.,3);Serial.print("\n\n");
  }
  if ((dt > 0) && r4)
  {
    Serial.print("POSICAO\t|\tRPM\t|\tPOTENCIA (W)\t|\tTORQUE (N.m)\t|\tTEMPO (s)\n");
    Serial.print("EP"); Serial.print("\t|\t"); Serial.print(2.2*rpm, 3); Serial.print("\t|\t"); Serial.print(Pot, 3); Serial.print("\t\t|\t"); Serial.print(torque/2.2, 3); Serial.print("\t\t|\t");Serial.print(t2/1000.,3);Serial.print("\n\n");
  }

  if ((rpm >28 || rpm < 25))                            //led para acusar ritmo da pedalada
    analogWrite(6, 200);
  else
    analogWrite(6, 0);
}
