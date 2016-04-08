/*线1*/
SELECT CONCAT(',[',UNIX_TIMESTAMP(DATE_FORMAT(CONCAT(DATE,' ',TIME),'%Y.%m.%d %H:%i')),'000,',CLOSE*10,']') FROM `stock` WHERE stockid='EURNZD.lmx';


/*开单标记*/

SELECT CONCAT(',[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000',']') FROM `order` a , `order_result` b WHERE a.stockid ='EURNZD.lmx' AND a.`orderid`=b.`ln_e_close`
/*开单未平标记*/
SELECT CONCAT(',[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000',']') FROM `order` a  WHERE a.stockid ='GBPAUD.lmx' AND a.`orderid` NOT IN (SELECT ln_e_close FROM order_result)


/*norm点*/

SELECT CONCAT(',[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000,',a.`norm_open`,']') FROM `order` a , `order_result` b WHERE a.stockid ='EURNZD.lmx' AND a.`orderid`=b.`ln_e_close`


/*norm差点*/
SELECT CONCAT(',[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000,',a.`norm_cha_open`,']') FROM `order` a , `order_result` b WHERE a.stockid ='EURNZD.lmx' AND a.`orderid`=b.`ln_e_close`



SELECT CONCAT(UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000'),CONCAT(UNIX_TIMESTAMP(DATE_FORMAT(b.closeA_time,'%Y-%m-%d %H:%i')),'000') FROM `order` a LEFT JOIN `order_result` b ON a.`orderid`=b.`ln_e_close` WHERE a.stockid ='GBPAUD.lmx' 





