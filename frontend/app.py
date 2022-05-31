from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import yaml

app = Flask(__name__)


db = yaml.safe_load(open('db.yaml'))
#configure db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



buffer = []
buffer_2 = []
action = 0
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/page_1.html', methods=['GET', 'POST'])
def page_1():
    cur = mysql.connection.cursor()
    program_names_res = cur.execute("select Program_name from Program")
    program_names = cur.fetchall()
    
    if request.method == 'POST':
        input_data = request.form
        start_date = input_data['start_date']
        if start_date == '': 
            start_date = None
        end_date = input_data['end_date']
        if end_date == '': 
            end_date = None
        duration = input_data['duration']
        if duration == '':
            duration = None
        ex_f_name = input_data['ex_f_name']
        if ex_f_name == '':
            ex_f_name = None
        ex_l_name = input_data['ex_l_name']
        if ex_l_name == '':
            ex_l_name = None  
        cur = mysql.connection.cursor()
        project_res = cur.execute(
            """
            select  p.Title 
            from Project p 
            where 
            (case 
                when %(x)s is not null then p.Start_date = %(x)s
                when %(y)s is not null then p.End_date = %(y)s
                when %(z)s is not null then timestampdiff(year,p.Start_date,p.End_date) = %(z)s
                when %(e)s is not null then p.Executive_id = (select e.Executive_id 
                                        from Executive e
                                        where e.Last_name = %(e)s)
                when %(w)s is not null then  p.Executive_id = (select e.Executive_id 
                                        from Executive e
                                        where e.First_name = %(w)s)
                else p.Title = p.Title 
            end)            
            """,{'x': start_date,'y': end_date,'z': duration,'w': ex_f_name,'e': ex_l_name})
        project_titles = cur.fetchall()
        global buffer 
        buffer = project_titles
        return redirect('/page_1_1.html')    
    return render_template('/page_1.html', program_names=program_names)

@app.route('/page_1_1.html', methods=['GET', 'POST'])
def page_1_1():
    global buffer
    if request.method == 'POST':
        project_tuple = request.form
        project = project_tuple['project']
        cur = mysql.connection.cursor()
        project_res = cur.execute(
            """
             select concat(r.First_name," ",r.Last_name) as fullname from
            Works_on_project wp 
            inner join Researcher r
            on r.Researcher_id = wp.Researcher_id
            where wp.Project_id = (select Project_id from Project where Title = %(x)s)
            """,{'x': project})
        researcher_names = cur.fetchall()
        return render_template('/page_1_1.html', project_titles=buffer, researcher_names=researcher_names)
    
    return render_template('/page_1_1.html', project_titles=buffer, researcher_names=[])



@app.route('/page_2_1.html')
def page_2_1():
    return render_template('page_2_1.html')

@app.route('/page_2_2.html')
def page_2_2():
    return render_template('page_2_2.html')

@app.route('/page_2.html')
def page_2():
    return render_template('page_2.html')

@app.route('/page_3.html', methods=['GET', 'POST'] )
def page_3():                                                                
    cur = mysql.connection.cursor()
    sf_field_res = cur.execute("select sf_name from Scientific_field")
    sf = cur.fetchall()
    if request.method == 'POST':
        field_tup = request.form
        field = field_tup['sf']
        cur = mysql.connection.cursor()
        sf_field_res = cur.execute(
            """
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
            where sf.Sf_name = %(x)s and e.Grade >= 50   /**/
            and p.Start_date <= curdate() and (timestampdiff(year,curdate(),p.End_date))
            """,{'x':field})                                     
        tup = cur.fetchall()  
        return render_template('page_3.html', sf=sf, related=tup)             
    return render_template('page_3.html', sf=sf, related=[])

@app.route('/page_4.html')
def page_4():                                                              
    cur = mysql.connection.cursor()
    res = cur.execute(
        """
        select p1.organization_name
        from per_year p1
        inner join per_year p2 
        on p1.year_of_project = p2.year_of_project + 1
        where p1.organization_name = p2.organization_name 
        and p1.proj_count = p2.proj_count
        """)   
    if res == 0:
        print("No results")                                                
    tuples = cur.fetchall() 
    return render_template('page_4.html', tuples=tuples)                         

