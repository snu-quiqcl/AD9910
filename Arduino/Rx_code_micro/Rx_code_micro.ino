#define MAX_RX_LENGTH 100

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
volatile int sdio_value[MAX_RX_LENGTH] = {0};
volatile int i = 0;

void csb_change(){
  csb_state = digitalRead(CSB);
  }

void sclk_change(){
  sclk_state = digitalRead(SCLK);
  if(sclk_state){ 
    if(csb_state == 0){
      sdio_value[i] = digitalRead(SDIO);
      i++;
    }
  }
}

void loop() {
  char ch = 0;
  //****let's delete this part when we check other part****
  int io_update = digitalRead(IO_UPDATE);
  unsigned long t1 = micros();
  while(io_update == 1){
    io_update = digitalRead(IO_UPDATE);
    if(io_update == 0){
      unsigned long t2 = micros();
      Serial.print("IO UPDATE DURATION : ");
      Serial.println(t2-t1);
    }
  }
  while( csb_state == 0 ){
    if(csb_state == 1) break;
  }
  if( i != 0 && csb_state != 0){
    Serial.println("show?");
    while(ch != '1'){
      ch = Serial.read();
    }
    ch = 0;
    Serial.print("Length : ");
    Serial.println(i);
    for( int j = 0; j < i;j++){
      Serial.println(sdio_value[j]);
      sdio_value[j] = 0;
    }

    i = 0;
  }
}
