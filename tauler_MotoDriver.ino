
//encara s'han d'acabar de mirar els PINs del motor driver
//valors de velocitat entra 0 i 225

// Sonic
int trig = 9;
int echo = 8;

// Motor A
int ENA = 10;
int IN1 = 11;
int IN2 = 12;

// Motor B
int ENB = 5;
int IN3 = 7;
int IN4 = 6;

int distancia = 10;
int dp = distancia - 2;
int dg = distancia + 2;
bool distancia_correcta = false;
bool massa_aprop = false;
bool dale = false;

int limit_nord = 5; // Alçada de 50 cm
int limit_sud = 0;
int limit_est = 7; // Amplada de 70 cm
int limit_oest = 0;

int recorregut = 0;

int posicio[2] = {0, 0}; //posicio inicial limit sud-oest (0,0) en mm 
                         // (eix x horitzontal oest-est, eix y vertical sud-nord)
int orientacio = 0; //orientacio inicial mirant a nord 
                    // 0 nord, 90 est, 180 sud, 270 oest, 360=0 = nord

void setup() {
  Serial.begin (9600);
//  setTime(17,00,00,2,5,2020);
  pinMode (trig, OUTPUT);
  pinMode (echo, INPUT);

// Declarem els pins com sortides
 pinMode (ENA, OUTPUT);
 pinMode (ENB, OUTPUT);
 pinMode (IN1, OUTPUT);
 pinMode (IN2, OUTPUT);
 pinMode (IN3, OUTPUT);
 pinMode (IN4, OUTPUT);
 
 digitalWrite (trig, LOW);
}

// ================================================== LOOP ====================

void loop() {

aturar ();

// Esperar a detectar objecte 20 cm per començar
  int cm = llegir_distancia (trig, echo);  
  
  Serial.println ("Espero a detectar senyal d'inici (objecte a 20 cm)...");
  
  while (not dale) {
    cm = llegir_distancia (trig,echo);
    if (cm == 20) {
      dale = true;} 
      
      Serial.print("Distancia: ");
      Serial.print(cm);
      Serial.print(" Dale?: ");
      Serial.println(dale);
      delay(100);
    }

// Fer perímetre

orientacio = 0;
posicio[0] = 0;
posicio[1] = 0;

Serial.println ("------ Anem al nord! -----");

recorregut = limit_nord - posicio [1];
avancar_cm(recorregut);
    
rotar (90);

Serial.println ("------ Anem a l'est! -----");

recorregut = limit_est - posicio [0];
avancar_cm(recorregut);
    
rotar (90);

Serial.println ("------ Anem al sud! -----");

recorregut = posicio [1] - limit_sud;
avancar_cm(recorregut);
    
rotar (90);

Serial.println ("------ Anem a l'oest! -----");

recorregut = posicio [0] - limit_oest;
avancar_cm(recorregut);
    
rotar (90);

Serial.println ("------ Fi de la volta! Esperem dale i tornem de començar -----");

dale = false;
delay(1000);
   
}


// ================================================== GIRAR ====================

void rotar (int angle) {
Serial.print ("Vaig a rotar : ");
Serial.println (angle);

if ((angle >= 360) || (angle <=-360) || (angle == 0)) {
  aturar ();
  Serial.print (angle);
  Serial.println ("ERR -> Angle de rotació demanat erroni"); 
  return;
}

if (angle <= -360) angle = 0; 

if (angle > 0) gira_dreta(200,100);
if (angle < 0) gira_esquerre(100,200);
if (angle == 0)  return;
  
int cicles = 1; 
  // De moment s'asigna a 10 per cada grau. 
  //Caldrà definir els cicles que es un 1 grau en funcio de la velocitat de gir

for (int j=0; j<angle ; j++){       // Per cada angle
  for (int i=0; i<=cicles; i++){    // Per cada cicle que cal esperar per fer un grau
    avancar ();                     // Deixar que el motor avanci
    } 
  orientacio++;
  }

aturar ();  
return;
}


// ================================================== AVANÇAR ====================

void avancar_cm (int cm) {
int cicles = 100; // De moment s'asigna a 100. Caldrà definir els cicles que es un 1cm en funcio de la velocitat

palante (100,100);

for (int j=1; j<=cm; j++) {          //Per cada cm
 for (int i=0; i<=cicles; i++){      //Per cada cicle que necessita per fer un cm
   avancar ();
   } 
   nova_posicio(); 
}
aturar ();  
}

void avancar () {  
  delay (10);
  //esperar a que el motor avanci
  }


// ================================================== POSICIO ====================

void nova_posicio () {
// en funcio de la orientació, calcula la nova posicio

Serial.print("Orientació: ");
Serial.print(posicio[0]);
Serial.print(" - Posicio inicial: x = ");
Serial.print(posicio[0]);
Serial.print(" y = ");
Serial.println(posicio[1]);


switch (orientacio) {
   case 0:
     // orientacio nord
     posicio[1]++;     
     break;
   case 180:
     // orientacio sud
     posicio[1]--;     
     break;
   case 90:
     {//  orientacio est
     posicio[0]++;
     }
     break;
   case 270:
     {//  orientacio oest
     posicio[0]--;
     }
     break;  
   default: 
     {// orientacio mal definida
     Serial.print(orientacio);
     Serial.println(" -> ERROR orientacio mal definida");
     }

}

Serial.print("Orientació: ");
Serial.print(posicio[0]);
Serial.print(" - Nova posicio (x,y) : (");
Serial.print(posicio[0]);
Serial.print(",");
Serial.print(posicio[1]);
Serial.println(")");

return;

}



// ================================================== ULTRASONIC ====================
 
int llegir_distancia(int trig, int echo) {
   long duration, distanceCm;
   
   digitalWrite(trig, LOW);  //per generar un pulso net ho posem a LOW 4us
   delayMicroseconds(4);
   digitalWrite(trig, HIGH);  //generem Trigger (disparo) de 10us
   delayMicroseconds(10);
   digitalWrite(trig, LOW);
   
   duration = pulseIn(echo, HIGH);  //medim el temps entre pulsos, en microsegons
   
   distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm
   return distanceCm;
}

// ================================================== ALTRES FUNCIONS ====================


bool entrevalors (int mesura, int valorbaix, int valoralt){
  if (mesura >= valorbaix && mesura <= valoralt){
    return true;}
  else {
  return false;}
  
  }


// ================================================== VELOCITAT MOTOR ====================

void palante(int velA, int velB) {
  
//Direccio motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, velA); //Velocidad motor A
 //Direccio motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, velB); //Velocidad motor B

  return;
}

void aturar(){
//Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 0); //Velocitat motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 0); //Velocitat motor B
 return;
}


void gira_dreta (int velA, int velB){
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, velA); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, velB); //Velocidad motor B
  return;
}

void gira_esquerre(int velA, int velB){
//Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, velA); //Velocitat motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, velB); //Velocitat motor B
 return;
}
