//+------------------------------------------------------------------+
//|                                             tracking_Balance.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

float  finalcost=AccountEquity();

int OnInit()
  {
//--- create timer
   EventSetTimer(60);
      
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
     OnInit();
  printf(UninitializeReason()+"     擦擦擦,time停止");
      
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
tracking_Balance();
tracking_Equity();
tracking_AccountMargin();
tracking_KPI1();
printf("tack");  
  }
//+------------------------------------------------------------------+
 void tracking_Balance()
{   string filename="json/tracking_Balance.json";
  int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);  
   FileSeek(filehandle, -1, SEEK_END);
   FileWriteString(filehandle, ",[ ");
   FileWriteString(filehandle,datetime(TimeLocal())*1000);
   FileWriteString(filehandle,","+(float(AccountBalance())-float(AccountEquity()))/ float(AccountBalance())*100 +"]"+" \r\n"+"]");

   FileClose(filehandle);
   }
 void tracking_Equity()
{   string filename="json/tracking_Equity.json";
  int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);  
   FileSeek(filehandle, -1, SEEK_END);
   FileWriteString(filehandle, ",[ ");
   FileWriteString(filehandle,datetime(TimeLocal())*1000);
   FileWriteString(filehandle,","+(float(AccountBalance()-finalcost)/finalcost*100)+"]"+" \r\n"+"]");

   FileClose(filehandle);
   }
 void tracking_AccountMargin()
{   string filename="json/tracking_AccountMargin.json";
  int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);  
   FileSeek(filehandle, -1, SEEK_END);
   FileWriteString(filehandle, ",[ ");
   FileWriteString(filehandle,datetime(TimeLocal())*1000);
   FileWriteString(filehandle,","+float(AccountMargin()/float(AccountBalance())*100  )+"]"+" \r\n"+"]");

   FileClose(filehandle);
   }


 void tracking_KPI1()
{   string filename="json/KPI_1.json";
  int filehandle=FileOpen(filename,FILE_WRITE|FILE_TXT);  
   FileWriteString(filehandle,"{\"jingzhi\":"+round(AccountEquity())+",\"jingzhibili\":"+(AccountEquity()-finalcost)/finalcost*100+",\"ordertotal\":"+OrdersTotal()+",\"lotscount\":"+countlots()+"}");
   FileClose(filehandle);
   FileDelete(filehandle);}
   
   
   
  
float countlots()
{  int total=OrdersTotal();
float countall=0;
for(int i=0;i<total;i++)
  {OrderSelect(i,SELECT_BY_POS);
  
   countall=countall+float(OrderLots());
  }

return(countall);
}