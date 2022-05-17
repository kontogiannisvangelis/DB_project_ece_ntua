DROP SCHEMA IF EXISTS eldik_db;
CREATE SCHEMA eldik_db;
USE eldik_db;

create table Organizations(
	Organization_id int unsigned auto_increment,
    Org_name varchar(50) not null,
    Post_code smallint(5) default null,
    Street varchar(20) default null,
    City varchar(20) not null,
    Org_type varchar(20) not null,
    primary key (Organization_id)
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Researcher(
	Researcher_id int unsigned  auto_increment, 
    First_name varchar(20) not null,
	Last_name varchar(20) not null,
	Birthdate date not null,
    Sex varchar(20) default null, #politically correct
    Start_date_work_org date not null,
    Organization_id int unsigned, 
    primary key (Researcher_id),
    constraint fk_organization_id_researcher foreign key (Organization_id) references Organizations(Organization_id) on delete restrict on update cascade 
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Research_center(
	Organization_id int unsigned,
    Budget_ministry int default null,
    Budget_private int default null,
    primary key(Organization_id),
    constraint fk_organization_id_reaseach_center foreign key (Organization_id) references Organizations(Organization_id) on delete restrict on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table University(
	Organization_id int unsigned,
    Budget_ministry int default null,
    primary key(Organization_id),
    constraint fk_organization_id_university foreign key (Organization_id) references Organizations(Organization_id) on delete restrict on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Coorporation(
	Organization_id int unsigned,
    Equity int default null,
    primary key(Organization_id),
    constraint fk_organization_id_coorporation foreign key (Organization_id) references Organizations(Organization_id) on delete restrict on update cascade 
    #add triggers when changing organization
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Evaluation(
	Evaluation_id int unsigned  auto_increment, 
	Eval_date date not null,
    Grade varchar(2) default null,
    Researcher_id int unsigned,
    primary key(Evaluation_id),
    constraint fk_researcher_id_evaluation foreign key(Researcher_id) references Researcher(Researcher_id) on delete restrict on update cascade
    #more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Organization_phones(
	Phone_number int unsigned,
    Organization_id int unsigned not null,
    primary key(Phone_number),
	constraint fk_organization_id_phones foreign key (Organization_id) references Organizations(Organization_id) on delete restrict on update cascade 
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Program(
	Program_id int unsigned  auto_increment,
	Program_name varchar(20) not null,
	Program_section varchar(20),
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
	Amount int default null,
	Start_Date date default null,
	End_Date date  default null,
    Project_description Varchar(400) default null,
    #Duration derived
    Evaluation_id int unsigned not null,
    Program_id int unsigned not null,
    Researcher_id int unsigned not null ,
    Executive_id int unsigned not null ,
	Organization_id int unsigned not null,
    primary key (Project_id),
    constraint fk_executive_id_project foreign key(Executive_id) references Executive(Executive_id) on delete restrict on update cascade,
    constraint fk_program_id_project foreign key(Program_id) references Program(Program_id) on delete restrict on update cascade,
	constraint fk_researcher_id_project foreign key(Researcher_id) references Researcher(Researcher_id) on delete restrict on update cascade,
    constraint fk_evaluation_id_project foreign key(Evaluation_id) references Evaluation(Evaluation_id)on delete restrict on update cascade,
    constraint fk_organization_id_project foreign key(Organization_id) references Organizations(Organization_id) on delete restrict on update cascade
    #add more constrains
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
create table Works_on_project(
	Project_id int unsigned,
    Researcher_id int unsigned,
    primary key(Project_id, Researcher_id),
	constraint fk_researcher_id_work_on_project foreign key(Researcher_id) references Researcher(Researcher_id) on delete restrict on update cascade,
    constraint fk_project_id_works_on_project foreign key(Project_id) references Project(Project_id) on delete restrict on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
    create table Sf_belongs(
	Project_id int unsigned,
    Scientific_field_id int unsigned,
    primary key(Project_id,Scientific_field_id),
    constraint fk_sf_field_sf_belongs foreign key(Scientific_field_id) references Scientific_field(Scientific_field_id) on delete restrict on update cascade,
    constraint fk_project_id_sf_belongs foreign key(Project_id) references Project(Project_id) on delete restrict on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Deliverable(
	Deliverable_id int unsigned  auto_increment,
    Project_id int unsigned,
    Title varchar(20),
    Deliv_description varchar(400) default null,
    Delivery_date date not null ,
    primary key (Deliverable_id, Project_id),
    constraint fk_project_id_deliverable foreign key(Project_id) references Project(Project_id) on delete restrict on update cascade
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


    
				