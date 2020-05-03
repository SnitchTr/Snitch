#include <Servo.h>
const int trig = 10;
const int echo = 11;
const int pwmleftmotorpin = 9;
const int pleftmotorpin = 13;
const int nleftmotorpin = 12;
const int pwmrightmotorpin = 3;
const int prightmotorpin = 8;
const int nrightmotorpin = 7;
const int angvar = 1;
int distance;
int distance_front;
int distance_left;
int distance_right;
int posx = 0;
int posy = 0;
// Declaramos la variable para controlar el servo
Servo servo;
 
void setup() {

  servo.attach(6);
  Serial.begin(9600);

}
 
void loop() {
for(int i = 0;i<180;){
  distance = llegir_distancia();
  servo.write(i);
Serial.print("D");
Serial.print(distance);
Serial.print("A");
Serial.print(i);
Serial.print("X");
Serial.print(posx);
Serial.print("Y");
Serial.println(posy);
i = i+angvar;
}
Serial.print("done");
for(int i=180;i>0;){
   distance = llegir_distancia();
  servo.write(i);
  Serial.print("D");
Serial.print(distance);
Serial.print("A");
Serial.print(i);
Serial.print("X");
Serial.print(posx);
Serial.print("Y");
Serial.print(posy);
Serial.println(" ");
i = i-angvar;
}
}
int llegir_distancia() {
   long duration, distanceCm;
   
   digitalWrite(trig, LOW);  //para generar un pulso limpio ponemos a LOW 4us
   delayMicroseconds(4);
   digitalWrite(trig, HIGH);  //generamos Trigger (disparo) de 10us
   delayMicroseconds(10);
   digitalWrite(trig, LOW);
   
   duration = pulseIn(echo, HIGH);  //medimos el tiempo entre pulsos, en microsegundos
   
   distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm
   return distanceCm;
}
void leftmotor_foward(int i){
analogWrite(pwmleftmotorpin, i);
digitalWrite(pleftmotorpin, HIGH);
digitalWrite(nleftmotorpin, LOW);
}
void rightmotor_foward(int i){
analogWrite(pwmrightmotorpin, i);
digitalWrite(prightmotorpin, HIGH);
digitalWrite(nrightmotorpin, LOW);
}
void leftmotor_back(int i){
  analogWrite(pwmleftmotorpin, i);
digitalWrite(pleftmotorpin, LOW);
digitalWrite(nleftmotorpin, HIGH);
}
void rightmotor_back(int i){
  analogWrite(pwmrightmotorpin, i);
digitalWrite(prightmotorpin, LOW);
digitalWrite(nrightmotorpin, HIGH);
}
void leftmotor_stop(){
  digitalWrite(pleftmotorpin, LOW);
digitalWrite(nleftmotorpin, LOW);
}
void rightmotor_stop(){
  digitalWrite(prightmotorpin, LOW);
digitalWrite(nrightmotorpin, LOW);
}
