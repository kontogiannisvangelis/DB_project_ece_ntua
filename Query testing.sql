create view per_year 
(year_of_project, organization_name, proj_count, pair_of_years)
as 
	select year(p.Start_date) as year_of_project ,org1.Org_name as organization_name, count(*) as proj_count, (year(p.Start_date) + year(p.Start_date)+1) as pair_of_years
		from Organizations org1 
		inner join Project p 
		on p.Organization_id = org1.Organization_id
		group by year_of_project, organization_name
		having proj_count < 10 ;

