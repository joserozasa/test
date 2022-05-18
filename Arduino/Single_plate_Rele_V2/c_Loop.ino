
void loop(){
  display();
  char incomingByte = char_listening();
  Serial.println(incomingByte);
  if (incomingByte == 'a') {a();} //Bajar a profundidad "a" y volver. Activar bomba y valvulas
  if (incomingByte == 'b') {b();} //Bajar a profundidad "a" y volver. Activar bomba y valvulas
  if (incomingByte == 'c') {c();} //Bajar a profundidad "a" y volver. Activar bomba y valvulas
  if (incomingByte == 'u') {carrete_up(0);run_motors();} // Subir carrete
  if (incomingByte == 'd') {carrete_down(0);run_motors();} // Bajar carrete
  if (incomingByte == 'p') {pump(0);run_motors();} // Bombea agua hacia las placas
  if (incomingByte == 'q') {q();} //Sirve programaticamente para el reconocimiento del arduino
  if (incomingByte == 'n') {light_on();}
  if (incomingByte == 'm') {light_off();}
  if (incomingByte == 'e') {get_current();}
  if (incomingByte == 'x') {print_current();}
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

void a(){
  //next_valve = char_listening();
  carrete_down(m_1);
  pump(water_renovation);
  carrete_up(m_1);
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
  
}

void b(){
  //next_valve = char_listening();
  carrete_down(m_5);
  pump(water_renovation);
  carrete_up(m_5);
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
  
}

void c(){
  //next_valve = char_listening();
  carrete_down(m_10);
  pump(water_renovation);
  carrete_up(m_10);
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
   
  }
  


void display(){
  Serial.println("");
  Serial.println("Iniciando control arduino_calibracion...");
  Serial.println("");
  Serial.println("Opciones: ");
  Serial.println("a: Comenzar muestreo profundidad 1 m.");
  Serial.println("b: Comenzar muestreo profundidad 5 m");
  Serial.println("c: Comenzar muestreo profundidad 10 m");
  Serial.println("u: Subir sonda");
  Serial.println("d: Bajar sonda");
  Serial.println("p: Bombear agua");
  Serial.println("n: Prender LED");
  Serial.println("m: Apagar LED");
  Serial.println("x: imprimir corriente sensor");
  Serial.println("--------------------------------------------------------------------------");
}



void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }
