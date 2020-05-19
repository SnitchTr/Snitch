#include <Servo.h>
const int servopin = 6;
const int trig = 10;
const int echo = 11;
const int avar = 1;
const int maxdistance = 30000;
const int minangle = 0;
const int maxangle = 180;
const int baudrate = 9600;
const float speedofsound = 0.343;
int distance;
int posx = 0;
int posy = 0;
Servo servo;
 
void setup() {

  servo.attach(servopin);
  Serial.begin(baudrate);

}
void loop() {
  for(int angle = minangle;angle<maxangle;){
    servo.write(angle);
    distance = llegir_distancia();
    if(distance < maxdistance){
    Serial.print("D");
    Serial.print(distance);
    Serial.print("A");
    Serial.print(angle);
    Serial.print("X");
    Serial.print(posx);
    Serial.print("Y");
    Serial.println(posy);
    }
    angle = angle+ avar;
  }
  Serial.println("done");

}
float llegir_distancia() {
   int duration, distancemm;
   
   digitalWrite(trig, LOW);  
   delayMicroseconds(4);
   digitalWrite(trig, HIGH);  
   delayMicroseconds(10);
   digitalWrite(trig, LOW);
   
   duration = pulseIn(echo, HIGH);  
   
   distancemm = duration * speedofsound;  
   return distancemm;
}
