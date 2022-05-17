DROP SCHEMA IF EXISTS eldik_db;
CREATE SCHEMA eldik_db;
USE eldik_db;

create table Organizations(
	Organization_id varchar(10),
    Org_name varchar(50),
    Post_code smallint(5),
    Street varchar(20),
    City varchar(20),
    Org_type varchar(20),
    primary key (Organization_id)
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Research_center(
	Organization_id varchar(10),
    Budget_ministry int,
    Budget_private int,
    primary key(Organization_id),
    foreign key (Organization_id) references Organizations(Organization_id)
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    

create table Researcher(
	Researcher_id varchar(10), 
    First_name varchar(20),
	Last_name varchar(20),
	Birthdate date,
    Sex varchar(20),
    Start_date_work_org date,
    Organization_id varchar(10), 
    primary key (Researcher_id),
    foreign key (Organization_id) references Organizations(Organization_id)
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table University(
	Organization_id varchar(10),
    Budget_ministry int,
    primary key(Organization_id),
    foreign key (Organization_id) references Organizations(Organization_id)
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Coorporation(
	Organization_id varchar(10),
    Equity int,
    primary key(Organization_id),
    foreign key (Organization_id) references Organizations(Organization_id)
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Evaluation(
	Evaluation_id varchar(10), 
	Eval_date date,
    Grade varchar(2),
    Researcher_id varchar(10),
    primary key(Evaluation_id),
    foreign key(Researcher_id) references Researcher(Researcher_id)
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    

    
create table Organization_phones(
	Phone_number varchar(10),
    Organization_id varchar(10),
    primary key(Phone_number),
	foreign key (Organization_id) references Organizations(Organization_id) 
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Program(
	Program_id varchar(10),
	Program_name varchar(20),
	Program_section varchar(20),
    primary key(Program_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Executive(
	Executive_id varchar(10),
    First_name varchar(20),
    Last_name varchar(20),
    primary key (Executive_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    

    
create table Scientific_field(
	Scientific_field_id varchar(10),
    Sf_name varchar(20),
    primary key(Scientific_field_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table Project(
	Project_id varchar(10),
	Amount int,
	Start_Date date,
	End_Date date ,
    Project_description Varchar(400),
    #Duration derived
    Evaluation_id varchar(10),
    Program_id varchar(10),
    Researcher_id varchar(10),
    Executive_id varchar(10) ,
	Organization_id varchar(10),
    primary key (Project_id),
    foreign key(Executive_id) references Executive(Executive_id) ,
    foreign key(Program_id) references Program(Program_id),
    foreign key(Researcher_id) references Researcher(Researcher_id),
    foreign key(Evaluation_id) references Evaluation(Evaluation_id),
    foreign key(Organization_id) references Organizations(Organization_id)
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Works_on_project(
	Project_id varchar(10),
    Researcher_id varchar(10),
    primary key(Project_id, Researcher_id),
	foreign key(Researcher_id) references Researcher(Researcher_id),
    foreign key(Project_id) references Project(Project_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
    create table Sf_belongs(
	Project_id varchar(10),
    Scientific_field_id varchar(10),
    primary key(Project_id,Scientific_field_id),
    foreign key(Scientific_field_id) references Scientific_field(Scientific_field_id),
    foreign key(Project_id) references Project(Project_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Deliverable(
	Deliverable_id varchar(10),
    Project_id varchar(10),
    Title varchar(20),
    Deliv_description varchar(400),
    Delivery_date date,
    primary key (Deliverable_id, Project_id),
    foreign key(Project_id) references Project(Project_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


    
				