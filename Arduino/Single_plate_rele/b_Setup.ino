
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

  //------------------------current sensor---------------
  pinMode(current_pin, INPUT);

//  //-----------------------DC------------------------
//   pinMode (ENB, OUTPUT); 
//   pinMode (IN3, OUTPUT);
//   pinMode (IN4, OUTPUT);
//   pinMode (ENA, OUTPUT); 
//   pinMode (IN1, OUTPUT);
//   pinMode (IN2, OUTPUT);

   //----------------------Valve---------------------
   pinMode(relay1,OUTPUT);
   pinMode(relay2,OUTPUT);
   rele('0');


  //--------------------Servos----------------------
  servos.begin();
  servos.setPWMFreq(50);  // Analog servos run at ~50 Hz updates
  digitalWrite(servo_enable_pin, HIGH);
  pinMode(servo_enable_pin, OUTPUT);
  
    
}

void q(){
  Serial.println("nano");
}
