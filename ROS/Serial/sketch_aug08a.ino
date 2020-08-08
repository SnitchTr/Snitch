byte count = 0;
byte num[2]={0,0};
byte x[2];
void setup() {
  Serial.begin(9600);
}

void loop() {
  for (byte i = 0; i < 255; i++) {
    num[1] = i;
  Serial.write(num,2); // send a byte with the value 45
  delay(5);
  }
 count = count +1;
 num[0] = count;
}
 
