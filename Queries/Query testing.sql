drop view per_year;
create view per_year 
(year_of_project, organization_name, proj_count)
as 
	select year(p.Start_date) as year_of_project ,org1.Org_name as organization_name, count(*) as proj_count
		from Organizations org1 
		inner join Project p 
		on p.Organization_id = org1.Organization_id
		group by year_of_project, organization_name
		having proj_count < 10 ;
        
select organization_name
from per_year p1
inner join per_year p2 
on p1.year_of_project = p2.year_of_project + 1
where p1.organization_name = p2.organization_name 
and p1.proj_count = p2.proj_count;
        
        