@app.route('/page_5.html')
def page_5():                                                                
    cur = mysql.connection.cursor()
    res = cur.execute(
        """
        select concat(sf1.Sf_name,", ",sf2.Sf_name) as Combinations
	    from Scientific_field sf1
	    inner join field_pairs p
	    on sf1.Scientific_field_id = p.first_field
	    inner join Scientific_field sf2
	    on sf2.Scientific_field_id = p.second_field
        """)                                                   
    tuples = cur.fetchall() 
    return render_template('page_5.html', tuples=tuples)                        


@app.route('/page_6.html')
def page_6():                                                                
    cur = mysql.connection.cursor()
    res = cur.execute(
        """
        select concat(r.First_name," ",r.Last_name) as fullname, re.counter
        from 
	    young_researchers re
        inner join Researcher r
        on r.Researcher_id = re.rid
        where re.counter = (select counter from young_researchers limit 1);
        """)                                                   
    tuples = cur.fetchall() 
    return render_template('page_6.html', tuples=tuples)                         

@app.route('/page_7.html')  
def page_7():                                                                
    cur = mysql.connection.cursor()
    res = cur.execute(
        """
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
        on e.Executive_id = Exec
        """)                                                  
    tuples = cur.fetchall() 
    return render_template('page_7.html', tuples=tuples)                         

@app.route('/page_8.html')
def page_8():                                                                
    cur = mysql.connection.cursor()
    res = cur.execute(
        """
        select concat(r.First_name," ",r.Last_name) as full_name, total_projects 
        from
        (select wp.Researcher_id as rid, count(*) as total_projects
        from works_on_project wp
        where wp.Project_id not in (select Project_id from Deliverable)
        group by wp.Researcher_id
        having total_projects >= 5) der 
        inner join Researcher r 
        on r.Researcher_id = rid
        """)                                                   
    tuples = cur.fetchall() 
    return render_template('page_8.html', tuples=tuples)                         

@app.route('/page_9.html', methods=['GET', 'POST'])
def page_9():
    if request.method == 'POST':
        table = int(request.form['table'])
        print(table)
        if table == 1:
            return redirect('/sf.html')
        if table == 2:
            return redirect('/executive.html')
        if table == 3:
            return redirect('/program.html')
        if table == 4:
            return redirect('/organization.html')
        if table == 5:
            return redirect('/researcher.html')
        if table == 6:
            return redirect('/project.html')
        if table == 7:
             return redirect('/evaluation.html')
        if table == 8:
            return redirect('/deliverable.html')
        if table == 9:
            return redirect('/works_on_project.html')
        if table == 10:
            return redirect('/phones.html')
        if table == 11:
            return redirect('/sf_belongs.html')
        if table == 12:
            return redirect('/university.html')
        if table == 13:
            return redirect('/corporation.html')
        if table == 14:
            return redirect('research_center.html')
    return render_template('page_9.html')

@app.route('/sf.html', methods=['GET', 'POST']) #checked 
def sf():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            d = request.form
            sf = d['sf']
            cur = mysql.connection.cursor()
            res = cur.execute("""insert into Scientific_field(Scientific_field_id, Sf_name) values(NULL, %(x)s)""", {'x': sf})
            mysql.connection.commit()
            cur.close()
            return render_template('sf.html')
        if update is not None:
            d = request.form
            new_sf = d['new_sf']
            old_sf = d['old_sf']
            cur = mysql.connection.cursor()
            res = cur.execute("""Update Scientific_field set Sf_name = %(y)s where  Sf_name = %(x)s""", {'x': old_sf,'y': new_sf})
            mysql.connection.commit()
            cur.close()
            return render_template('sf.html')
        if delete is not None:
            d = request.form
            sf = d['sf']
            cur = mysql.connection.cursor()
            res = cur.execute("""Delete from Scientific_field where Sf_name = %(y)s""", {'y': sf})
            mysql.connection.commit()
            cur.close()
            return render_template('sf.html')
    return render_template('sf.html')
    

