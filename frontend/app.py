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
def page_3():                                                                #uncommend lines below
    cur = mysql.connection.cursor()
    sf_field_res = cur.execute("select sf_name from Scientific_field")
    sf = cur.fetchall()
    if request.method == 'POST':
        #field = request.form
        #cur = mysql.connection.cursor()
        #sf_field_res = cur.execute("")                                      #add query
        #tup = cur.fetchall()  
        return render_template('page_3.html', sf=sf, related=sf)             #change to sf to tup
    return render_template('page_3.html', sf=sf, related=[])

@app.route('/page_4.html')
def page_4():                                                                #uncommend lines below
    #cur = mysql.connection.cursor()
    #res = cur.execute("")                                                   #add query
    #tuples = cur.fetchall() 
    return render_template('page_4.html', tuples=[])                         #change [] to tuples

@app.route('/page_5.html')
def page_5():                                                                #uncommend lines below
    #cur = mysql.connection.cursor()
    #res = cur.execute("")                                                   #add query
    #tuples = cur.fetchall() 
    return render_template('page_5.html', tuples=[])                         #change [] to tuples


@app.route('/page_6.html')
def page_6():                                                                #uncommend lines below
    #cur = mysql.connection.cursor()
    #res = cur.execute("")                                                   #add query
    #tuples = cur.fetchall() 
    return render_template('page_6.html', tuples=[])                         #change [] to tuples

@app.route('/page_7.html')  
def page_7():                                                                #uncommend lines below
    #cur = mysql.connection.cursor()
    #res = cur.execute("")                                                   #add query
    #tuples = cur.fetchall() 
    return render_template('page_7.html', tuples=[])                         #change [] to tuples

@app.route('/page_8.html')
def page_8():                                                                #uncommend lines below
    #cur = mysql.connection.cursor()
    #res = cur.execute("")                                                   #add query
    #tuples = cur.fetchall() 
    return render_template('page_8.html', tuples=[])                         #change [] to tuples

@app.route('/page_9.html')
def page_9():
    return render_template('page_9.html')

@app.route('/page_9_ins.html')
def page_9_ins():
    return render_template('page_9_ins.html')

@app.route('/page_9_up.html')
def page_9_up():
    return render_template('page_9_up.html')

@app.route('/page_9_del.html')
def page_9_del():
    return render_template('page_9_del.html')

@app.route('/page_9_ins_1.html')
def page_9_ins_1():
    return render_template('page_9_ins_1.html')


if __name__ == '__main__':
    app.run(debug=True)