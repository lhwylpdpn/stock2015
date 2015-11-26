//+------------------------------------------------------------------+
//|                                                     test2015.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
string orderA[];
string orderB[];
string py_orderid[];
string lnA_B[];
string lnA_B_except[];
string filename_all;
int filename_balance;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(3);
   //load_continue();
//---
      filename_all="balance.txt";
      filename_balance=FileOpen(filename_all,FILE_READ|FILE_WRITE|FILE_TXT);
      load_continue();
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   string filename="reportdata_continue.csv";
   int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV); 
   for(int i=0;i<ArraySize(orderA);i++)
   {
    if(StringLen(orderA[i])>0)
    {
     string str=string(orderA[i])+","+string(orderB[i])+","+string(py_orderid[i])+","+string(lnA_B[i])+","+string(lnA_B_except[i]);
     FileWriteString(filehandle,str+"\r\n");

     }
   }
   FileClose(filehandle);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   order_close();
   clac_stop(0.005);
   printf("tick 正常");
   if (is_null_file("tick.csv")==0 && (Minute()==59 || Minute()==14 || Minute()==29 || Minute()==44 ))
   { tickcheck();}
    
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
   //order_close("123968655","123968656","1","2015-03-03");
  //OrderSelect(123867990, SELECT_BY_TICKET,MODE_TRADES); 
// printf(clac_risk("123875771","123966842"));
   if (is_null_file("price_record.csv")==0 && (Minute()==0 || Minute()==15 || Minute()==30 || Minute()==45 ))
   { get_data();}
    
   if(is_null_file("create.txt")!=0)
  {Print("有建仓需求");
   read_API();
  }
  }
   

 
  int is_null_file(string filename)
  { int h=FileOpen(filename,FILE_READ|FILE_TXT);
    int size= FileSize(h);
    FileClose(h);
    return(size);
   }
 
//+------------------------------------------------------------------+

//+---获取历史未完成的订单数据
//+------------------------------------------------------------------+ 
 
 
 void load_continue()
  {
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];

      while(!FileIsEnding(filename_balance))
      {

         u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filename_balance),u_sep,result);
   //--- Show a comment 
       ArrayResize(orderA,ArraySize(orderA)+1);
       ArrayResize(orderB,ArraySize(orderB)+1);
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);

       orderA[ArraySize(orderA)-1]=result[0];
       orderB[ArraySize(orderB)-1]=result[1];
       py_orderid[ArraySize(py_orderid)-1]=result[2];
       lnA_B[ArraySize(lnA_B)-1]=result[3];
       lnA_B_except[ArraySize(lnA_B_except)-1]=result[4];
       printf(orderA[0]);
       printf(orderB[0]);
       printf(py_orderid[0]);
       printf(lnA_B[0]);
       printf(lnA_B_except[0]);
       
   //--- Now output all obtained strings
        
      //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
     }
       printf("有历史没交易订单数");
   }

 void tickcheck()
{ string filename="tick.csv";
  int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV);  

update_data(filehandle,"AUDCAD");

FileClose(filehandle);
              }
//+------------------------------------------------------------------+

//+---获取价格数据写入外部文件
//+------------------------------------------------------------------+
void get_data()
{ string filename="price_record.csv";
  int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV);  

update_data(filehandle,"AUDCAD");
update_data(filehandle,"USDSGD");
update_data(filehandle,"USDCHF");
update_data(filehandle,"NZDCHF");
update_data(filehandle,"NZDCAD");
update_data(filehandle,"GBPSGD");
update_data(filehandle,"GBPNZD");
update_data(filehandle,"GBPCAD");
update_data(filehandle,"GBPAUD");
update_data(filehandle,"EURSGD");
update_data(filehandle,"EURNZD");
update_data(filehandle,"EURCAD");
update_data(filehandle,"EURAUD");
update_data(filehandle,"CADCHF");
update_data(filehandle,"AUDSGD");
update_data(filehandle,"AUDNZD");
update_data(filehandle,"AUDCHF");

                FileClose(filehandle);
                printf("打印数据");}
             
  void update_data(int filehandle,string name)
{   
  // string str=name+","+string(iTime(name,15,0))+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2)+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2);
   string str=name+","+string(iTime(name,15,0))+","+string( iOpen(name,0,0))+","+string(iClose(name,0,0));
 
   FileWriteString(filehandle,str+"\r\n");
 }
 

//+------------------------------------------------------------------+
//+------------------------------------------------------------------+读取python文件函数

