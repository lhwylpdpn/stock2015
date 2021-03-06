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
string orderB_A[];
string py_orderid[];
string lnA_B[];
string lnA_B_except[];
string send_number[];
string close_bucang[];
string filename_all;
int tt[]={1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181};
int filename_balance;
string first_ticket[];

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
  OnInit();
  printf(UninitializeReason()+"     擦擦擦,time停止");

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   order_close();
   clac_stop();
   printf("tick 正常");
   if (FileIsExist("tick.csv") && (Minute()==0 || Minute()==5|| Minute()==10|| Minute()==15|| Minute()==20|| Minute()==25|| Minute()==30|| Minute()==35|| Minute()==40 || Minute()==45|| Minute()==50|| Minute()==55))
   { tickcheck();}
    
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
      if(GlobalVariableGet("clearall")==10086)
     {
      clearalldata();
      GlobalVariableSet("clearall",0);
     }
   printf(!FileIsExist("price_record.csv"));
   printf(Minute());
   if (!FileIsExist("price_record.csv") && (Minute()==1 || Minute()==6|| Minute()==11|| Minute()==16|| Minute()==21|| Minute()==26|| Minute()==31|| Minute()==36|| Minute()==41 || Minute()==46|| Minute()==51|| Minute()==56))
   { get_data();}
   // get_data();
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
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);
       ArrayResize(send_number,ArraySize(send_number)+1);
       ArrayResize(close_bucang,ArraySize(close_bucang)+1);
       ArrayResize(orderB_A,ArraySize(orderB_A)+1);
       orderA[ArraySize(orderA)-1]=result[0];
      
       py_orderid[ArraySize(py_orderid)-1]=result[1];
       lnA_B[ArraySize(lnA_B)-1]=result[2];
       lnA_B_except[ArraySize(lnA_B_except)-1]=result[3];
       send_number[ArraySize(send_number)-1]=result[4];
       close_bucang[ArraySize(close_bucang)-1]=float(result[5]);       
       orderB_A[ArraySize(orderB_A)-1]=float(result[6]);
  

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

update_data(filehandle,"AUDNZD");
update_data(filehandle,"AUDCAD");
update_data(filehandle,"AUDUSD");
update_data(filehandle,"EURAUD");
update_data(filehandle,"EURCAD");
update_data(filehandle,"EURCHF");
update_data(filehandle,"EURGBP");
update_data(filehandle,"EURUSD");
update_data(filehandle,"GBPAUD");
update_data(filehandle,"GBPCAD");
update_data(filehandle,"GBPCHF");
update_data(filehandle,"GBPUSD");
update_data(filehandle,"NZDUSD");
update_data(filehandle,"USDCAD");
update_data(filehandle,"USDCHF");
update_data(filehandle,"AUDCHF");
update_data(filehandle,"CADCHF");
update_data(filehandle,"EURNZD");
update_data(filehandle,"NZDCAD");
update_data(filehandle,"NZDCHF");
update_data(filehandle,"GBPNZD");
update_data(filehandle,"USDSGD");



