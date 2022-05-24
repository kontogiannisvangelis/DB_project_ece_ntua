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
	where sf.Sf_name = @Udata_intresting_field and e.Grade >= 50   /*User data used*/
    and p.Start_date <= '2017-04-04' <= p.End_date ;

