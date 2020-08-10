#define SYS_FREQ 1000 // in MHz
#define SET_PROFILE_TEST_LENGTH 72
#define SET_CFR1_TEST 40
#define SET_CFR2_TEST 40
#define SET_CFR3_TEST 40

int SCLK = 2;
int SDIO = 4;
int CSB = 3;
int IO_UPDATE = 5;

void setup() {
  Serial.begin(9600);
  pinMode(SCLK,OUTPUT);
  pinMode(SDIO,OUTPUT);
  pinMode(CSB,OUTPUT);
  pinMode(IO_UPDATE,OUTPUT);
  Serial.println("Tx Start");

}

void set_profile_TEST(){  // set frequency 50Mhz, phase 0, amplitude 1.0
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);

  Serial.println("start Transfer of set_profile_TEST");
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  delay(1000);
  int sdio_set_profile_TEST[SET_PROFILE_TEST_LENGTH] = {
    0,0,0,0,1,1,1,0, 
    0,0,1,1,1,1,1,1, 
    1,1,1,1,1,1,1,1, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,1,1,0,0, 
    1,1,0,0,1,1,0,0, 
    1,1,0,0,1,1,0,0, 
    1,1,0,0,1,1,0,0
  };

  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, LOW);
  digitalWrite(SDIO, sdio_set_profile_TEST[0]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  for(int i = 1 ; i < SET_PROFILE_TEST_LENGTH - 1; i++){
    delayMicroseconds(100);
    digitalWrite(SCLK,0);
    delayMicroseconds(50);
    digitalWrite(SDIO, sdio_set_profile_TEST[i]);
    delayMicroseconds(50);
    digitalWrite(SCLK,1);
    
    }
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(SDIO, sdio_set_profile_TEST[SET_PROFILE_TEST_LENGTH - 1]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, 1);
}

void set_cfr1(){
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);

  Serial.println("start Transfer of set_cfr1");
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  delay(1000);
  int sdio_set_cfr1[SET_CFR1_TEST] = {
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,1, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0
  };

  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, LOW);
  digitalWrite(SDIO, sdio_set_cfr1[0]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  for(int i = 1 ; i < SET_CFR1_TEST - 1; i++){
    delayMicroseconds(100);
    digitalWrite(SCLK,0);
    delayMicroseconds(50);
    digitalWrite(SDIO, sdio_set_cfr1[i]);
    delayMicroseconds(50);
    digitalWrite(SCLK,1);
    
    }
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(SDIO, sdio_set_cfr1[SET_CFR1_TEST - 1]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, 1);
}

void set_cfr2(){
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);

  Serial.println("start Transfer of set_cfr2");
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  delay(1000);
  int sdio_set_cfr2[SET_CFR2_TEST] = {
    0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,1,
    0,0,0,0,0,0,0,0, 
    0,0,1,0,0,0,0,0
  };

  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, LOW);
  digitalWrite(SDIO, sdio_set_cfr2[0]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  for(int i = 1 ; i < SET_CFR2_TEST - 1; i++){
    delayMicroseconds(100);
    digitalWrite(SCLK,0);
    delayMicroseconds(50);
    digitalWrite(SDIO, sdio_set_cfr2[i]);
    delayMicroseconds(50);
    digitalWrite(SCLK,1);
    
    }
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(SDIO, sdio_set_cfr2[SET_CFR2_TEST - 1]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, 1);
}

void set_cfr3(){
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);

  Serial.println("start Transfer of set_cfr2");
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  delay(1000);
  int sdio_set_cfr3[SET_CFR3_TEST] = {
    0,0,0,0,0,0,1,0, 
    0,0,0,0,1,0,0,0, 
    0,0,0,0,0,1,1,1, 
    1,1,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0
  };

  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(100);
  digitalWrite(SCLK,1);
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, LOW);
  digitalWrite(SDIO, sdio_set_cfr3[0]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  for(int i = 1 ; i < SET_CFR3_TEST - 1; i++){
    delayMicroseconds(100);
    digitalWrite(SCLK,0);
    delayMicroseconds(50);
    digitalWrite(SDIO, sdio_set_cfr3[i]);
    delayMicroseconds(50);
    digitalWrite(SCLK,1);
    
    }
  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(SDIO, sdio_set_cfr3[SET_CFR3_TEST - 1]);
  delayMicroseconds(50);
  digitalWrite(SCLK,1);

  delayMicroseconds(100);
  digitalWrite(SCLK,0);
  delayMicroseconds(50);
  digitalWrite(CSB, 1);
}

void io_update(){
  delay(100);
  digitalWrite(IO_UPDATE, 1);
  delay(10);
  digitalWrite(IO_UPDATE, 0);
  delay(100);
}

/*
void set_profile(frequency, phase, amplitude){ // frequency in MHz
  
}
*/

void loop() {
  int go = 0;
  int re = 0;
  int select = 0;
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  Serial.println("start?");
  while( go != '1'){
    go = Serial.read();
  }
  if(go == '1'){
    Serial.println(">> select function");
    Serial.println(">> [1] set_profile");
    Serial.println(">> [2] set CFR1");
    Serial.println(">> [3] set CFR2");
    Serial.println(">> [4] set CFR3");
    Serial.println(">> [5] IO UPDATE");
    while(select != '1' && select != '2' && select != '3' && select != '4' && select != '5'){
      select = Serial.read();
    }
    switch(select){
      case '1':
        Serial.println("set_profile");
        set_profile_TEST();
        break;
      case '2':
        Serial.println("set CFR1");
        set_cfr1();
        break;
      case '3':
        Serial.println("set CFR2");
        set_cfr2();
        break;
      case '4':
        Serial.println("set CFR3");
        set_cfr3();
        break;
      case '5':
        Serial.println("IO UPDATE");
        io_update();
        break;
      default:
        Serial.println("Error Input");
        break;
      }
    Serial.println("Restart?");
    while(re != '1'){
      re = Serial.read();
    }
    re = 0;
  }
  go = 0;
  select = 0;
}
