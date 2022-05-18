

//Con LOW se abern las valvulas

void valve_test(){
  Serial.println("Comenzando testeo de valvulas");
  valve('1');
  Serial.println("1 abierta, 2 cerrada");
  delay(5000);
  valve('2');
  Serial.println("1 cerrada, 2 abierta");
  delay(5000);
  valve('0');
  Serial.println("Valculas cerradas, fin testeo");
}

void valve(int n_valve){
  if (n_valve == '1'){
    digitalWrite(relay1,LOW);
    digitalWrite(relay2,HIGH);
  }
  else if (n_valve == '2'){
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,LOW);
  }
  else if (n_valve == '0'){
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,HIGH);
  }
  else{
    Serial.println("Mala seleccion de valvula");
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,HIGH);
  }
}


void update_valve(){
  if (next_valve == 1){
    next_valve = 2;
  }
  else if (next_valve = 2){
    next_valve = 1;
  }
}
