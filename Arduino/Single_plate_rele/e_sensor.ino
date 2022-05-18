

boolean get_current(){
  float voltageSensor;
  float current=0;

  for (int i=0; i<1000; i++){
    voltageSensor = analogRead(current_pin) * (5.0/1023.0);
    current = current + abs((voltageSensor-2.5)/sensor_sensitivity);
    }
  current = current/1000;
  if(current>current_limit){
    Serial.println('1'); //Esta energizado
  }
  else{
    Serial.println('0');//Esta sin energia
  }
}

void print_current(){
  float voltageSensor;
  
  while(true){
    float current=0;
    for (int i=0; i<1000; i++){
    voltageSensor = analogRead(current_pin) * (5.0/1023.0);
    current = current + abs((voltageSensor-2.5)/sensor_sensitivity);
    }
    current = current/1000;
    Serial.println(current);  
    delay(200);
  }
  
}


 
