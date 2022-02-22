#include "def_values.h"

long randNumber=0;
char CRLF[] = {'\n', '\r'};
char data[50] = {0};
int i, j = 0;
int Temp1Val, Temp2Val, Press1Val, Press2Val = 0;
int Heater1,Heater2,Pump1,Pump2=0; 
int Heater1Cmd,Heater2Cmd,Pump1Cmd,Pump2Cmd=0;

int Heater1Pin = 2;  // Heater1 connected to digital pin 2
int Heater2Pin = 3;  // Heater2 connected to digital pin 3
int Pump1Pin = 4;    // Pump1 connected to digital pin 4
int Pump2Pin = 5;    // Pump2 connected to digital pin 5
int temp[3]={0,0,0};
char value[3] = {0};
int count=0;

bool temp1reportingflag=0;
bool temp2reportingflag=0;
bool press1reportingflag=0;
bool press2reportingflag=0;

char Message[7]={0};

char Data1[4]={0};
char Data2[4]={0};
char Data3[4]={0};
char Data4[4]={0};
char Data5[4]={0};

char RxData[30]={0};



String str;
String MessageStr;

String DataStr1;
String DataStr2;
String DataStr3;
String DataStr4;
String DataStr5;


void setup()
{
  Serial.begin(19200);
  pinMode(Heater1Pin,OUTPUT);  // sets the Heater1Pin as output
  pinMode(Heater2Pin,OUTPUT);  // sets the Heater2Pin as output
  pinMode(Pump1Pin,OUTPUT);    
  pinMode(Pump2Pin,OUTPUT);    
  digitalWrite(Heater1Pin,LOW); 
  digitalWrite(Heater2Pin,LOW); 
  digitalWrite(Pump1Pin,LOW); 
  digitalWrite(Pump2Pin,LOW); 
  
  //randomSeed(analogRead(4));

}