@app.route('/program.html', methods=['GET', 'POST']) #checked
def program():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert:")
            d = request.form
            pr_name = d['pr_name']
            pr_sec = d['pr_sec']
            cur = mysql.connection.cursor()
            res = cur.execute("""insert into Program(Program_id,Program_name,Program_section) values(NULL, %(x)s, %(y)s)""", {'x': pr_name, 'y': pr_sec})
            mysql.connection.commit()
            cur.close()
            return render_template('program.html')
        if update is not None:
            print("update:")
            d = request.form
            new_pr_name = d['new_pr_name']
            new_pr_sec = d['new_pr_sec']
            old_pr_name = d['old_pr_name']
            cur = mysql.connection.cursor()
            if new_pr_sec != '' :
                res = cur.execute("""UPDATE Program set Program_section =  %(x)s  where Program_name = %(y)s""", {'x': new_pr_sec,'y': old_pr_name})
            if new_pr_name != '':
                res = cur.execute("""UPDATE Program set Program_name =  %(x)s  where Program_name = %(y)s""", {'x': new_pr_name,'y': old_pr_name})
            mysql.connection.commit()
            cur.close()
            return render_template('program.html')
        if delete is not None:
            print("delete:")
            d = request.form
            pr_name = d['pr_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""DELETE FROM Program WHERE Program_name =  %(x)s """, {'x':pr_name})
            mysql.connection.commit()
            cur.close()
            return render_template('program.html')
    return render_template('program.html')

@app.route('/executive.html', methods=['GET', 'POST']) #checked
def executive():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert:")
            d = request.form
            ex_f_name = d['ex_f_name']
            ex_l_name = d['ex_l_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""Insert into Executive (Executive_id, First_name, Last_name) values(null,%(x)s,%(y)s )""", {'x':ex_f_name,'y': ex_l_name})
            mysql.connection.commit()
            cur.close()
            return render_template('executive.html')
        if update is not None:
            print("update:")
            d = request.form
            new_ex_f_name = d['new_ex_f_name']
            new_ex_l_name = d['new_ex_l_name']
            old_ex_f_name = d['old_ex_f_name']
            old_ex_l_name = d['old_ex_l_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""Update Executive  set  First_name = %(x)s , Last_name = %(y)s 
                                 where First_name = %(z)s and Last_name = %(w)s""", {'x':new_ex_f_name,'y': new_ex_l_name,'z':old_ex_f_name,'w':old_ex_l_name})
            mysql.connection.commit()
            cur.close()
            return render_template('executive.html')
        if delete is not None:
            print("delete:")
            d = request.form
            ex_f_name = d['ex_f_name']
            ex_l_name = d['ex_l_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""Delete from Executive where First_name = %(x)s and Last_name = %(y)s""", {'x':ex_f_name,'y': ex_l_name})
            mysql.connection.commit()
            cur.close()
            return render_template('executive.html')
    return render_template('executive.html')

@app.route('/researcher.html', methods=['GET', 'POST']) #checked
def researher():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print('insert')
            d = request.form
            r_f_name = d['r_f_name']
            r_l_name = d['r_l_name']
            r_sex = d['r_sex']
            r_bday = d['r_bday']
            r_org = d['r_org']
            st_d_work_org = d['st_d_work_org']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Organization_id from Organizations where Org_name = %(o)s)""",{'o':r_org})
            res = cur.execute("""Insert into Researcher(Researcher_id, First_name, Last_name, Birthdate, Sex, Start_date_work_org,Organization_id)  
            values(null,%(x)s,%(y)s,%(w)s,%(z)s,%(q)s,@Udata) """, {'x':r_f_name,'y': r_l_name,'z':r_sex,'w':r_bday,'q':st_d_work_org})
            mysql.connection.commit()
            cur.close()
            return render_template('researcher.html')
        if update is not None:
            print('update')
            d = request.form
            r_f_name = d['r_f_name']
            r_l_name = d['r_l_name']
            r_sex = d['r_sex']
            r_bday = d['r_bday']
            r_org = d['r_org']
            st_d_work_org = d['st_d_work_org']
            old_r_f_name = d['old_r_f_name']
            old_r_l_name = d['old_r_l_name']
            old_r_bday = d['old_r_bday']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Organization_id from Organizations where Org_name = %(o)s)""",{'o':r_org})
            res = cur.execute("""set @old_f_name = %(o)s""",{'o':old_r_f_name})
            res = cur.execute("""set @old_l_name = %(o)s""",{'o':old_r_l_name})
            res = cur.execute("""set @old_bday = %(o)s""",{'o':old_r_bday})
            if r_l_name!= '':
                res = cur.execute("""Update Researcher set Last_name = %(x)s where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """, {'x':r_l_name})
                res = cur.execute("""set @old_l_name = %(o)s""",{'o':r_l_name})
            if r_f_name!= '':
                res = cur.execute("""Update Researcher set First_name = %(x)s where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """, {'x':r_f_name})
                res = cur.execute("""set @old_f_name = %(o)s""",{'o':r_f_name})
            if r_bday!= '':
                res = cur.execute("""Update Researcher set Birthdate = %(x)s where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """, {'x':r_bday})
                res = cur.execute("""set @old_bday = %(o)s""",{'o':r_bday})
            if r_sex != '':
                res = cur.execute("""Update Researcher set Sex = %(x)s where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """, {'x':r_sex})
            if st_d_work_org != '':
                res = cur.execute("""Update Researcher set Start_date_work_org = %(x)s where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """, {'x':st_d_work_org})
            if r_org != '':
                res = cur.execute("""Update Researcher set Organization_id = @Udata where First_name = @old_f_name and Last_name = @old_l_name
                                    and Birthdate = @old_bday """)
            mysql.connection.commit()
            cur.close()
            return render_template('researcher.html')
        if delete is not None:
            print('delete')
            d = request.form
            r_f_name = d['r_f_name']
            r_l_name = d['r_l_name']
            r_bday = d['r_bday']
            cur = mysql.connection.cursor()
            res = cur.execute(""" Delete from Researcher where First_name = %(x)s 
                              and Last_name = %(y)s and Birthdate = %(z)s""",{'x':r_f_name,'y':r_l_name,'z':r_bday})
            mysql.connection.commit()
            cur.close()
            return render_template('researcher.html')
    return render_template('researcher.html')


