
//Librerias
#include <AccelStepper.h>

//-----------------------General-------------------------
char incomingByte;

//-----------------------Steppers------------------------
#define EN 8
//-------Carrete--Eje Y

#define c_DIR 6   /* Pin de dirección para el eje carrete */
#define c_STEP 3  /* Pin de pasos para el eje carrete */
AccelStepper c_stepper(AccelStepper::DRIVER, c_STEP, c_DIR);


long cc = -100; //100 para operacion noraml, 1 para debug

long m_1 = 74 * cc;//TODO Debe quedar definido el metro, luego en las funciones a,b,c se multiplica por este valor
long m_5 = 380 * cc;
long m_10 = 860 * cc;

int ponderador = 9700; //lo borre para bajar memoria, creo que este yta no se usa

int c_speed = 600;
int c_max_speed = 600;



//-------Bomba--Eje X

#define b_DIR 5   /* Pin de dirección para el eje bomba */
#define b_STEP 2  /* Pin de pasos para el eje bomba */
AccelStepper b_stepper(AccelStepper::DRIVER, b_STEP, b_DIR);

long water_renovation = 65000; //65.000 para renovacion real, 650 para pruebas

int b_speed = 500;
int b_max_speed = 700;



//-----------------------DC------------------------

int IN1 = 11; //Z End Stop (M1)
int IN2 = 12; //Spin Enable (M1)
int ENA = 10; //Y End Stop (M1)
int IN3 = 13; //SpinDir (M2)
int IN4 = A3; //Coolant (M2)
int ENB = 9; //X End Stop (M2)




//-------------------Valve-------------------------
int relay1 = 7;
int relay2 = 4;

int next_valve = 1; //ultima valvula (->placa) en ser renovada
