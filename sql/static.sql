


SELECT 成功盈利率 AS '成功盈利率 >0.0007',失败盈利率,成功率 AS '成功率 >88%',失败率,(成功盈利率*成功率+失败盈利率*失败率)/100 AS "数据期望 >0" FROM (SELECT
COUNT(CASE WHEN order_type=1 THEN 1 END )/COUNT(*) * SUM(CASE WHEN order_type=1 THEN ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B) END)/COUNT(*) AS 成功盈利率 ,
COUNT(CASE WHEN order_type=0 THEN 1 END )/COUNT(*) * SUM(CASE WHEN order_type=1 THEN ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B) END)/COUNT(*) AS 失败盈利率,
CONCAT(ROUND(COUNT(CASE WHEN order_type=1 THEN 1 END )/COUNT(*)*100,4),"%")  AS 成功率,
CONCAT(ROUND(COUNT(CASE WHEN order_type=0 THEN 1 END )/COUNT(*)*100,4),"%")  AS 失败率
FROM `order_result`
) a 
UNION
SELECT '建仓额外差损失百分比','平均建仓损失','建仓正确性百分比','平均建仓利润空间','-'
UNION
SELECT CONCAT(ROUND(COUNT(CASE WHEN LN(openb)-LN(opena)-ln_e_open<0 THEN 1 END)/COUNT(*)*100,4),"%") AS 建仓额外差赢损百分比,
AVG(LN(openb)-LN(opena)-ln_e_open) AS 平均建仓损失,
CONCAT(ROUND(COUNT(CASE WHEN LN(openb)-LN(opena)-ln_e_close>0 THEN 1 END)/COUNT(*)*100,4),"%") AS 建仓正确性百分比,
AVG(LN(openb)-LN(opena)-ln_e_close) AS 平均建仓利润空间,'-'
FROM `order_result`
UNION
SELECT '成功平均持仓时间_分钟','成功最大持仓时间_分钟','失败最大持仓时间_分钟','失败最大持仓时间_分钟','-'
/*订单建仓正确性、建仓额差等*/
UNION
SELECT AVG(CASE WHEN order_type=1 THEN TIMESTAMPDIFF(MINUTE,openB_time,closeB_time) END) AS 成功平均持仓时间_分钟,
MAX(CASE WHEN order_type=1 THEN TIMESTAMPDIFF(MINUTE,openB_time,closeB_time) END) AS 成功最大持仓时间_分钟,
AVG(CASE WHEN order_type=0 THEN TIMESTAMPDIFF(MINUTE,openB_time,closeB_time) END) AS 失败最大持仓时间_分钟,
MAX(CASE WHEN order_type=0 THEN TIMESTAMPDIFF(MINUTE,openB_time,closeB_time) END) AS 失败最大持仓时间_分钟,'-'
 FROM `order_result`
UNION
SELECT '平均每日建仓','-','-','-','-'
UNION
SELECT ROUND(COUNT(*)/(STR_TO_DATE(MAX(openA_time),'%Y.%c.%d ')-STR_TO_DATE(MIN(openA_time),'%Y.%c.%d ')+1),2) AS 平均每日建仓数 ,'-','-','-','-'FROM `order_result`
UNION
SELECT "日均盈利  >0.05%",'-','-','-','-'
/*平均每日建仓数*/ 
UNION
SELECT CONCAT(ROUND(SUM((closeA-openA)*lots_A+(openB-closeB)*lots_B)/SUM(openA*lots_A+openB*lots_B)*100,4),"%"),'-','-','-','-' FROM order_result



