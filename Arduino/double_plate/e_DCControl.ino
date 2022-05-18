
char time_moving;
int time_moving_int;
int velocidad = 200;
int light_intensity;




void prender_ventilador(){
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite(ENA,254); //Velocidad a la que mueve la plataforma (entre 1 y 254)
 Serial.println("Ventilador encendido... ");
 }

void apagar_ventilador(){
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite(ENA,0);
 Serial.println("Ventilador apagado... ");
}



void change_light(){
  Serial.println("Modificar la intesnidad de la luz: 1 para intensidad baja, 2 para intensidad media, 3 para intensidad alta. 0 para apagar.");
  bool resp; //TODO cambiar por funcion listenting
  resp = false;
  while(!resp){
    if (Serial.available() > 0) {
      resp = true;
      }
    }
 light_intensity = Serial.read();
 if (light_intensity =='1'){
  Serial.println("Intensidad de luz baja");
  set_light(60); 
 }
 else if (light_intensity =='2'){
  Serial.println("Intensidad de luz media");
  set_light(80);
 }
 else if (light_intensity =='3'){
  Serial.println("Intensidad de luz alta");
  set_light(240);
 }
 else if (light_intensity =='0'){
  Serial.println("Luz apagada");
  set_light(0);
 }
 else{
  Serial.println("No existe la opcion, intentar nuevamente");
 }
}

void set_light(int intensity){
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  analogWrite(ENB,intensity); //intensidad (entre 1 y 254)
}


void z_endstop_reached(){
//TODO detiene el movimiento de nivelacion
//TODO indica que enstop se alcanzo
//TODO Impide que continue el movimiento en esa direccion. Una variable que diga cual toco, y que la funcion mover desactive cuando se mueva en otra direccion
}