//update_data(filehandle,"USDJPY");
//update_data(filehandle,"NZDJPY");
//update_data(filehandle,"EURJPY");
//update_data(filehandle,"GBPJPY");
//update_data(filehandle,"AUDJPY");
//update_data(filehandle,"CADJPY");

                FileClose(filehandle);
                printf("打印数据");}
             
  void update_data(int filehandle,string name)
{  //多读几次，为了防止时间读错误或者为空
  // string str=name+","+string(iTime(name,15,0))+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2)+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2);
   string str=name+","+string(TimeLocal())+","+string( iOpen(name,0,0))+","+string(MarketInfo(name,MODE_BID));
    str=name+","+string(TimeLocal())+","+string( iOpen(name,0,0))+","+string(MarketInfo(name,MODE_BID));
    
   FileWriteString(filehandle,str+"\r\n");
 }
   void update_data_zhunbei(int filehandle,string name)
{  //多读几次，为了防止时间读错误或者为空
  // string str=name+","+string(iTime(name,15,0))+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2)+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2);
   string str=name+","+string(iTime(name,5,0))+","+string( iOpen(name,0,0))+","+string(iClose(name,0,0));
 

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
     // printf(float(result[5]));
   //--- Now output all obtained strings
        order_send(result[0],float(result[1]),float(result[2]),string(result[3]),string(result[4]),float(result[5]),0.01,0);
        //         stockid ，    买入价，      卖出价   ，      订单号，          补仓点            多 or 空
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
void order_send (string nameA,float open ,float except_close ,string orderid, string bucang ,float open_status,string open_number,string pre_orderid)
  { 
//--- 


//--- 测试控制总订单数
//if(open_number==0.01)
//  {
//   
//  
//         int total_test=OrdersTotal();
//         float countall_test=0;
//         for(int i=0;i<total_test;i++)
//           {OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
//           // printf(""+OrderOpenTime());
//           if(OrderLots()==0.01)
//             {
//               countall_test=countall_test+float(OrderLots());
//             }
//             }
// 
//      if(countall_test>=0.05)
//        {printf(orderid+"这个没开..");
//         return;
//        }
//        
//   }


      int ticket_buy;
      int open_s;
      int open_s2;
      float bucangjiage;
  
      if (open_status>0.5)
        {open_s=1;
        open_s2=9;
        }
      else
        {open_s=0;
         open_s2=10;
        
        }

      ticket_buy=OrderSend(nameA,open_s,open_number,MarketInfo(nameA,open_s2),3,0,0,"",1,0);
     printf(ticket_buy);
      printf(GetLastError());
      while(ticket_buy<0)
         {ticket_buy=OrderSend(nameA,open_s,open_number,MarketInfo(nameA,open_s2),3,0,0,"",1,0);}
      OrderSelect(ticket_buy, SELECT_BY_TICKET,MODE_TRADES); 
       if (open_status>0.5)
        {
        bucangjiage=float(OrderOpenPrice())+float(bucang);}
      else
        {
         bucangjiage=float(OrderOpenPrice()) - float(bucang);
        }
      
      
       ArrayResize(orderA,ArraySize(orderA)+1);
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);
       ArrayResize(send_number,ArraySize(send_number)+1);
       ArrayResize(close_bucang,ArraySize(close_bucang)+1);
       ArrayResize(orderB_A,ArraySize(orderB_A)+1);
       orderA[ArraySize(orderA)-1]=ticket_buy;
       py_orderid[ArraySize(py_orderid)-1]=orderid;
       lnA_B[ArraySize(lnA_B)-1]=open;
       lnA_B_except[ArraySize(lnA_B_except)-1]=except_close;
       send_number[ArraySize(send_number)-1]=open_number;
       close_bucang[ArraySize(close_bucang)-1]=bucangjiage;
       orderB_A[ArraySize(orderB_A)-1]=pre_orderid;
       FileWrite(filename_balance,string(ticket_buy)+","+string(orderid)+","+string(open)+","+string(except_close)+","+string(open_number)+","+string(bucangjiage)+","+string(TimeCurrent())+","+string(pre_orderid));
 
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
        string buy_ticket="";
        float ln_close=0;
        float buy_num;
        float open_type;
        float open_price;
        buy_ticket=orderA[i];
        ln_close=lnA_B_except[i];
        string orderB_A_ticket="";
        orderB_A_ticket=orderB_A[i];
        OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameA=OrderSymbol();
        buy_num=OrderLots();
        open_type=OrderType();
         open_price=OrderOpenPrice();
        //平仓判断条件
         //printf(MathLog(MarketInfo(nameB,MODE_ASK))-MathLog(MarketInfo(nameA,MODE_BID)));
         //printf("close"+string(ln_close));

        if(MarketInfo(nameA,MODE_BID)>ln_close&&open_type==0)
         
          { int i_close=1;
            int ticket=0;
            ticket=OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_BID),8,Red);
          while(ticket<0&&i_close<5)
          {ticket=OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_BID),8,Red);
           i_close=i_close+1;}
           
           if(ticket>0)
             {
              
             
               for(int j=0;j<ArraySize(orderA);j++)
            {
              if(orderA[j]==orderB_A_ticket)
               {printf(string(j)+","+orderA[j]+","+orderB_A_ticket);
               close_bucang[j]=open_price+MarketInfo(nameA,MODE_BID)-MarketInfo(nameA,MODE_ASK);
               }
            }
         //close_with_other(orderB_A_ticket);
        //printf(GetLastError());
          tracking(orderA[i],orderB_A[i]+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]); 
             orderA[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
             send_number[i]="";
             close_bucang[i]="";
       
       
              }
       
        }
        
         if(MarketInfo(nameA,MODE_ASK)<ln_close&&open_type==1)
         
          { int i_close=1;
            int ticket=0;
            ticket=OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_ASK),8,Red);
          while(ticket<0&&i_close<5)
          {OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_ASK),8,Red);
           i_close=i_close+1;}
           
            if(ticket>0)
              {
               
              
           
           
            for(int j=0;j<ArraySize(orderA);j++)
             { 
              if(orderA[j]==orderB_A_ticket)
               {printf(string(j)+","+orderA[j]+","+orderB_A_ticket);
                 close_bucang[j]=open_price+MarketInfo(nameA,MODE_ASK)-MarketInfo(nameA,MODE_BID);
               }
             }
            //close_with_other(orderB_A_ticket);
        //printf(GetLastError());
          tracking(orderA[i],orderB_A[i]+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]); 
             orderA[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
             send_number[i]="";
             close_bucang[i]="";
             
             
                  }
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

