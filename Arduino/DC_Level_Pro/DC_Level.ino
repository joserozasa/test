#include <Adafruit_MotorShield.h>
#include <EEPROM.h> 


Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *Motor4 = AFMS.getMotor(1);
Adafruit_DCMotor *Motor1 = AFMS.getMotor(2);
Adafruit_DCMotor *Motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *Motor2 = AFMS.getMotor(4);

int motor_speed = 180;
int ponderador_distancia = 500;




void setup(){
  Serial.begin(115200);

  if (!AFMS.begin()) {         // create with the default frequency 1.6KHz
  // if (!AFMS.begin(1000)) {  // OR with a different frequency, say 1KHz
    Serial.println("Could not find Motor Shield. Check wiring.");
    while (1);
  }
  Serial.println("Comenzando control nivelacion");        
           Motor1->run(RELEASE);    
           Motor2->run(RELEASE);    
           Motor3->run(RELEASE);    
           Motor4->run(RELEASE);     
           Motor1->setSpeed(motor_speed);
           Motor2->setSpeed(motor_speed);
           Motor3->setSpeed(motor_speed);
           Motor4->setSpeed(motor_speed);
   }

void loop(){   
  display();
  char incomingByte = char_listening();
  Serial.println(incomingByte);
  if (incomingByte == 'c') {calibrar();}
  if (incomingByte == 's') {subir_placa();}
  if (incomingByte == 'b') {bajar_placa();}
  if (incomingByte == 'i') {set();}

}


void calibrar(){
  int sd_pos;
  int si_pos;
  int id_pos;
  int ii_pos;

  sd_pos = EEPROM.read(0);
  si_pos = EEPROM.read(1);
  id_pos = EEPROM.read(2);
  ii_pos = EEPROM.read(3);

  Serial.println("Las posiciones anteriores son:");
  Serial.print("Servo 1: superior derecho = ");
  Serial.println(sd_pos);
  Serial.print("Servo 2: inferior derecho = ");
  Serial.println(id_pos);
  Serial.print("Servo 3: inferior izquierdo = ");
  Serial.println(ii_pos);
  Serial.print("Servo 4: superior izquierdo = ");
  Serial.println(si_pos);

  Serial.println("Que esquina se modificara??: ");
  Serial.println("x para terminar con la nivelacion     ");

  int new_position;
  char incomingByte;
  uint8_t esquina;
  while (incomingByte!='0'){
    
    char incomingByte = char_listening();
    if(incomingByte == 'x'){
      break;
    }
    Serial.print("Esquina seleccionado: ");
    Serial.println(incomingByte);

    Serial.println("A que altura se movera (medio es 50, rango de 1 a 100): ");
    new_position = int_listening();
    Serial.print("La posicion del servo ");
    Serial.print(incomingByte);
    Serial.print(" ahora es ");
    Serial.println(new_position);

    if(incomingByte == '1'){
      setEsquina('1', new_position, sd_pos);
      sd_pos = new_position;
    }
    else if(incomingByte == '2'){
      setEsquina('2', new_position, id_pos);
      id_pos = new_position;
    }
    else if(incomingByte == '3'){
      setEsquina('3', new_position, ii_pos);
      ii_pos = new_position;
    }
    else if (incomingByte == '4'){
      setEsquina('4', new_position, si_pos);
      si_pos = new_position;
    }
    else{
      Serial.println("Esquina mal seleccionada, volver a intentar...");
    }

    

    print_position(sd_pos, id_pos, ii_pos, si_pos);
    
  }
  EEPROM.update(0,sd_pos);
  EEPROM.update(1,id_pos);
  EEPROM.update(2,ii_pos);
  EEPROM.update(3,si_pos);
}


