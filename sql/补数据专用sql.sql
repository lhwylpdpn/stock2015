TRUNCATE TABLE `stock`;
TRUNCATE TABLE `releation_mid`;


DROP TABLE bushuju;
CREATE TABLE bushuju 
SELECT * FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') IN (SELECT  STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') FROM stock GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') HAVING COUNT(*)<>1

) AND stockid IN (SELECT stockid FROM stock GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') HAVING COUNT(*)<>1
) GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') ;

DELETE FROM stock WHERE stockid IN (SELECT stockid FROM  bushuju) AND STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') IN (SELECT STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') FROM bushuju);

INSERT INTO stock SELECT * FROM bushuju;
/*慎重用，删除掉数据中 重复的项，会有小影响*/


