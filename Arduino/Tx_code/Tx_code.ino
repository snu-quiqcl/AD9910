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

void loop() {
  int go = 0;
  int re = 0;
  digitalWrite(SDIO,0);
  digitalWrite(CSB,1);
  digitalWrite(IO_UPDATE,0);
  digitalWrite(SCLK,1);
  Serial.println("start?");
  while( go != '1'){
    go = Serial.read();
  }
  if(go == '1'){
    Serial.println("start Transfer");
    digitalWrite(SDIO,0);
    digitalWrite(CSB,1);
    digitalWrite(IO_UPDATE,0);
    digitalWrite(SCLK,1);
    delay(1000);
    int sdio_temp[10] = {1,1,0,0,0,1,0,1,1,0};
  
    digitalWrite(SCLK,0);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,1);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,0);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,1);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,0);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,1);
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,0);
    //delayMicroseconds(50);
    delay(100);
    digitalWrite(CSB, LOW);
    digitalWrite(SDIO, sdio_temp[0]);
    //delayMicroseconds(50);
    delay(100);
    digitalWrite(SCLK,1);
  
    for(int i = 1 ; i < 9; i++){
      //delayMicroseconds(100);
      delay(100);
      digitalWrite(SCLK,0);
      //delayMicroseconds(50);
      delay(100);
      digitalWrite(SDIO, sdio_temp[i]);
      //delayMicroseconds(50);
      delay(100);
      digitalWrite(SCLK,1);
      
      }
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,0);
    //delayMicroseconds(50);
    delay(100);
    digitalWrite(SDIO, sdio_temp[9]);
    //delayMicroseconds(50);
    delay(100);
    digitalWrite(SCLK,1);
  
    //delayMicroseconds(100);
    delay(100);
    digitalWrite(SCLK,0);
    //delayMicroseconds(50);
    delay(100);
    digitalWrite(CSB, 1);
  
    delay(100);
    digitalWrite(IO_UPDATE, 1);
    delay(1);
    digitalWrite(IO_UPDATE, 0);
    delay(100);
    Serial.println("Restart?");
    /*if(1){
      char ch = Serial.read();
      if( ch == '1'){
        Serial.println("Restart");
        }
      else{
        Serial.println("End");
        }
      }*/
    while(re != '1'){
      re = Serial.read();
    }
    re = 0;
  }
}
