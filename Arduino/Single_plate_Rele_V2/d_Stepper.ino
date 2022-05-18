



void carrete_down(long distance){
  if (distance == 0){
    Serial.println("Cuantos m quiere bajar la sonda?");
    char incomingByte = char_listening();
    distance = long(incomingByte-'0')*ponderador;
    Serial.print("Bajando sonda (cm): ");
    Serial.println(distance/100);
    }
  enable_steppers("yes");  
  c_stepper.moveTo(c_stepper.currentPosition()+distance);
  c_stepper.setSpeed(c_speed);
  run_motors();
}


void carrete_up(long distance){  
  if (distance == 0){
    Serial.println("Cuantos m quiere subir la sonda?");
    char incomingByte = char_listening();
    distance = long(incomingByte-'0')* ponderador;        
    Serial.println("Subiendo sonda (cm): ");
    Serial.println(distance/100);
    }
  enable_steppers("yes");
  c_stepper.moveTo(c_stepper.currentPosition()-distance);
  c_stepper.setSpeed(c_speed);
  run_motors();
}

void pump(long distance){
  if (distance == 0){
    Serial.println("Para bombear en direccon normal (n) o reverse (r): ");
    char incomingByte = char_listening();
    if (incomingByte == 'n'){
      Serial.println("Numero del 1 al 5, 5 es renovacion completa");
      char incomingByte = char_listening();
      distance = long(incomingByte-'0')*+water_renovation;
    }
    else if (incomingByte == 'r'){
      Serial.println("Cuantos metros bombear en direccion reversa?");
      char incomingByte = char_listening();
      distance = long(incomingByte-'0')*-water_renovation;
    }
  }
  
  enable_steppers("yes");  
  b_stepper.moveTo(b_stepper.currentPosition()- distance);
  b_stepper.setSpeed(b_speed);
  run_motors();
}



void enable_steppers(String en){
  if (en == "yes"){
    digitalWrite(EN, LOW); //Se activa con LOW
  }
  else {
    digitalWrite(EN, HIGH);
  }
}


void run_motors(){
  while (c_stepper.distanceToGo()!=0){
    c_stepper.runSpeedToPosition();
  }
  while (b_stepper.distanceToGo()!=0){
    b_stepper.runSpeedToPosition();
  }
  enable_steppers("no");
  
}
