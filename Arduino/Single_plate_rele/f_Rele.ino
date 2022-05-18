

//Con LOW se abern las valvulas

void rele_test(){
  Serial.println("Comenzando testeo de rele");
  rele('1');
  Serial.println("1 abierta, 2 cerrada");
  delay(2000);
  rele('2');
  Serial.println("1 cerrada, 2 abierta");
  delay(2000);
  rele('0');
  Serial.println("Valculas cerradas, fin testeo");
}

void rele(int n_rele){
  if (n_rele == '1'){
    digitalWrite(relay1,LOW);
    digitalWrite(relay2,HIGH);
  }
  else if (n_rele == '2'){
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,LOW);
  }
  else if (n_rele == '0'){
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,HIGH);
  }
  else{
    Serial.println("Mala seleccion de rele");
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,HIGH);
  }
}
//
//void update_valve(){
//  if(next_valve == 1){
//    next_valve = 2;
//  }
//  else if(next_valve == 2){
//    next_valve = 1;
//  }
//  }
