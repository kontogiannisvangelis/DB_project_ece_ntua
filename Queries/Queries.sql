
/*Query 1*/
select Program_name from Program;

set @Udata_end_date = null;
set @Udata_start_date = null;
set @Udata_First_name = null;
set @Udata_Last_name = null;
set @Udata_duration_years = 4;

select  p.Title 
	from Project p 
	where 
    (case 
		when @Udata_end_date is not null then p.Start_date = @Udata_start_date 
		when @Udata_start_date is not null then p.End_date = @Udata_end_date 
		when @Udata_duration_years is not null then timestampdiff(year,p.Start_date,p.End_date) = @Udata_duration_years
		when @Udata_Last_name is not null then p.Executive_id = (select e.Executive_id 
								from Executive e
								where e.Last_name = @Udata_Last_name)
		when @Udata_First_name is not null then  p.Executive_id = (select e.Executive_id 
								from Executive e
								where e.First_name = @Udata_First_name)
	    else p.Title = p.Title 
	end); /*I have 3 "and" but maybe user gives only 1 condition in where clause ,
																	then we can make "attribute = Udata" a true value so only one condition is taken under consideration.
                                                                    For instance making Udata_first_name = "not null" then, where clause is true for all tuples for all 
															       first_names in Executive */
                                                                   
set @Udata_project_title = 'Random title 1';
 select concat(r.First_name," ",r.Last_name) as fullname from
 Works_on_project wp 
 inner join Researcher r
 on r.Researcher_id = wp.Researcher_id
 where wp.Project_id = (select Project_id from Project where Title = @Udata_project_title);
 
 
 
 
/*Query 2 */                                                                    
create view projects_per_researcher
	(researcher_fullname, project_title)
    as select concat(r.First_name," ",r.Last_name) , p.Title from 
    Works_on_project wp inner join Project p 
    on wp.Project_id = p.Project_id 
    inner join Researcher r 
    on r.Researcher_id = wp.Researcher_id
    order by r.First_name, r.Last_name ASC;
    
/*View to be included*/

/*Qyery 3 */
set @Udata_intresting_field = 'Physics';


 select p.Title, concat(r.First_name," ",r.Last_name) as full_name
	from Project p inner join Sf_belongs sfbelon
    on p.Project_id = sfbelon.Project_id
    inner join Scientific_field sf
    on sf.Scientific_field_id = sfbelon.Scientific_field_id
    inner join Works_on_project wp
    on wp.Project_id = p.Project_id 
    inner join Researcher r
    on r.Researcher_id = wp.Researcher_id
    inner join Evaluation e
    on e.Evaluation_id = p.Evaluation_id
	where sf.Sf_name = @Udata_intresting_field and e.Grade >= 50   /**/
    and p.Start_date <= curdate() and (timestampdiff(year,curdate(),p.End_date));

/*Query 4*/
create view per_year 
(year_of_project, organization_name, proj_count)
as 
	select year(p.Start_date) as year_of_project ,org1.Org_name as organization_name, count(*) as proj_count
		from Organizations org1 
		inner join Project p 
		on p.Organization_id = org1.Organization_id
		group by year_of_project, organization_name
		having proj_count >= 10 ;
        
select p1.organization_name
from per_year p1
inner join per_year p2 
on p1.year_of_project = p2.year_of_project + 1
where p1.organization_name = p2.organization_name 
and p1.proj_count = p2.proj_count;

/*Query 5 */
create view field_pairs 
(first_field,second_field,counter)
as 
	(select sf1.Scientific_field_id as first_field, sf2.Scientific_field_id as second_field, count(*) as counter
	from Sf_belongs sf1
    inner join Sf_belongs sf2
    on sf2.Project_id = sf1.Project_id
	group by sf1.Scientific_field_id, sf2.Scientific_field_id
    having sf1.Scientific_field_id > sf2.Scientific_field_id
    order by counter DESC
    limit 3);
    
select concat(sf1.Sf_name,", ",sf2.Sf_name) as Combinations
	from Scientific_field sf1
	inner join field_pairs p
	on sf1.Scientific_field_id = p.first_field
	inner join Scientific_field sf2
	on sf2.Scientific_field_id = p.second_field;
    
    
 /*Query 6 */   
create view young_researchers (rid,counter) as
	(select wp.Researcher_id as rid, count(*) as counter from
			Works_on_project wp
			group by wp.Researcher_id
			having wp.Researcher_id in 
			(select Researcher_id from Researcher r where year(curdate()) - year(r.Birthdate) <= 40)
			order by counter DESC);
            
select concat(r.First_name," ",r.Last_name) as fullname, re.counter
from 
	young_researchers re
    inner join Researcher r
    on r.Researcher_id = re.rid
where re.counter = (select counter from young_researchers limit 1);

/*Query 7 */
select concat(e.First_name," ",e.Last_name) as fullname, corp_name, total_amount
from  
	(select p.Executive_id as Exec, o.Org_name as corp_name, sum(p.Amount) as total_amount,o.Org_type
	from Project p
	inner join Organizations o
	on p.Organization_id = o.Organization_id
	group by p.Executive_id, o.Organization_id
	having o.Org_type = 'Corporation'
	order by total_amount DESC
	limit 5) der
    inner join Executive e
    on e.Executive_id = Exec;
  

/*Query 8 */
select concat(r.First_name," ",r.Last_name) as full_name, total_projects 
from
	(select wp.Researcher_id as rid, count(*) as total_projects
	from works_on_project wp
    where wp.Project_id not in (select Project_id from Deliverable)
	group by wp.Researcher_id
	having total_projects >= 5) der 
    inner join Researcher r 
    on r.Researcher_id = rid;





























    
    


	


    
    
    
    
    
    
    
    
	