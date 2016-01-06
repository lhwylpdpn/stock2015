SELECT COUNT(*),stockid FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')>DATE_ADD(NOW(),INTERVAL -5 DAY) GROUP BY stockid;
/*查看每个id 目前有的count总数，应该全一样*/
SELECT COUNT(a) FROM (SELECT stockid,DATE,TIME,COUNT(*) AS a FROM stock   GROUP BY STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') ,stockid HAVING COUNT(*)>1) a;
/*查看每个id 日期有重复的数据，应该没有内容*/


SELECT COUNT(*),MAX(releation) FROM `releation_mid`;
/*查看关系表数据正确性*/
SELECT stockid,DATE,TIME,COUNT(*) AS a FROM stock   GROUP BY STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') ,stockid HAVING COUNT(*)>1;
SHOW STATUS;

SELECT * FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')>DATE_ADD(NOW(),INTERVAL -1 DAY) AND stockid='eursgd'  GROUP BY STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i'),stockid  DESC


SELECT * FROM stock WHERE stockid='audsgd' AND STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')>DATE_ADD(NOW(),INTERVAL -1 DAY)


SELECT a.stockid,a.close_now,a.avgA_B,a.stdA_B,a.norm_ln_prev,a.norm_ln_prev2,a.avg_cha,a.std_cha,a.norm_cha_prev,a.norm_cha_prev2,b.flag FROM `releation_mid` a ,model_config b WHERE a.stockid=b.stockid



SELECT * FROM stock GROUP BY stockid