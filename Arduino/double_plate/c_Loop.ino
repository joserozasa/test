
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
  //if (incomingByte == 's') {stir();} // Proceso para limpiar placa placas
  if (incomingByte == 'q') {q();} //Sirve programaticamente para el reconocimiento del arduino
  if (incomingByte == 'o') {prender_ventilador();} // Sube xxx la plataforma para enfocar
  if (incomingByte == 'f') {apagar_ventilador();} // Baja xxx la plataforma para enfocar
  if (incomingByte == 'l') {change_light();} // Baja xxx la plataforma para enfocar
  if (incomingByte == 'v') {valve_test();}
  if (incomingByte == 'n') {set_light(250);}
  if (incomingByte == 'm') {set_light(0);}
    
}


char char_listening(){
  char answer;
  bool incoming_byte = false;; //TODO cambiar por funcion listening
  while(!incoming_byte){
    if (Serial.available() > 0) {
      incoming_byte = true;
      }
    }
  answer = Serial.read();
  return answer;
}

void a(){
  next_valve = char_listening();
  prender_ventilador();
  carrete_down(m_1);
  valve(next_valve);
  pump(water_renovation);
  valve('0');//Cerrando las valvulas
  carrete_up(m_1);
  apagar_ventilador();
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
  
}

void b(){
  next_valve = char_listening();
  prender_ventilador();
  carrete_down(m_5);
  valve(next_valve);
  pump(water_renovation);
  valve('0');//Cerrando las valvulas
  carrete_up(m_5);
  apagar_ventilador();  
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
  
}

void c(){
  next_valve = char_listening();
  prender_ventilador();
  carrete_down(m_10);
  valve(next_valve);
  pump(water_renovation);
  valve('0');//Cerrando las valvulas
  carrete_up(m_10);
  apagar_ventilador();  
  Serial.println("ready");//Este mensaje permite al programa comenzar la lectura, aquí comienza sin esperar la subida del carrete
   
  }
  


void display(){
  Serial.println("");
  Serial.println("Iniciando control arduino_calibracion...");
  Serial.println("");
  Serial.println("Opciones: ");
  Serial.println("a: Comenzar muestreo profundidad 1 m.");
  Serial.println("b: Comenzar muestreo profundidad 5 m.(no implementado)");
  Serial.println("c: Comenzar muestreo profundidad 10 m.(no implementado)");
  Serial.println("u: Subir sonda");
  Serial.println("d: Bajar sonda");
  Serial.println("p: Activar bomba");
  Serial.println("s: Limpiar placa");
  Serial.println("o: Activar ventilador");
  Serial.println("f: Desctivar ventilador");
  Serial.println("l: Control de iluminación");
  Serial.println("v: Prueba de valvulas");
  Serial.println("--------------------------------------------------------------------------");
}


void types(String a) { Serial.println("it's a String"); }
void types(int a) { Serial.println("it's an int"); }
void types(char *a) { Serial.println("it's a char*"); }
void types(float a) { Serial.println("it's a float"); }
void types(bool a) { Serial.println("it's a bool"); }
