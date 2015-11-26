
SHOW STATUS;
SELECT a.stockid,a.date,a.time,a.close,b.stockid,b.date,b.time,b.close FROM (
(SELECT * FROM `stock_back` WHERE stockid='AUDCHF15.csv') a ,

(SELECT * FROM `stock_back` WHERE stockid='NZDCHF15.csv') b )
WHERE a.date=b.date AND a.time=b.time AND  STR_TO_DATE(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i')>=DATE_ADD(NOW(),INTERVAL -11116 DAY) ORDER BY STR_TO_DATE(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i')


SELECT stockid,COUNT(*) FROM stock_back GROUP BY stockid

SELECT stockid FROM stock_foreign.stock_back WHERE stockid IN ('NZDCHF15.csv','AUDCHF15.csv','AUDNZD15.csv','EURAUD15.csv') GROUP BY stockid;