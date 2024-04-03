import mysql.connector

connect = mysql.connector.connect(
    host="localhost",
    user="root",
    password="{dDO`HklZa!@|]xoV[r&",
    database="retail_pro"
)


ClearProductPerato='TRUNCATE TABLE product_perato'
UpdateProductPerato = '''
INSERT INTO product_perato
(SELECT sub.*,SUM(sub.total) OVER(ORDER BY sub.total DESC)*100/SUM(sub.total) OVER() AS parato
FROM
(SELECT td.product_id ,p.description,SUM(td.qty) As total FROM trans_dtl td 
JOIN (SELECT product_id,description FROM product) p ON p.product_id=td.product_id
WHERE trans_date > DATE_SUB(NOW(),INTERVAL 1 YEAR)  
GROUP BY product_id) AS sub);
'''
ClearInterPurchaseInterval='TRUNCATE TABLE inter_purchase_interval'
UpdateInterPurchaseInterval='''
INSERT INTO inter_purchase_interval 
(SELECT ipi.member_id,ROUND(AVG(DATEDIFF(ipi.trans_date,ipi.last_date))) AS ipi 
FROM 
(SELECT th.member_id,th.trans_date,
LAG(th.trans_date) OVER(PARTITION BY th.member_id ORDER BY th.trans_date) AS last_date
FROM trans_hdr th 
WHERE th.trans_date > DATE_SUB(NOW(),INTERVAL 1 YEAR)) AS ipi
GROUP BY ipi.member_id
ORDER BY ipi)
'''
ClearSeasonalityIdx='TRUNCATE TABLE seasonality'
UpdateSeasonalityIdx='''
INSERT INTO seasonality 
SELECT sub.product_id,p.description ,sub.year,
CASE 
	WHEN sub.month = 1 THEN 'Jan'
	WHEN sub.month = 2 THEN 'Feb'
	WHEN sub.month = 3 THEN 'Mar'
	WHEN sub.month = 4 THEN 'Apr'
	WHEN sub.month = 5 THEN 'May'
	WHEN sub.month = 6 THEN 'Jun'
	WHEN sub.month = 7 THEN 'Jul'
	WHEN sub.month = 8 THEN 'Aug'
	WHEN sub.month = 9 THEN 'Sep'
	WHEN sub.month = 10 THEN 'Oct'
	WHEN sub.month = 11 THEN 'Nov'
	WHEN sub.month = 12 THEN 'Dec'
END AS month,
sub.sale/AVG(sub.sale)OVER(PARTITION BY sub.product_id,sub.year) AS seasonality
FROM
(SELECT td.product_id,
Year(td.trans_date) AS year,
MONTH(td.trans_date) AS month,
SUM(td.qty) AS sale
FROM trans_dtl td
GROUP BY product_id ,year,month)sub
JOIN product p ON p.product_id =sub.product_id
'''
ClearTransactionMatrix='TRUNCATE TABLE transaction_matrix'
UpdateTransactionMatrix='''
INSERT INTO transaction_matrix 
(SELECT sub2.member_id,
CASE 
	WHEN sub2.rnk BETWEEN 1 AND 10 THEN 'Gold'
	WHEN sub2.rnk BETWEEN 11 AND 30 THEN 'Silver'
	WHEN sub2.rnk BETWEEN 31 AND 50 THEN 'Bronz'
	ELSE 'no-membership'
END AS membership
FROM
(SELECT sub.*,RANK() OVER(ORDER BY sub.trip DESC) AS rnk
FROM
(SELECT member_id ,COUNT(trans_id) AS trip
FROM trans_hdr
WHERE trans_date < DATE_SUB(NOW(),INTERVAL 1 YEAR) 
GROUP BY member_id)sub)sub2);
'''
ClearRewardScore='TRUNCATE TABLE reward_score'
UpdateRewardScore='''
INSERT INTO reward_score 
SELECT reward.product_id,reward.member_id,(reward.trip-reward.min)/(reward.max-reward.min) AS reward
FROM 
(SELECT trip.*,MIN(trip.trip)OVER(PARTITION BY trip.product_id) AS min,
MAX(trip.trip)OVER(PARTITION BY trip.product_id) AS max
FROM 
(SELECT td.product_id,th.member_id,COUNT(th.trans_id) AS trip  FROM trans_hdr th
JOIN (SELECT product_id,trans_id FROM trans_dtl) td ON td.trans_id=th.trans_id
WHERE th.trans_date > DATE_SUB(NOW(),INTERVAL 1 YEAR) 
GROUP BY td.product_id,th.member_id)trip)reward
'''
ClearDiscount='TRUNCATE TABLE discount'
UpdateDiscount='''
INSERT INTO discount
SELECT sub.product_id,sub.member_id,(sub.reward_per+sub.membership_per) AS discount
FROM
(SELECT rs.product_id,rs.member_id,
CASE 
	WHEN rs.reward <0.25 THEN 0
	WHEN rs.reward <0.3  THEN 3
	WHEN rs.reward <0.5  THEN 5
	WHEN rs.reward <0.7  THEN 7
	ELSE 9
END AS reward_per,
CASE 
	WHEN tm.membership ='no-membership' THEN 0
	WHEN tm.membership = 'Bronz'        THEN 5
	WHEN tm.membership = 'Silver'       THEN 10
	WHEN tm.membership = 'Gold'         THEN 15
END AS membership_per
FROM reward_score rs
JOIN transaction_matrix tm ON tm.member_id =rs.member_id)sub;
'''
ClearAffinity='TRUNCATE affinity'
UpdateAffinity='''
INSERT INTO affinity
WITH total AS(
SELECT product_id,COUNT(trans_id) AS total
FROM trans_dtl td
GROUP BY product_id
)
SELECT sub.p1,sub.p2,sub.cnt/sub.total AS affinity_score
FROM
(SELECT td.product_id AS p1,td2.product_id  AS p2 ,COUNT(td.trans_id) AS cnt ,tl.total
FROM trans_dtl td 
JOIN trans_dtl td2 ON td.trans_id=td2.trans_id 
JOIN total tl ON tl.product_id=td.product_id
WHERE td.product_id != td2.product_id 
GROUP BY td.product_id,td2.product_id
ORDER BY cnt DESC)sub
GROUP BY sub.p1
'''

cursor = connect.cursor()
cursor.execute(ClearProductPerato)
cursor.execute(UpdateProductPerato)
cursor.execute(ClearInterPurchaseInterval)
cursor.execute(UpdateInterPurchaseInterval)
cursor.execute(ClearSeasonalityIdx)
cursor.execute(UpdateSeasonalityIdx)
cursor.execute(ClearTransactionMatrix)
cursor.execute(UpdateTransactionMatrix)
cursor.execute(ClearRewardScore)
cursor.execute(UpdateRewardScore)
cursor.execute(ClearDiscount)
cursor.execute(UpdateDiscount)
cursor.execute(ClearAffinity)
cursor.execute(UpdateAffinity)

connect.commit()
cursor.close()
connect.close()