void clac_stop()
{
   
   
    
       for(int i=0;i<ArraySize(orderA);i++)
       {  
       if(StringLen(orderA[i])>0)
          {
              string nameA="";
              double priceA_open="";
              string buy_ticket="";
              float ln_close=0;
              float buy_num;
              float open_type;
              float bucang;
              buy_ticket=orderA[i];
              ln_close=lnA_B_except[i];
              float bucangjiage=close_bucang[i];
              
                    OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
                    nameA=OrderSymbol();
                    priceA_open=OrderOpenPrice();
                    buy_num=OrderLots();
                    open_type=OrderType();
                   // printf(((MarketInfo(nameA,MODE_BID)-priceA_open)+(priceB_open-MarketInfo(nameB,MODE_ASK)))/(priceA_open+priceB_open));
              
              
              
               printf(nameA+","+string(bucangjiage)+","+string(float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100))+","+string(ln_close));
               
               
               if(MarketInfo(nameA,MODE_ASK)<bucangjiage &&open_type==0 && tt[ArrayMaximum(tt)]!=tt[ArrayBsearch(tt,buy_num*100)])
                 {
 
                 order_send(nameA,bucangjiage,priceA_open,00000,string(priceA_open-bucangjiage),0.1,float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100),buy_ticket);
             
                   // printf(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red));

                 close_bucang[i]=0;
                 } 
            
               if(MarketInfo(nameA,MODE_BID)>bucangjiage &&open_type==1 && tt[ArrayMaximum(tt)]!=tt[ArrayBsearch(tt,buy_num*100)])
                 { 

                 order_send(nameA,bucangjiage,priceA_open,00000,string(bucangjiage-priceA_open),0.9,float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100),buy_ticket);
                 
                   // printf(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red));

                 close_bucang[i]=1000;
                 } 
           

           
           
            }  
         }
 
   

  }


void tracking(string buy_ticket,string tag)
{  string string_tracking="";
   OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
   string_tracking=OrderSymbol()+","+OrderOpenPrice()+","+OrderOpenTime()+","+OrderClosePrice()+","+OrderCloseTime()+","+OrderLots()+","+OrderType()+","+OrderCommission()+","+OrderProfit()+",";
   string_tracking=string_tracking+tag;
   int filehandle=FileOpen("order/report_"+rand()+rand()+".csv",FILE_READ|FILE_WRITE|FILE_TXT);
   int size= FileSize(filehandle);
   FileSeek(filehandle, 0, SEEK_END);
   FileWrite(filehandle,string_tracking);
   FileClose(filehandle);
   }
   
   
   
   
//+------------------------------------------------------------------+ for lining baobiao                                   
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+




       
       
 void close_with_other(string buy_ticket)
{  printf("close   "+buy_ticket);
   
  for(int i=0;i<ArraySize(orderA);i++)
    {
     if(orderA[i]==buy_ticket)
       {
        OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        string nameA=OrderSymbol();
        float buy_num=OrderLots();
        int open_type=OrderType();
        int type;
        int i_close=0;
        if(open_type==0)
          {
           type=9;
          }
       if(open_type==1)
          {
           type=10;
          }
        while(!OrderClose(buy_ticket,buy_num,MarketInfo(nameA,type),8,Red)&&i_close<30)
          {OrderClose(buy_ticket,buy_num,MarketInfo(nameA,type),8,Red);
           i_close=i_close+1;}
           tracking(buy_ticket,orderB_A[i]+","); 
       if(orderB_A[i]!=0)
          {  

            close_with_other(orderB_A[i]);
        
          }
             orderA[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
             send_number[i]="";
             close_bucang[i]="";
             orderB_A[i]="";
       }
    }
}

 
 
 
void clearalldata()
{      ArrayResize(orderA,0);
       ArrayResize(py_orderid,0);
       ArrayResize(lnA_B,0);
       ArrayResize(lnA_B_except,0);
       ArrayResize(send_number,0);
       ArrayResize(close_bucang,0);
       ArrayResize(orderB_A,0);

}