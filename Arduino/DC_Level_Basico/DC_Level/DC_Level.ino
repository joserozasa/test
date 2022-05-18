#include <AFMotor.h>
#include <EEPROM.h> 


AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(4);
AF_DCMotor motor4(3);


byte dir_motor_1_for = 2;
byte dir_motor_1_back = 1;

byte dir_motor_2_for = 1;
byte dir_motor_2_back = 2;

byte dir_motor_3_for = 1;
byte dir_motor_3_back = 2;

byte dir_motor_4_for = 2;
byte dir_motor_4_back = 1;

int motor_speed = 180;
float ponderador_distancia = 400;
int desp_limite = 10;




void setup(){
  Serial.begin(115200);
  
  motor1.setSpeed(motor_speed);
  motor2.setSpeed(motor_speed);
  motor3.setSpeed(motor_speed);
  motor4.setSpeed(motor_speed);
 
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);

   }

void loop(){   
  display();
  char incomingByte = char_listening();
  Serial.println(incomingByte);
  if (incomingByte == 'c') {calibrar();}
  if (incomingByte == 's') {subir_placa();}
  if (incomingByte == 'b') {bajar_placa();}
  if (incomingByte == 'z') {set();}

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

  

//  Serial.println("Las posiciones anteriores son:");
//  Serial.print("Servo 1: superior derecho = ");
//  Serial.println(sd_pos);
//  Serial.print("Servo 2: inferior derecho = ");
//  Serial.println(id_pos);
//  Serial.print("Servo 3: inferior izquierdo = ");
//  Serial.println(ii_pos);
//  Serial.print("Servo 4: superior izquierdo = ");
//  Serial.println(si_pos);

  Serial.println("Seleccionar esquina y luego distancia objetivo (1 - 100, comenzando en 50)");
  Serial.println("x para terminar con la nivelacion     ");

  int new_position;
  char incomingByte;
  uint8_t esquina;
  while (incomingByte!='0'){
    
    print_position(sd_pos, id_pos, ii_pos, si_pos);
    
    incomingByte = char_listening();
    if(incomingByte == 'x'){
      break;
    }
    Serial.print("Esquina seleccionada -> ");
    Serial.print(incomingByte);
    new_position = int_listening();
    Serial.print(" para moverse a: ");
    Serial.println(new_position);
    Serial.print("Moviendo motor ");
    Serial.print(incomingByte);
    Serial.print(" a posicion ");
    Serial.println(new_position);
    Serial.println();


    if(incomingByte == '1'){
      if(abs(sd_pos - new_position) > desp_limite){
        restriccion();
      }
      else{
        setEsquina('1', new_position, sd_pos);
        sd_pos = new_position;
    }}
    else if(incomingByte == '2'){
      if(abs(id_pos - new_position) > desp_limite){
        restriccion();
      }
      else{
      setEsquina('2', new_position, id_pos);
      id_pos = new_position;
    }}
    else if(incomingByte == '3'){
      if(abs(ii_pos - new_position) > desp_limite){
        restriccion();
      }
      else{
      setEsquina('3', new_position, ii_pos);
      ii_pos = new_position;
    }}
    else if (incomingByte == '4'){
      if(abs(si_pos - new_position) > desp_limite){
        restriccion();
      }
      else{
      setEsquina('4', new_position, si_pos);
      si_pos = new_position;
    }}
    else{
      Serial.println("Esquina mal seleccionada, volver a intentar...");
    }
    
  }
  EEPROM.update(0,sd_pos);
  EEPROM.update(1,id_pos);
  EEPROM.update(2,ii_pos);
  EEPROM.update(3,si_pos);
}


void setEsquina(uint8_t n_esquina, int new_position, int old_position){
  float dist = abs(new_position - old_position);
  if(n_esquina == '1'){
    if(new_position > old_position){
      motor1.run(dir_motor_1_for);   //-----------------------------------------------------> forward es 1 y backward 2. 
      delay(dist*ponderador_distancia); 
      motor1.run(RELEASE);   
    }
    else if(new_position < old_position){
      motor1.run(dir_motor_1_back);   
      delay(dist*ponderador_distancia); 
      motor1.run(RELEASE);        
    }
  }
  else if(n_esquina == '2'){
    if(new_position > old_position){
      motor2.run(dir_motor_2_for);   
      delay(dist*ponderador_distancia); 
      motor2.run(RELEASE);   
    }
    else if(new_position < old_position){
      motor2.run(dir_motor_2_back);   
      delay(dist*ponderador_distancia); 
      motor2.run(RELEASE);        
    }
  }
  else if(n_esquina == '3'){
    if(new_position > old_position){
      motor3.run(dir_motor_3_for);   
      delay(dist*ponderador_distancia); 
      motor3.run(RELEASE);   
    }
    else if(new_position < old_position){
      motor3.run(dir_motor_3_back);   
      delay(dist*ponderador_distancia); 
      motor3.run(RELEASE);        
    }
  }
  else if(n_esquina == '4'){
    if(new_position > old_position){
      motor4.run(dir_motor_4_for);   
      delay(dist*ponderador_distancia); 
      motor4.run(RELEASE);   
    }
    else if(new_position < old_position){
      motor4.run(dir_motor_4_back);   
      delay(dist*ponderador_distancia); 
      motor4.run(RELEASE);        
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
  motor1.run(dir_motor_1_for);
  motor2.run(dir_motor_2_for);
  motor3.run(dir_motor_3_for);
  motor4.run(dir_motor_4_for);
  delay(dist * ponderador_distancia);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  
  
}


void bajar_placa(){
  Serial.println("Que distancia subira la paca");
  int dist;
  dist = int_listening();
  Serial.print("Bajando la placa: ");
  Serial.println(dist);
  motor1.run(dir_motor_1_back);
  motor2.run(dir_motor_2_back);
  motor3.run(dir_motor_3_back);
  motor4.run(dir_motor_4_back);  
  delay(dist * ponderador_distancia);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void set(){
  Serial.println("Seteo inicial placa");
  EEPROM.update(0,50);
  EEPROM.update(1,50);
  EEPROM.update(2,50);
  EEPROM.update(3,50);
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
void restriccion(){
  Serial.print("---------------< No se puede mover mas de ");
  Serial.print(desp_limite);
  Serial.println(" por seguridad>-----------------------");
  Serial.println();
}

void display(){
  Serial.println("");
  Serial.println("Iniciando control nivelacion...");
  Serial.println("");
  Serial.println("Opciones: ");
  Serial.println("c: Calibracion por esquina");
  Serial.println("s: Subir placa completa");
  Serial.println("b: Bajar placa completa");
  Serial.println("z: set 50 en todos los motores (solo hacerlo al inicio)");
  Serial.println("Nivelacion inicial --> nivelar y salir del monitor serial antes de apretar 'x' ");
  
  Serial.println("--------------------------------------------------------------------------");
}
