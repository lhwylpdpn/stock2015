//+------------------------------------------------------------------+
//|                                       close_zhiying_pingcang.mq4 |
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
int OnInit()
  {
//--- create timer
   EventSetTimer(2);
      
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
//---
   close_beizhu();
   zhiying();
  }
//+------------------------------------------------------------------+



void close_beizhu()
{ int total=OrdersTotal();
printf(total);
   for(int i=0;i<total;i++)
     {
      
     
                 string comment;
                 if(OrderSelect(i,SELECT_BY_POS)==false)
                   { Print("OrderSelect 失败错误代码是",GetLastError());
                     
                   }
                 comment = OrderComment();
               
                  if(comment!="")
                  
                    {int type;
                    if(OrderType()==0){type=9;}
                    if(OrderType()==1){type=10;}                   
                    OrderClose(OrderTicket(),OrderLots(),MarketInfo(OrderSymbol(),type),10,Red);
                     printf("强制平仓订单"+OrderTicket()+"备注是"+OrderComment());
     }
     }
   
}

void zhiying()


{
 printf("目前盈利,"+(AccountEquity()-9343)/9343);
 if((AccountEquity()-9343)/9343>=0.04 || (AccountEquity()-9343)/9343<-0.2)
   {
    
   
 while(OrdersTotal()>0)
   {for(int i=0;i<OrdersTotal();i++)
    {  int type;
       if(OrderSelect(i,SELECT_BY_POS)==false)
                   { Print("OrderSelect 失败错误代码是",GetLastError());
                     
                   }
       if(OrderType()==0){type=9;}
       if(OrderType()==1){type=10;}       
       OrderClose(OrderTicket(),OrderLots(),MarketInfo(OrderSymbol(),type),10,Red);
    }
   }
   
     GlobalVariableSet("clearall",10086);
}
}