void read_API()
  {string filename="create.txt";
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];
   int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);
      while(!FileIsEnding(filehandle))
      {

         u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filehandle),u_sep,result);
   //--- Show a comment 

   //--- Now output all obtained strings
        order_send(result[0],result[1],float(result[2]),float(result[3]),string(result[4]));
        //         多 ，      空，      开仓ln   ，      平仓ln，          订单号
      //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
        
     }
     
       FileClose(filehandle);
       FileDelete(filename);
   }




//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+


//开仓需要 开仓的名称、期望对数差、期望平仓对数差、期望开仓时间
   //+------------------------------------------------------------------+建仓函数      
void order_send (string nameA,string nameB,float lnA_B_in,float lnA_B_except_in,string orderid)
  { 
//--- 
      int ticket_buy;
      int ticket_sell;
      
      
      
      
      ticket_buy=OrderSend(nameA,OP_BUY,0.01,MarketInfo(nameA,MODE_ASK),3,0,0,"",1,0);
      ticket_sell=OrderSend(nameB,OP_SELL,0.01,MarketInfo(nameB,MODE_BID),3,0,0,"",1,0);
      
      while(ticket_buy<0)
         {ticket_buy=OrderSend(nameA,OP_BUY,0.01,MarketInfo(nameA,MODE_ASK),3,0,0,"",1,0);}
      while(ticket_sell<0)
         {ticket_sell=OrderSend(nameB,OP_SELL,0.01,MarketInfo(nameB,MODE_BID),3,0,0,"",1,0);}
     //tracking(filehandle_all,string(ticket_buy)+","+string(ticket_sell)+","+string(except_buy_price)+","+string(except_sell_price)+","+string(buyprice)+","+string(sellprice)+","+string(TimeCurrent()));

       ArrayResize(orderA,ArraySize(orderA)+1);
       ArrayResize(orderB,ArraySize(orderB)+1);
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);

       orderA[ArraySize(orderA)-1]=ticket_buy;
       orderB[ArraySize(orderB)-1]=ticket_sell;
       py_orderid[ArraySize(py_orderid)-1]=orderid;
       lnA_B[ArraySize(lnA_B)-1]=lnA_B_in;
       lnA_B_except[ArraySize(lnA_B_except)-1]=lnA_B_except_in;
       FileWrite(filename_balance,string(ticket_buy)+","+string(ticket_sell)+","+string(orderid)+","+string(lnA_B_in)+","+string(lnA_B_except_in)+","+string(TimeCurrent()));
     
     }
//+------------------------------------------------------------------+ 平仓交易函数                                     
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+



   void order_close()
  {

   for(int i=0;i<ArraySize(orderA);i++)
     {
      if(StringLen(orderA[i])>0)
       {
        string nameA="";
        string nameB="";
        string buy_ticket="";
        string sell_ticket="";
        float ln_close=0;
        buy_ticket=orderA[i];
        sell_ticket=orderB[i];
        ln_close=lnA_B_except[i];
        OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameA=OrderSymbol();
        OrderSelect(sell_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameB=OrderSymbol();
        //平仓判断条件
         printf(MathLog(MarketInfo(nameB,MODE_ASK))-MathLog(MarketInfo(nameA,MODE_BID)));
         printf("close"+string(ln_close));
        if(MathLog(MarketInfo(nameB,MODE_ASK))-MathLog(MarketInfo(nameA,MODE_BID))<ln_close)
         
          { int i_close=1;
            int j_close=1;
          while(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red)&&i_close<3)
          {OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red);
           i_close=i_close+1;}
          while(!OrderClose(sell_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red)&&j_close<3)
          {OrderClose(sell_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red);
          j_close=j_close+1;}
        //printf(GetLastError());
          tracking(orderA[i],orderB[i],"[正态分布卖出"+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]+"]"); 
             orderA[i]="";
             orderB[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
        }
            } 
             }
              
              }
         
       


//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+ 计算止盈止损                                  
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//return 1 操作  return  0 不操作

