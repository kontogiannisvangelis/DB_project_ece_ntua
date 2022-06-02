DELETE FROM university where Organization_id<1000;

DELETE FROM research_center where Organization_id<1000;

DELETE FROM corporation where Organization_id<1000;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/University.csv' 
INTO TABLE university 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Researc_center.csv' 
INTO TABLE research_center
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Corporation.csv' 
INTO TABLE corporation 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

DELETE FROM Deliverable d where d.Project_id  in (select p.Project_id from Project p 
where p.Organization_id in (10,20,30));
    
    