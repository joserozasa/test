
void setup() 
{                
  /* Initialize serial */
  Serial.begin(115200); 

  //-----------------------Steppers------------------------
  pinMode(EN, OUTPUT); 
    
  c_stepper.setMaxSpeed(c_max_speed);
  c_stepper.setSpeed(c_speed);

  b_stepper.setMaxSpeed(b_max_speed);
  b_stepper.setSpeed(b_speed);

  enable_steppers("no");

  //-----------------------DC------------------------
   pinMode (ENB, OUTPUT); 
   pinMode (IN3, OUTPUT);
   pinMode (IN4, OUTPUT);
   pinMode (ENA, OUTPUT); 
   pinMode (IN1, OUTPUT);
   pinMode (IN2, OUTPUT);

   //----------------------Valve---------------------
   pinMode(relay1,OUTPUT);
   pinMode(relay2,OUTPUT);
   valve('0');



  
    
}

void q(){
  Serial.println("nano");
}

// Funcion que permanece escuchando a que llegue otro comando serial void listening(){} con output el char recibido
