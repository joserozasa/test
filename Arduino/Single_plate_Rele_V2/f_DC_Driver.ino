

void light_on(){
  Serial.println("Light ON");
  rele('1');
}

void light_off(){
  rele('0');
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
