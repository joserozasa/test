
void setServo(uint8_t n_servo, int angulo){
  int duty;
  if (n_servo == si_index){
    duty = map(angulo, 100, 0, posB_0, posB_180);
  }
  else{
    duty = map(angulo, 100, 0, posA_0, posA_180);
  }
  
  servos.setPWM(n_servo, 0, duty);
}


void servo_test(){

  Serial.println("Iniciando prueba de servos");
  char servo_prueba = '1';
  int new_position = int_listening();
  setServo(servo_prueba,new_position);
  setServo(sd_index,0);
  setServo(ii_index,0);
  setServo(id_index,0);
  delay(1500);
  setServo(si_index,100);
  setServo(sd_index,100);
  setServo(ii_index,100);
  setServo(id_index,100);
  delay(1500);
  setServo(si_index,50);
  setServo(sd_index,50);
  setServo(ii_index,50);
  setServo(id_index,50);
  delay(1500);

  
  
}

void servo_level(){
  servo_enable(true);
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

  Serial.println("Que servo se modificara??: ");
  Serial.println("x para terminar con la nivelacion     ");

  rele('2');

  int new_position;
  char incomingByte;
  uint8_t servo;
  while (incomingByte!='0'){
    
    char incomingByte = char_listening();
    if(incomingByte == 'x'){
      break;
    }
    Serial.print("Servo seleccionado: ");
    Serial.println(incomingByte);

    Serial.println("A que altura se movera (medio es 50, rango de 1 a 100): ");
    new_position = int_listening();
    Serial.print("La posicion del servo ");
    Serial.print(incomingByte);
    Serial.print(" ahora es ");
    Serial.println(new_position);

    if(incomingByte == '1'){
      sd_pos = new_position;
      new_position = 100 - new_position;
      servo = sd_index;
    }
    else if(incomingByte == '2'){
      id_pos = new_position;
      servo = id_index;
    }
    else if(incomingByte == '3'){
      ii_pos = new_position;
      new_position = 100 - new_position;
      servo = ii_index;
    }
    else if (incomingByte == '4'){
      si_pos = new_position;
      servo = si_index;
    }
    else{
      Serial.println("Servo mal seleccionado, volver a intentar...");
    }

    setServo(servo, new_position);

    print_position(sd_pos, id_pos, ii_pos, si_pos);
    
  }
  servo_enable(false);
  EEPROM.update(0,sd_pos);
  EEPROM.update(1,id_pos);
  EEPROM.update(2,ii_pos);
  EEPROM.update(3,si_pos);
  rele('0');
}

void servo_enable(bool en){
  if(en){
    digitalWrite(servo_enable_pin, LOW);
  }
  else{
    digitalWrite(servo_enable_pin, HIGH);
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
