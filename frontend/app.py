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
            return redirect('phones.html')
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
            sf = d['sf']
            cur = mysql.connection.cursor()
            res = cur.execute("""insert into Scientific_field(Scientific_field_id, Sf_name) values(NULL, %(x)s)""", {'x': sf})
            mysql.connection.commit()
            cur.close()
            #add here queries
            return render_template('program.html')
        if update is not None:
            print("update:")
            d = request.form
            #add here queries
            return render_template('program.html')
        if delete is not None:
            print("delete:")
            d = request.form
            #add here queries
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
            #add here queries
            return render_template('executive.html')
        if update is not None:
            print("update:")
            d = request.form
            #add here queries
            return render_template('executive.html')
        if delete is not None:
            print("delete:")
            d = request.form
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('researcher.html')
        if update is not None:
            print('update')
            d = request.form
            #get vars for dict d
            #add here queries
            return render_template('researcher.html')
        if delete is not None:
            print('delete')
            d = request.form
            #get vars for dict d
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('phones.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('phones.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('works_on_project.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('works_on_project.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('organization.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('organization.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
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
            #get vars for dict d
            #add here queries
            return render_template('deliverable.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('deliverable.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('evaluation.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
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
            #get vars for dict d
            #add here queries
            return render_template('project.html')
        if update is not None:
            print("update")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('project.html')
        if delete is not None:
            print("delete")
            d = request.form
            print(d)
            #get vars for dict d
            #add here queries
            return render_template('project.html')
    return render_template('project.html')


if __name__ == '__main__':
    app.run(debug=True)