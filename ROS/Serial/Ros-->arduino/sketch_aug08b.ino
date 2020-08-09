
byte buffer[2];
int var;

void setup(){
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);

}

void loop(){
  Serial.readBytes(buffer, 2);
  var = to_int(buffer);
switch (var) {
  case 1:
      digitalWrite(LED_BUILTIN, HIGH);
    break;
  case 2:
      digitalWrite(LED_BUILTIN, LOW);
    break;
  default:
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);  
    break;
}
}
int to_int(byte x[2]){
  int val;
  val = x[0]*256+x[1];
  return val;
}