void setEsquina(uint8_t n_esquina, int new_position, int old_position){
  int dist = 0;
  if(n_esquina == '1'){
    if(new_position > old_position){
      dist = new_position - old_position;
      Motor1->run(FORWARD);   
      delay(dist*ponderador_distancia); 
      Motor1->run(RELEASE);   
    }
    else if(new_position < old_position){
      dist = old_position - new_position;
      Motor1->run(BACKWARD);   
      delay(dist*ponderador_distancia); 
      Motor1->run(RELEASE);        
    }
  }
  else if(n_esquina == '2'){
    if(new_position > old_position){
      dist = new_position - old_position;
      Motor2->run(FORWARD);   
      delay(dist*ponderador_distancia); 
      Motor2->run(RELEASE);   
    }
    else if(new_position < old_position){
      dist = old_position - new_position;
      Motor2->run(BACKWARD);   
      delay(dist*ponderador_distancia); 
      Motor2->run(RELEASE);        
    }
  }
  else if(n_esquina == '3'){
    if(new_position > old_position){
      dist = new_position - old_position;
      Motor3->run(FORWARD);   
      delay(dist*ponderador_distancia); 
      Motor3->run(RELEASE);   
    }
    else if(new_position < old_position){
      dist = old_position - new_position;
      Motor3->run(BACKWARD);   
      delay(dist*ponderador_distancia); 
      Motor3->run(RELEASE);        
    }
  }
  else if(n_esquina == '4'){
    if(new_position > old_position){
      dist = new_position - old_position;
      Motor4->run(FORWARD);   
      delay(dist*ponderador_distancia); 
      Motor4->run(RELEASE);   
    }
    else if(new_position < old_position){
      dist = old_position - new_position;
      Motor4->run(BACKWARD);   
      delay(dist*ponderador_distancia); 
      Motor4->run(RELEASE);        
    }
  }
}

char char_listening(){ 
  bool incoming_byte = false;
  while(!incoming_byte){
    if (Serial.available() > 0) {
      incoming_byte = true;
      }
    }
  char answer;
  answer = Serial.read();
  return answer;
  }

void subir_placa(){
  Serial.println("Que distancia subira la paca");
  int dist;
  dist = int_listening();
  Serial.print("Subiendo la placa: ");
  Serial.println(dist);
  Motor1->run(FORWARD);
  Motor2->run(FORWARD);
  Motor3->run(FORWARD);
  Motor4->run(FORWARD);
  delay(dist * ponderador_distancia);
  Motor1->run(RELEASE);
  Motor2->run(RELEASE);
  Motor3->run(RELEASE);
  Motor4->run(RELEASE);
  
  
}


void bajar_placa(){
  Serial.println("Que distancia subira la paca");
  int dist;
  dist = int_listening();
  Serial.print("Bajando la placa: ");
  Serial.println(dist);
  Motor1->run(BACKWARD);
  Motor2->run(BACKWARD);
  Motor3->run(BACKWARD);
  Motor4->run(BACKWARD);  
  delay(dist * ponderador_distancia);
  Motor1->run(RELEASE);
  Motor2->run(RELEASE);
  Motor3->run(RELEASE);
  Motor4->run(RELEASE);
}

void set(){
  Serial.println("Seteo inicial placa");
}

int int_listening(){
  String readString;
  bool incoming_int = false;
  while(!incoming_int){
    while (Serial.available()) {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the String readString
      delay(2);  //slow looping to allow buffer to fill with next character
    }
    
  
  if (readString.length() >0) {
    int n = readString.toInt();  //convert readString into a number
    incoming_int = true;
    return n;
  } 
  }
}

void print_position(int sd, int id, int ii, int si){
  Serial.print("4: ");
  Serial.print(si);
  Serial.print("         1: ");
  Serial.println(sd);
  Serial.println("");
  Serial.println("");
  Serial.print("3: ");
  Serial.print(ii);
  Serial.print("         2: ");
  Serial.println(id);
}

void display(){
  Serial.println("");
  Serial.println("Iniciando control nivelacion...");
  Serial.println("");
  Serial.println("Opciones: ");
  Serial.println("c: Calibracion por esquina");
  Serial.println("s: Subir placa completa");
  Serial.println("b: Bajar placa completa");
  Serial.println("Nivelacion inicial --> nivelar y salir del monitor serial antes de apretar 'x' ");
  Serial.println("--------------------------------------------------------------------------");
}
