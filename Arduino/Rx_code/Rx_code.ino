int SCLK = 2;
int SDIO = 4;
int CSB = 3;
int IO_UPDATE = 5;

void setup() {
  Serial.begin(9600);
  pinMode(SCLK,INPUT);
  pinMode(SDIO,INPUT);
  pinMode(CSB,INPUT_PULLUP);
  pinMode(IO_UPDATE,INPUT);
  Serial.println("Rx Start");
  attachInterrupt(digitalPinToInterrupt(CSB), csb_change, CHANGE);
  attachInterrupt(digitalPinToInterrupt(SCLK), sclk_change, CHANGE);
}

volatile int csb_state = 1;
volatile int sclk_state = 0;
volatile int sdio_value[10] = {0};
volatile int i = 0;

void csb_change(){
  csb_state = digitalRead(CSB);
  if(!csb_state) Serial.println("CSBDOWN");
  else Serial.println("CSBUP");
  }

void sclk_change(){
  sclk_state = digitalRead(SCLK);
  if(!sclk_state) Serial.println("SCLKDOWN");
  else{ 
    Serial.println("SCLKUP");
    if(csb_state == 0){
      sdio_value[i] = digitalRead(SDIO);
      Serial.println(i);
      i++;
    }
  }
}

void loop() {
  char ch = 0;
  
  
  while( csb_state == 0 ){
    if(csb_state == 1) break;
  }
  if( i != 0){
    Serial.println("show?");
    while(ch != '1'){
      ch = Serial.read();
    }
    ch = 0;
    for( int j = 0; j < 10;j++){
      Serial.println(sdio_value[j]);
    }

    i = 0;
  }
}