@app.route('/phones.html', methods=['GET', 'POST']) #checked
def phones():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            ph = d['ph']
            org = d['org']
            cur = mysql.connection.cursor()     
            res = cur.execute("""set @UDATA = (select Organization_id from Organizations where Org_name = %(y)s)""", {'y': org})
            res = cur.execute("""Insert into Organization_phones(Phone_number, Organization_id) 
                              values(%(x)s, @UDATA)""", {'x':ph})
            mysql.connection.commit()
            cur.close()
            return render_template('phones.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            new_ph = d['new_ph']
            new_org = d['new_org']
            old_ph = d['old_ph']
            old_org = d['old_org']
            cur = mysql.connection.cursor()     
            res = cur.execute("""set @UDATA = (select Organization_id from Organizations where Org_name = %(y)s)""", {'y': new_org })
            res = cur.execute("""UPDATE Organization_phones set Phone_number = %(x)s , Organization_id = @UDATA 
                               where Phone_number = %(z)s""", {'x':new_ph, 'z':old_ph})
            mysql.connection.commit()
            cur.close()
            return render_template('phones.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            ph = d['ph']
            cur = mysql.connection.cursor()     
            res = cur.execute("""DELETE FROM Organization_phones where Phone_number = %(x)s""", {'x':ph})
            mysql.connection.commit()
            cur.close()
            return render_template('phones.html')
    return render_template('phones.html')

@app.route('/works_on_project.html', methods=['GET', 'POST']) #checked
def works_on_project():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            pr = d['pr']
            f_name = d['f_name']
            l_name= d['l_name']
            br = d['br']
            cur = mysql.connection.cursor()     
            res = cur.execute("""set @UDATA = (select Project_id from Project where Title = %(y)s)""", {'y': pr })
            res = cur.execute("""set @UDATA2 = (select Researcher_id from Researcher where First_name = %(y)s and Last_name = %(x)s and Birthdate = %(z)s)""",
             {'y': f_name,'x': l_name,'z': br })
            res = cur.execute("""INSERT INTO Works_on_Project(Project_id,Researcher_id) values(@UDATA , @UDATA2) """)
            mysql.connection.commit()
            cur.close()
            return render_template('works_on_project.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            pr = d['pr']
            f_name = d['f_name']
            l_name= d['l_name']
            br = d['br']
            cur = mysql.connection.cursor()     
            res = cur.execute("""set @UDATA = (select Project_id from Project where Title = %(y)s)""", {'y': pr })
            res = cur.execute("""set @UDATA2 = (select Researcher_id from Researcher where First_name = %(y)s and Last_name = %(x)s and Birthdate = %(z)s)""",
             {'y': f_name,'x': l_name,'z': br })
            res = cur.execute("""DELETE FROM Works_on_Project WHERE Project_id = @UDATA and Researcher_id = @UDATA2 """)
            mysql.connection.commit()
            cur.close()
            return render_template('works_on_project.html')
    return render_template('works_on_project.html')

@app.route('/organization.html', methods=['GET', 'POST']) #checked
def organization():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            org_name = d['org_name']
            abr = d['abr']
            ps = d['ps']
            stre = d['str']
            city = d['city']
            org_type = d['type']

            cur = mysql.connection.cursor()
            res = cur.execute("""Insert into Organizations(Organization_id, Org_name, Abbreviation, Post_code, Street, City, Org_type)
                                 values(null,%(x)s, %(y)s,%(z)s,%(w)s,%(f)s,%(o)s)""", {'x': org_name,'y': abr, 'z': ps, 'w':stre, 'f':city, 'o':org_type})
            mysql.connection.commit()
            cur.close()
            return render_template('organization.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            org_name = d['org_name']
            abr = d['abr']
            ps = d['ps']
            stre = d['str']
            city = d['city']
            org_type = d['type']
            old_org_name = d['old_org_name']
            cur = mysql.connection.cursor()
            if abr != '':
                res = cur.execute("""UPDATE Organizations set Abbreviation = %(o)s where Org_name = %(x)s""", {'o': abr,'x':old_org_name})
            if ps != '':
                res = cur.execute("""UPDATE Organizations set Post_code = %(o)s where Org_name = %(x)s""", {'o': ps,'x':old_org_name})
            if stre != '':
                res = cur.execute("""UPDATE Organizations set Street = %(o)s where Org_name = %(x)s""", {'o': stre,'x':old_org_name})
            if city != '':
                res = cur.execute("""UPDATE Organizations set City = %(o)s where Org_name = %(x)s""", {'o': city,'x':old_org_name})
            if org_name != '':
                res = cur.execute("""UPDATE Organizations set Org_name = %(o)s where Org_name = %(x)s""", {'o': org_name,'x':old_org_name})
            mysql.connection.commit()
            cur.close()
            return render_template('organization.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            org_name = d['org_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""Delete from Organizations where Org_name = %(o)s""", {'o': org_name})
            mysql.connection.commit()
            cur.close()
            #get vars for dict d
            #add here queries
            return render_template('organization.html')
    return render_template('organization.html')

@app.route('/deliverable.html', methods=['GET', 'POST']) #checked
def deliverable():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            title = d['title']
            pr = d['pr']
            del_desc = d['del_desc']
            del_date = d['del_date']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @udata = (select project_id from Project where title = %(x)s)""",{'x':pr})
            res = cur.execute("""insert into deliverable(deliverable_id,project_id,Title,deliv_description,Delivery_date) 
                                values(null, @udata,%(x)s,%(y)s,%(z)s)""",{'x':title,'y':del_desc,'z':del_date})
            mysql.connection.commit()
            cur.close()
            return render_template('deliverable.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            title = d['title']
            pr = d['pr']
            del_desc = d['del_desc']
            del_date = d['del_date']
            old_title = d['old_title']
            old_pr = d['old_pr']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @udata = (select project_id from Project where title = %(x)s)""",{'x':pr})
            if del_desc != '':
                res = cur.execute("""update deliverable set deliv_description = %(x)s 
                                  where Title = %(y)s and Project_id = @udata""",{'x':del_desc,'y':old_title})
            if del_date != '':
                res = cur.execute("""update deliverable set delivery_date = %(x)s 
                                  where Title = %(y)s and Project_id = @udata""",{'x':del_date,'y':old_title})
            if title != '':
                res = cur.execute("""update deliverable set title = %(x)s 
                                  where Title = %(y)s and Project_id = @udata""",{'x':title,'y':old_title})
            mysql.connection.commit()
            cur.close()
            return render_template('deliverable.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            title = d['title']
            pr = d['pr']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @udata = (select project_id from Project where title = %(x)s)""",{'x':pr})
            res = cur.execute("""delete from deliverable where title = %(x)s and Project_id = @udata""",{'x':title})
            mysql.connection.commit()
            cur.close()
            return render_template('deliverable.html')
    return render_template('deliverable.html')

@app.route('/evaluation.html', methods=['GET', 'POST']) #checked
def evaluation():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('evaluation.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            eval_date = d['eval_date']
            grade = d['grade']
            pr_name = d['pr_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @udata = (select evaluation_id from Project where Title = %(o)s)""", {'o': pr_name})
            if eval_date != '':
                res = cur.execute("""update evaluation set eval_date = %(o)s where evaluation_id = @udata""",{'o':eval_date})
            if grade != '':
                res = cur.execute("""update evaluation set grade = %(o)s where evaluation_id = @udata""",{'o':grade})
            mysql.connection.commit()
            cur.close()
            return render_template('evaluation.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            pr_name = d['pr_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @udata = (select evaluation_id from Project where Title = %(o)s)""", {'o': pr_name})
            res = cur.execute("""delete from evaluation where evaluation_id = @udata""")
            mysql.connection.commit()
            cur.close()
            return render_template('evaluation.html')
    return render_template('evaluation.html')

@app.route('/project.html', methods=['GET', 'POST']) #checked
def project():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        update = request.form.get("update")
        if insert is not None:
            print("insert")
            d = request.form
            print(d)
            title = d['title']
            amount = d['amount']
            start_date = d['start_date']
            end_date = d['end_date']
            pr_desc = d['pr_desc']
            eval_date = d['eval_date']
            eval_grade = d['eval_grade']
            eval_f_name = d['eval_f_name']
            eval_l_name = d['eval_l_name']
            eval_bday = d['eval_bday']
            org_name = d['org_name']
            pr_name = d['pr_name']
            l_r_f_n = d['l_r_f_n']
            l_r_l_n = d['l_r_l_n']
            l_r_bd = d['l_r_bd']
            ex_f_name = d['ex_f_name']
            ex_l_name = d['ex_l_name']
            if eval_date == '':
                eval_date = None
            if amount == '':
                amount = None
            if pr_desc == '':
                pr_desc = None
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Program_data = (select Program_id from Program where Program_name = %(c)s)""",{'c':pr_name})
            res = cur.execute("""set @Researcher = (select Researcher_id from Researcher where 
                        First_name = %(x)s and Last_name = %(y)s and Birthdate = %(z)s) """,{'x':l_r_f_n,'y':l_r_l_n,'z':l_r_bd})
            res = cur.execute("""set @Executive = (select Executive_id from Executive where First_name = %(x)s
            and Last_name = %(y)s) """,{'x':ex_f_name,'y':ex_l_name})
            res = cur.execute("""set @udata = (select Researcher_id from Researcher where First_name = %(c)s
                             AND last_name = %(v)s and Birthdate = %(b)s)""",{'c':eval_f_name,'v':eval_l_name,'b':eval_bday})
            res = cur.execute("""set @udata2 = (select Organization_id from Organizations where org_name = %(x)s) """,{'x':org_name})
            res = cur.execute("""Insert into Evaluation(Evaluation_id,Eval_date, Grade, Researcher_id, Organization_id)
                              values(null,%(x)s,%(y)s,@udata,@udata2)""",{'x':eval_date,'y':eval_grade})
            res = cur.execute("""set @Eval_data = 
                            (select Evaluation_id from Evaluation order by Evaluation_id DESC limit 1) """)                   
            res = cur.execute("""Insert into Project(Project_id,Amount,Title,Start_date,End_date,Project_description,
                             Evaluation_id,Program_id,Researcher_id,Executive_id,Organization_id) 
                             values(null,%(x)s,%(y)s,%(z)s,%(w)s,%(r)s,@Eval_data,@Program_data,@Researcher,@Executive,@udata2)
                              """,{'x':amount,'y':title,'z':start_date,'w':end_date,'r':pr_desc})
            mysql.connection.commit()
            cur.close()                  
            return render_template('project.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            old_pr = d['old_pr']
            title = d['title']
            amount = d['amount']
            start_date = d['start_date']
            end_date = d['end_date']
            pr_desc = d['pr_desc']
            org_name = d['org_name']
            pr_name = d['pr_name']
            l_r_f_n = d['l_r_f_n']
            l_r_l_n = d['l_r_l_n']
            l_r_bd = d['l_r_bd']
            ex_f_name = d['ex_f_name']
            ex_l_name = d['ex_l_name']
            cur = mysql.connection.cursor()
            if amount != '':
                res = cur.execute("""Update Project set Amount = %(a)s where Title = %(b)s""",{'a':amount,'b':old_pr})
            if start_date != '':
                res = cur.execute("""Update Project set Start_date = %(a)s where Title = %(b)s
                """,{'a':start_date,'b':old_pr})
            if end_date != '':
                res = cur.execute("""Update Project set End_date = %(a)s 
                where title = %(b)s""",{'a':end_date,'b':old_pr})
            if pr_desc != '':
                res = cur.execute("""Update Project set Project_description = %(a)s 
                where title = %(b)s""",{'a':pr_desc,'b':old_pr})
            if org_name != '':
               res = cur.execute("""set @Organization = (select Organization_id from Organizations 
                         where Org_name = %(x)s)""",{'x':org_name})
               res = cur.execute("""Update Project set Organization_id = @Organization 
               where title = %(b)s""",{'b':old_pr})
            if l_r_f_n != '' and l_r_l_n !='' and l_r_bd != '':
               res = cur.execute("""set @Researcher = (select Researcher_id from Researcher where First_name = %(x)s and
                                    Last_name = %(y)s and Birthdate = %(z)s)""",{'x':l_r_f_n,'y':l_r_l_n,'z':l_r_bd})
               res = cur.execute("""Update Project set Researcher_id = @Researcher 
               where title = %(b)s""",{'b':old_pr})
            if ex_f_name != '' and ex_l_name != '':
               res = cur.execute("""set @Executive = (select Executive_id from Executive where First_name = %(x)s and
                        Last_name = %(y)s)""",{'x':ex_f_name,'y':ex_l_name})
               res = cur.execute("""Update Project set Executive_id = @Executive 
               where title = %(b)s""",{'b':old_pr})
            if pr_name != '':
                res = cur.execute("""set @Program = (select Program_id from Program where Program_name = %(x)s)""",{'x':pr_name})
                res = cur.execute("""Update Project set Program_id = @Program where title = %(a)s""",{'a':old_pr})
            if title != '':
                res = cur.execute("""Update Project set Title = %(a)s where Title = %(b)s """,{'a':title,'b':old_pr})
            mysql.connection.commit()
            cur.close()
            return render_template('project.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            pr_title = d['pr_title']
            cur = mysql.connection.cursor()
            res = cur.execute("""Delete from Project where Title = %(x)s""",{'x':pr_title})
            mysql.connection.commit()
            cur.close()
            return render_template('project.html')
    return render_template('project.html')

@app.route('/sf_belongs.html', methods=['GET', 'POST'])
def sf_belongs():
    if request.method == 'POST':
        insert = request.form.get("insert")
        delete = request.form.get("delete")
        if insert is not None:
            print("insert")
            d = request.form
            sf = d['sf']
            pr_name = d['pr_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Scientific_field_id from Scientific_field where Sf_name = %(x)s)""",{'x': sf})
            res = cur.execute("""set @Udata2 = (select Project_id from Project where Title = %(y)s)""",{'y':pr_name})
            res = cur.execute("""insert into sf_belongs(Project_id, Scientific_field_id) 
            values(@Udata2, @Udata)""")
            mysql.connection.commit()
            cur.close()
            print(d)
            return render_template('/sf_belongs.html')
        if delete is not None:
            print("delete")
            d = request.form
            sf = d['sf']
            pr_name = d['pr_name']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Scientific_field_id from Scientific_field where Sf_name = %(x)s)""",{'x': sf})
            res = cur.execute("""set @Udata2 = (select Project_id from Project where Title = %(y)s)""",{'y':pr_name})
            res = cur.execute("""delete from Sf_belongs where Scientific_field_id = @Udata and Project_id = @Udata2""")
            mysql.connection.commit()
            cur.close()
            print(d)
            return render_template('/sf_belongs.html')
    return render_template('/sf_belongs.html')

@app.route('/university.html', methods=['GET', 'POST'])
def university():
    if request.method == 'POST':
        update = request.form.get("update")
        if update is not None:
            print("update")
            d = request.form
            print(d)
            org_name = d['org_name']
            budget = d['new_budget_ministry']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Organization_id from Organizations where Org_name = %(x)s)""",{'x': org_name})
            res = cur.execute("""update University set Budget_ministry = %(x)s where Organization_id = @Udata""",{'x':budget})
            mysql.connection.commit()
            cur.close()
            return render_template('/university.html')
    return render_template('/university.html')

@app.route('/corporation.html', methods=['GET', 'POST'])
def corporation():
    if request.method == 'POST':
        insert = request.form.get("insert")
        update = request.form.get("update")
        delete = request.form.get("delete")
        if update is not None:
            print("update")
            d = request.form
            print(d)
            org_name = d['org_name']
            equity  = d['new_equity']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Organization_id from Organizations where Org_name = %(x)s)""",{'x': org_name})
            res = cur.execute("""update Corporation set equity = %(x)s where Organization_id = @Udata""",{'x': equity})
            mysql.connection.commit()
            cur.close()
            return render_template('/corporation.html')
    return render_template('/corporation.html')

@app.route('/research_center.html', methods=['GET', 'POST'])
def research_center():
    if request.method == 'POST':
        insert = request.form.get("insert")
        update = request.form.get("update")
        delete = request.form.get("delete")
        if update is not None:
            print("update")
            d = request.form
            print(d)
            org_name = d['org_name']
            budget_min = d['new_budget_ministry']
            budget_pri = d['new_budget_private_actions']
            cur = mysql.connection.cursor()
            res = cur.execute("""set @Udata = (select Organization_id from Organizations where Org_name = %(x)s)""",{'x': org_name})
            if budget_min != '':
                res = cur.execute("""update Research_center set Budget_ministry = %(x)s where Organization_id = @Udata""",{'x': budget_min})
            if budget_pri !='':
                res = cur.execute("""update Research_center set Budget_private = %(x)s where Organization_id = @Udata""",{'x': budget_pri})
            mysql.connection.commit()
            cur.close()
            return render_template('/research_center.html')
    return render_template('/research_center.html')

if __name__ == '__main__':
    app.run(debug=True)