

byte DummyData1[] = "03 0C 05 0A 25 70 35 2A CB 0A 02 12 1C 5E 52 6F 1D 5C 66 15\n\r";
byte DummyData2[] = "0C 03 0D 0A 2A 72 3C 25 CA 2C A2 EF 1D 12 AC 62 1A 50 DF 4A\n\r";


byte HeaterDataON[] = "03";
byte HeaterDataOFF[] = "0C";

byte PumpDataON[] = "0C";
byte PumpDataOFF[] = "03";


byte TempData1[] = "05 0A";
byte TempData2[] = "25 70";
byte TempData3[] = "35 2A";
byte TempData4[] = "CB 0A";

byte PressureData1[] = "02 12";
byte PressureData2[] = "1C 5E";
byte PressureData3[] = "52 6F";
byte PressureData4[] = "1D 5C";

byte TempData5[] = "0D 0A";
byte TempData6[] = "2A 72";
byte TempData7[] = "3C 25";
byte TempData8[] = "CA 2C";

byte PressureData9[] =  "A2 EF";
byte PressureData10[] = "1D 12";
byte PressureData11[] = "AC 62";
byte PressureData12[] = "1A 50";




byte WeightScale1[] = "66";
byte WeightScale2[] = "DF";




int Temp1N = 200;
int Temp1W = 500;
int Temp1A = 800;

int Temp2N = 300;
int Temp2W = 600;
int Temp2A = 900;

int Press1N = 100;
int Press1W = 300;
int Press1A = 600;

int Press2N = 200;
int Press2W = 400;
int Press2A = 600;

int CurrStateTemp1 =0;
int PrevStateTemp1 =0;

int CurrStateTemp2 =0;
int PrevStateTemp2 =0;


int CurrStatePress1 =0;
int PrevStatePress1 =0;


int CurrStatePress2 =0;
int PrevStatePress2 =0;




int checkTemp1Lmts(int);
int checkTemp2Lmts(int);
int checkPress1Lmts(int);
int checkPress2Lmts(int);

void sendTemp1Mess(int);
void sendTemp2Mess(int);
void sendPress1Mess(int);
void sendPress2Mess(int);




void sendTemp1Mess(int Temp1DState)
{
  
  CurrStateTemp1 = Temp1DState;

  if(CurrStateTemp1 != PrevStateTemp1)
  {
    if(!Serial.available())
      {        
        Serial.print("Temp1State = ");
        switch (CurrStateTemp1)
        {            
          case 1:
            Serial.print("Normal");break; 
          case 2:
            Serial.print("Warning");break;  
          case 3:
            Serial.print("Action");break;           
         }
          
         Serial.print('\n');
         Serial.print('\r');        
     
        PrevStateTemp1 = CurrStateTemp1; 
      }      
  }
  PrevStateTemp1 = CurrStateTemp1;  
  
}


void sendTemp2Mess(int Temp2DState)
{  
  CurrStateTemp2 = Temp2DState;
  if(CurrStateTemp2 != PrevStateTemp2)
  {
    if(!Serial.available())
      {        
        Serial.print("Temp2State = ");
        switch (CurrStateTemp2)
        {            
          case 1:
            Serial.print("Normal");break; 
          case 2:
            Serial.print("Warning");break;  
          case 3:
            Serial.print("Action");break;           
         }
          
         Serial.print('\n');
         Serial.print('\r');        
     
        PrevStateTemp2 = CurrStateTemp2; 
      }      
  }
  PrevStateTemp2 = CurrStateTemp2;  
  
}



void sendPress1Mess(int Press1DState)
{
  CurrStatePress1 = Press1DState;

  if(CurrStatePress1 != PrevStatePress1)
  {
      if(!Serial.available())
      {
        
        Serial.print("Press1State = ");
        switch (CurrStatePress1)
        {            
          case 1:
            Serial.print("Normal");break; 
          case 2:
            Serial.print("Warning");break;  
          case 3:
            Serial.print("Action");break;           
         }          
         Serial.print('\n');
         Serial.print('\r'); 
         
         PrevStatePress1 = CurrStatePress1; 
      }
    
  }
  PrevStatePress1 = CurrStatePress1;
  
  
}

void sendPress2Mess(int Press2DState)
{
  CurrStatePress2 = Press2DState;

  if(CurrStatePress2 != PrevStatePress2)
  {
      if(!Serial.available())
      {
        
        Serial.print("Press2State = ");
        switch (CurrStatePress2)
        {            
          case 1:
            Serial.print("Normal");break; 
          case 2:
            Serial.print("Warning");break;  
          case 3:
            Serial.print("Action");break;           
         }          
         Serial.print('\n');
         Serial.print('\r'); 
         
         PrevStatePress2 = CurrStatePress2; 

         
      }
    
  }
  PrevStatePress2 = CurrStatePress2;
  
  
}







int checkTemp1Lmts(int Temp1Val)
{
    
    if(Temp1Val>Temp1A)
      return 3;
    else if(Temp1Val>Temp1W)
      return 2;  
    else if(Temp1Val>Temp1N)
      return 1;  
    else return 1;
  
}


int checkTemp2Lmts(int Temp2Val)
{
    
    if(Temp2Val>Temp2A)
      return 3;
    else if(Temp2Val>Temp2W)
      return 2;  
    else if(Temp2Val>Temp2N)
      return 1;  
    else return 1;
  
}


int checkPress1Lmts(int Press1Val)
{
    
    if(Press1Val>Press1A)
      return 3;
    else if(Press1Val>Press1W)
      return 2;  
    else if(Press1Val>Press1N)
      return 1;  
    else return 1;
  
}


int checkPress2Lmts(int Press2Val)
{
    
    if(Press2Val>Press2A)
      return 3;
    else if(Press2Val>Press2W)
      return 2;  
    else if(Press2Val>Press2N)
      return 1;  
    else return 1;
  
}
