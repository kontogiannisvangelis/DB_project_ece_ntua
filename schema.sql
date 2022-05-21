DROP SCHEMA IF EXISTS eldik_db;
CREATE SCHEMA eldik_db;
USE eldik_db;


create table Organizations(
	Organization_id int unsigned auto_increment,
    Org_name varchar(50) not null,
    Abbreviation varchar(10) not null,
    Post_code int(5) not null,
    Street varchar(20) not null,
    City varchar(20) not null,
    Org_type varchar(20) not null, check (Org_type in ('University', 'Corporation', 'Research_center')),
    primary key (Organization_id)
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Researcher(
	Researcher_id int unsigned  auto_increment, 
    First_name varchar(20) not null,
	Last_name varchar(20) not null,
	Birthdate date not null,
    Sex varchar(20) default null check (Sex in ('Female', 'Male', 'Other')),
    Start_date_work_org date not null,
    Organization_id int unsigned not null, 
    primary key (Researcher_id),
    constraint fk_organization_id_researcher foreign key (Organization_id) references Organizations(Organization_id) on delete cascade on update cascade 
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Research_center(
	Organization_id int unsigned,
    Budget_ministry int default null,
    Budget_private int default null,
    primary key(Organization_id),
    constraint fk_organization_id_reaseach_center foreign key (Organization_id) references Organizations(Organization_id) on delete cascade on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table University(
	Organization_id int unsigned,
    Budget_ministry int default null,
    primary key(Organization_id),
    constraint fk_organization_id_university foreign key (Organization_id) references Organizations(Organization_id) on delete cascade on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table corporation(
	Organization_id int unsigned,
    Equity int default null,
    primary key(Organization_id),
    constraint fk_organization_id_corporation foreign key (Organization_id) references Organizations(Organization_id) on delete cascade on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Evaluation(
	Evaluation_id int unsigned  auto_increment, 
	Eval_date date not null,
    Grade int default 0 check(Grade<=100 and Grade>=0),
    Researcher_id int unsigned ,
    Organization_id int unsigned,
    #check the one who does  the eval researcher_id does not belong to organization_id from project
    primary key(Evaluation_id),
    constraint fk_researcher_id_evaluation foreign key(Researcher_id) references Researcher(Researcher_id) on delete set null on update cascade,
    constraint fk_organization_id_evaluation foreign key(Organization_id) references Organizations(Organization_id) on delete set null on update cascade
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Organization_phones( 
	Phone_number bigint unsigned,
    Organization_id int unsigned not null,
    primary key(Phone_number),
	constraint fk_organization_id_phones foreign key (Organization_id) references Organizations(Organization_id) on delete cascade on update cascade 
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Program(
	Program_id int unsigned  auto_increment,
	Program_name varchar(20) not null,
	Program_section varchar(20) not null,
    primary key(Program_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Executive(
	Executive_id int unsigned  auto_increment,
    First_name varchar(20) not null,
    Last_name varchar(20) not null,
    primary key (Executive_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    

    
create table Scientific_field(
	Scientific_field_id int unsigned  auto_increment,
    Sf_name varchar(20) not null,
    primary key(Scientific_field_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table Project(
	Project_id int unsigned  auto_increment,
	Amount int default 0, #when we insert amount we have to check if eval greater than 50
    Title varchar(30) not null,
	Start_Date date default null, 
	End_Date date  default null,
    Project_description Varchar(400) default null,
    #Duration derived and check between 1 and 4 years
    Evaluation_id int unsigned not null,  
    Program_id int unsigned not null,
    Researcher_id int unsigned not null , 
    Executive_id int unsigned not null ,
	Organization_id int unsigned not null,
    primary key (Project_id),
    constraint fk_executive_id_project foreign key(Executive_id) references Executive(Executive_id) on delete restrict on update cascade, #crete trigger that changes null to a person
    constraint fk_program_id_project foreign key(Program_id) references Program(Program_id) on delete restrict on update cascade,
	constraint fk_researcher_id_project foreign key(Researcher_id) references Researcher(Researcher_id) on delete restrict on update cascade, #wait answer
    constraint fk_evaluation_id_project foreign key(Evaluation_id) references Evaluation(Evaluation_id)on delete restrict on update cascade,
    constraint fk_organization_id_project foreign key(Organization_id) references Organizations(Organization_id) on delete restrict on update cascade #wait answer
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Works_on_project(
	Project_id int unsigned,
    Researcher_id int unsigned,
    primary key(Project_id, Researcher_id),
	constraint fk_researcher_id_work_on_project foreign key(Researcher_id) references Researcher(Researcher_id) on delete cascade on update cascade,
    constraint fk_project_id_works_on_project foreign key(Project_id) references Project(Project_id) on delete cascade on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
    create table Sf_belongs(
	Project_id int unsigned,
    Scientific_field_id int unsigned,
    primary key(Project_id,Scientific_field_id),
    constraint fk_sf_field_sf_belongs foreign key(Scientific_field_id) references Scientific_field(Scientific_field_id) on delete restrict on update cascade,
    constraint fk_project_id_sf_belongs foreign key(Project_id) references Project(Project_id) on delete cascade on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Deliverable(
	Deliverable_id int unsigned  auto_increment,
    Project_id int unsigned,
    Title varchar(20),
    Deliv_description varchar(400) default null,
    Delivery_date date not null ,
    primary key (Deliverable_id, Project_id),
    constraint fk_project_id_deliverable foreign key(Project_id) references Project(Project_id) on delete cascade on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
DELIMITER $$
create trigger evaluator_check before insert on Evaluation
for each row
begin 
if new.Organization_id = (
		select r.Organization_id
        from Researcher r
        where new.Researcher_id = r.Researcher_id)
then
signal sqlstate '45000';
end if;
end$$
DELIMITER ;


DELIMITER $$

create trigger org_insert_type after insert on Organizations
for each row 
begin
		if new.Org_type = 'University'
			then insert into University  values(new.Organization_id,null);
		 else if new.Org_type = 'Corporation'
			then insert into corporation values(new.Organization_id,null);
		 else if new.Org_type = 'Research_center'
			then insert into Research_center values(new.Organization_id,null,null);
	else signal sqlstate '02000' set message_text = 'Wrong type!!';
    end if;
    end if;
    end if;
    end$$*/
    
DELIMITER ;

DELIMITER $$
create trigger duration_check before insert on Project
for each row
begin 
if (select TIMESTAMPDIFF(Year, new.Start_date, new.End_Date)) not in (1,2,3,4)
then
signal sqlstate '45000';
end if;
end$$

 

 
 




    
				