void clac_stop(float stop_per)
{
   if (stop_per>0)
   {
    
       for(int i=0;i<ArraySize(orderA);i++)
       {  
       if(StringLen(orderA[i])>0)
          {
              string nameA="";
              string nameB="";
              double priceA_open="";
              double priceB_open="";
              string buy_ticket="";
              string sell_ticket="";
              float ln_close=0;
              buy_ticket=orderA[i];
              sell_ticket=orderB[i];
              ln_close=lnA_B_except[i];
                    OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
                    nameA=OrderSymbol();
                    priceA_open=OrderOpenPrice();
                    OrderSelect(sell_ticket, SELECT_BY_TICKET,MODE_TRADES); 
                    nameB=OrderSymbol();
                    priceB_open=OrderOpenPrice();
                   // printf(((MarketInfo(nameA,MODE_BID)-priceA_open)+(priceB_open-MarketInfo(nameB,MODE_ASK)))/(priceA_open+priceB_open));
               if(((MarketInfo(nameA,MODE_BID)-priceA_open)+(priceB_open-MarketInfo(nameB,MODE_ASK)))/(priceA_open+priceB_open)>stop_per || ((MarketInfo(nameA,MODE_BID)-priceA_open)+(priceB_open-MarketInfo(nameB,MODE_ASK)))/(priceA_open+priceB_open)<-stop_per)
                 { int i_close=1;
                    int j_close=1;
                      while(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red)&&i_close<3)
                     {OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red);
                     i_close=i_close+1;}
                      while(!OrderClose(sell_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red)&&j_close<3)
                     {OrderClose(buy_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red);
                     j_close=j_close+1;}
                   // printf(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red));
                tracking(orderA[i],orderB[i],"[止盈损卖出"+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]+"]"); 
                orderA[i]="";
                orderB[i]="";
                py_orderid[i]="";
                lnA_B[i]="";
                lnA_B_except[i]="";
                 
                 } 
            }  
         }
 
   }

  }

//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+ 计算仓息和手续费                                
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+
 float clac_risk(string buy_ticket,string sell_ticket,float )

{     
      return 0;


}

 //+------------------------------------------------------------------+
 //+-日志记录功能------------------------------------+
 //+------------------------------------------------------------------+
 //+------------------------------------------------------------------+


void tracking(string buy_ticket,string sell_ticket,string tag)
{  string string_tracking="";
   OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
   string_tracking=OrderSymbol()+","+OrderOpenPrice()+","+OrderOpenTime()+","+OrderClosePrice()+","+OrderCloseTime()+","+OrderLots()+","+OrderType()+",";
   OrderSelect(sell_ticket, SELECT_BY_TICKET,MODE_TRADES);
   string_tracking=string_tracking+OrderSymbol()+","+OrderOpenPrice()+","+OrderOpenTime()+","+OrderClosePrice()+","+OrderCloseTime()+","+OrderLots()+","+OrderType()+",";
   string_tracking=string_tracking+tag+TimeCurrent();
   int filehandle=FileOpen("report_"+Year()+"_"+Month()+"_"+Day()+".csv",FILE_READ|FILE_WRITE|FILE_TXT);
   int size= FileSize(filehandle);
   if(size==0)
     {
      FileWrite(filehandle,"多单名称,多单开单价格,多单开单时间,多单平仓价格,多单平仓时间,多单开单手数,开单类型,空单名称,空单开单价格,空单开单时间,空单平仓价格,空单平仓时间,空单手数,开单类型,特殊记录,记录时间");
     }
   FileSeek(filehandle, 0, SEEK_END);
   FileWrite(filehandle,string_tracking);
   FileClose(filehandle);
   }
   
   
   
   
//+------------------------------------------------------------------+ 超时平仓函数                                   
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+



   void clac_time(float time_count)
  {

   for(int i=0;i<ArraySize(orderA);i++)
     {
      if(StringLen(orderA[i])>0)
       {
        string nameA="";
        string nameB="";
        string buy_ticket="";
        string sell_ticket="";
        float ln_close=0;
        buy_ticket=orderA[i];
        sell_ticket=orderB[i];
        ln_close=lnA_B_except[i];
        OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameA=OrderSymbol();
        OrderSelect(sell_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameB=OrderSymbol();


        if(MathLog(MarketInfo(nameB,MODE_ASK))-MathLog(MarketInfo(nameA,MODE_BID))<ln_close)
         
          { int i_close=1;
            int j_close=1;
          while(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red)&&i_close<3)
          {OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red);
           i_close=i_close+1;}
          while(!OrderClose(sell_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red)&&j_close<3)
          {OrderClose(sell_ticket,0.01,MarketInfo(nameB,MODE_ASK),0.01,Red);
          j_close=j_close+1;}
        //printf(GetLastError());
          tracking(orderA[i],orderB[i],"[正态分布卖出"+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]+"]"); 
             orderA[i]="";
             orderB[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
        }
            } 
             }
              
              }
         
       