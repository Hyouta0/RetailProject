-- CREATE  database retail;
use retail;
CREATE TABLE member(
member_id int PRIMARY KEY,
f_name    varchar(30),
l_name    varchar(30),
store_id  int,
mem_date  varchar(10));

show tables;
-- DROP TABLE member;

LOAD DATA LOCAL INFILE '/home/kiran/code/RetailProject/member_data.csv'
INTO TABLE member
FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
LINES TERMINATED BY '\n';
-- IGNORE 1 ROWS;

SELECT * FROM  member;

CREATE TABLE product(
product_id  INT PRIMARY KEY,
description VARCHAR(30),
price       FLOAT,
category    VARCHAR(30),
max_qty     INT);

LOAD DATA LOCAL INFILE '/home/kiran/code/RetailProject/product.csv'
INTO TABLE product
FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM product;

CREATE TABLE trans_hdr(
trans_id varchar(30),
member_id int ,
store_id int,
trans_date varchar(10),
PRIMARY KEY(trans_id,member_id)
);
DROP TABLE trans_hdr;
LOAD DATA LOCAL INFILE '/home/kiran/code/RetailProject/transHeader.csv'
INTO TABLE trans_hdr 
FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
TRUNCATE TABLE trans_hdr; 
SELECT * FROM trans_hdr;


CREATE TABLE trans_dtl(
trans_id  varchar(30),
product_id int,
qty         int,
amount     FLOAT,
trans_date varchar(10),
PRIMARY KEY(trans_id,product_id)
);
DROP TABLE trans_dtl;

LOAD DATA LOCAL INFILE '/home/kiran/code/RetailProject/transDetail.csv'
INTO TABLE trans_dtl 
FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM trans_dtl;