void loop()
{
  Temp1Val = analogRead(0);
  Temp2Val = analogRead(1);
  Press1Val = analogRead(2);
  Press2Val = analogRead(3);

  //delay(0.5)

  while ((Serial.available()>0)  &  (count<=27)) // data has arrived
  {    
    
    RxData[count] = Serial.read();
       
    count=count+1;   
    

    if(count==27)
    {     
      for (i=0;i<7;i++)
        MessageStr += String(RxData[i]);
     
      for (i=7;i<11;i++)
        DataStr1 += String(RxData[i]);
      //Serial.print("Data1 is  = ");
      //Serial.print(DataStr1);
      //Serial.print('\n');
      //Serial.print('\r');

      for (i=11;i<15;i++)
        DataStr2 += String(RxData[i]);
        
      for (i=15;i<19;i++)
        DataStr3 += String(RxData[i]);
        
      for (i=19;i<23;i++)
        DataStr4 += String(RxData[i]);
        
      for (i=23;i<27;i++)
        DataStr5 += String(RxData[i]);  

          
      

      if((MessageStr == "DataReq"))
      {
        Serial.println(Temp1Val);
        Serial.println(Temp2Val);
        Serial.println(Press1Val);
        Serial.println(Press2Val);
        randNumber = random(1000);
        Serial.println(randNumber);
        
        Serial.println(digitalRead(Heater1Pin));
        Serial.println(digitalRead(Heater2Pin));
        Serial.println(digitalRead(Pump1Pin));
        Serial.println(digitalRead(Pump2Pin));    

      
      } 

      else if((MessageStr == "GetT1Lm"))  // Temp 1 Limits Request 
      {
        Serial.println(Temp1N);   // Normal
        Serial.println(Temp1W);   // Warning
        Serial.println(Temp1A);   // Action
     
      } 
      else if((MessageStr == "GetT2Lm"))  // Temp 2 Limits Request 
      {
        Serial.println(Temp2N);   // Normal
        Serial.println(Temp2W);   // Warning
        Serial.println(Temp2A);   // Action
     
      } 

      else if((MessageStr == "GetP1Lm"))  // Press 1 Limits Request 
      {
        Serial.println(Press1N);   // Normal
        Serial.println(Press1W);   // Warning
        Serial.println(Press1A);   // Action
     
      } 
      else if((MessageStr == "GetP2Lm"))  // Press 2 Limits Request 
      {
        Serial.println(Press2N);   // Normal
        Serial.println(Press2W);   // Warning
        Serial.println(Press2A);   // Action
     
      } 

      else if((MessageStr == "UpdT1Lm"))  // Temp 1 Update Limits Request 
      {

        Temp1N = DataStr1.toInt();Temp1W = DataStr2.toInt();Temp1A = DataStr3.toInt();       
                 
      } 

      else if((MessageStr == "UpdT2Lm"))  // Temp 2 Update Limits Request 
      {

        Temp2N = DataStr1.toInt(); Temp2W = DataStr2.toInt();Temp2A = DataStr3.toInt();                     
    
      }    

      else if((MessageStr == "UpdP1Lm"))  // Press 1 Update Limits Request 
      {

        Press1N = DataStr1.toInt();
        Press1W = DataStr2.toInt();
        Press1A = DataStr3.toInt();      
    
      }   

      else if((MessageStr == "UpdP2Lm"))  // Press 2 Update Limits Request 
      {

        Press2N = DataStr1.toInt();
        Press2W = DataStr2.toInt();
        Press2A = DataStr3.toInt();      
    
      }   

      else if((MessageStr == "cmdhea1"))  // Heater 1 "operate" command recieved 
      {     
        if(DataStr1=="ON  ")digitalWrite(Heater1Pin,HIGH);                        
        else if(DataStr1=="OFF ")digitalWrite(Heater1Pin,LOW);       
               
      } 
      else if((MessageStr == "cmdhea2"))  // Heater 2 "operate" command recieved 
      {     
        if(DataStr1=="ON  ")digitalWrite(Heater2Pin,HIGH);                        
        else if(DataStr1=="OFF ")digitalWrite(Heater2Pin,LOW);       
               
      }
      else if((MessageStr == "cmdpmp1"))  // pump 1 "operate" command recieved 
      {     
        if(DataStr1=="ON  ")digitalWrite(Pump1Pin,HIGH);                        
        else if(DataStr1=="OFF ")digitalWrite(Pump1Pin,LOW);       
               
      } 
      else if((MessageStr == "cmdpmp2"))  // pump 2 "operate" command recieved 
      {     
        if(DataStr1=="ON  ")digitalWrite(Pump2Pin,HIGH);                        
        else if(DataStr1=="OFF ")digitalWrite(Pump2Pin,LOW);       
               
      }
      
      if((MessageStr == "temp1st"))  // temp1 reporting enable/disable
      { 
          if(DataStr1=="En  ")temp1reportingflag=1; 
          else if(DataStr1=="Dis ")temp1reportingflag=0;           
               
      }


      else if((MessageStr == "temp2st"))  // temp2 reporting enable/disable
      { 
          if(DataStr1=="En  ")temp2reportingflag=1; 
          else if(DataStr1=="Dis ")temp2reportingflag=0;           
               
      }

                         
     else if((MessageStr == "pres1st"))  // press1 reporting enable/disable
      { 
          if(DataStr1=="En  ")press1reportingflag=1;
          else if(DataStr1=="Dis ") press1reportingflag=0;           
               
      }

     else if((MessageStr == "pres2st"))  // press2 reporting enable/disable
      { 
          if(DataStr1=="En  ")press2reportingflag=1;
          else if(DataStr1=="Dis ") press2reportingflag=0;           
               
      }      
      
      

//
//      else if((MessageStr == "Pres1st"))  // pump 2 "operate" command recieved 
//      { 
//
//          int Press1DState = checkPress1Lmts(Press1Val);
//          sendPress1Mess(Press1DState);   
//               
//      }            
//      
//      else if((MessageStr == "Pres2st"))  // pump 2 "operate" command recieved 
//      { 
//
//          int Press2DState = checkPress1Lmts(Press2Val);
//          sendPress2Mess(Press2DState);   
//               
//      }            
         
//
    if(temp1reportingflag==1)
    {      
      
      int Temp1DState = checkTemp1Lmts(Temp1Val);
      sendTemp1Mess(Temp1DState);    
    } 

    if(temp2reportingflag==1)
    {       
      int Temp2DState = checkTemp2Lmts(Temp2Val);
      sendTemp2Mess(Temp2DState);    
    } 

    if(press1reportingflag==1)
    {       
      int Press1DState = checkPress1Lmts(Press1Val);
      sendPress1Mess(Press1DState);    
    } 

    if(press2reportingflag==1)
    {       
      int Press2DState = checkPress2Lmts(Press2Val);
      sendPress2Mess(Press2DState);    
    } 
    

      DataStr1 = "";
      DataStr2 = "";
      DataStr3 = "";
      DataStr4 = "";
      DataStr5 = "";

      MessageStr = "";    
      count=0;
      }
     

      
      
    //stringOne += String(value[i],dec);
  }
  
//delay(10);
 

//  
//  int Temp2DState = checkTemp2Lmts(Temp2Val);
//  sendTemp2Mess(Temp2DState);
//
//
//  
//  
//  int Press1DState = checkPress1Lmts(Press1Val);
//  sendPress1Mess(Press1DState);
//
//
//  
//  
//  int Press2DState = checkPress2Lmts(Press2Val);
//  sendPress2Mess(Press2DState);
//
//  delay(10);
  
  


  //Serial.flush();

}
