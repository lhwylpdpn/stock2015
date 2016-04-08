SELECT a.stockid,UNIX_TIMESTAMP(DATE_FORMAT(CONCAT(a.date,' ',a.time),'%Y.%m.%d %h:%i')) AS time_,a.close,b.norm_open,b.norm_cha_open,!ISNULL(b.a) AS a , b.c FROM (SELECT * FROM `stock` WHERE stockid='GBPAUDpro') a LEFT JOIN
(
SELECT stockid,norm_open,norm_cha_open,DATE_FORMAT(order_time_send,'%Y.%m.%d') a ,  DATE_FORMAT(order_time_send,'%h:%i') b ,DATE_FORMAT(b.closeA_time,'%Y.%m.%d %h:%i') AS c FROM `order` a ,`order_result` b
 WHERE stockid='GBPAUDpro' AND a.`orderid`=b.`ln_e_close`


) b
ON a.stockid=b.stockid AND a.date=b.a AND a.time=b.b;







SELECT a.stockid,a.date,a.time,a.close,b.norm_open,b.norm_cha_open,!ISNULL(b.a) FROM (SELECT * FROM `stock` WHERE stockid='GBPAUDpro') a LEFT JOIN
(

SELECT stockid,norm_open,norm_cha_open,DATE_FORMAT(order_time_send,'%Y.%m.%d') a ,  DATE_FORMAT(order_time_send,'%h:%i') b FROM `order` WHERE stockid='GBPAUDpro' AND
orderid NOT IN (SELECT ln_e_close FROM `order_result` WHERE nameA='GBPAUDpro')
) b
ON a.stockid=b.stockid AND a.date=b.a AND a.time=b.b;


