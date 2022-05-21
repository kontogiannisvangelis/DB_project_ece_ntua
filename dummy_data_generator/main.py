from random import randint
import names as names
import csv
program_names = []
for i in range(30):
    program_name = 'Program ' + str(i+1)
    program_names.append(program_name)

sections = []
for i in range(5):
    sec = 'Section ' + str(i)
    sections.append(sec)

post_code = []
for i in range(30):
    post_code.append(randint(10000, 55555))

city = ['Athens', 'Larisa', 'Arta', 'Thessalonicki', 'Volos']

first_name = []
last_name = []
for i in range(120):
    first_name.append(names.get_first_name())

for i in range(120):
    last_name.append((names.get_last_name()))

org_name = []
org_abr = []

for i in range(40):
    name = 'Organization ' + str(i+1)
    name_2 = 'Org'+str(i+1)
    org_name.append(name)
    org_abr.append(name_2)

street = ['King 1', 'Hudson 2', 'Sherman 3', 'Hickory 4', 'Redwood 5', 'Magnolia 6', 'Lexington 7', 'Laurel 8',
          'Myrtle 9', 'Front Street 10']

org_type = ['Corporation', 'University', 'Research_center']

sex = ['Male', 'Female', 'Other']

description = []
for i in range(300):
    string = 'Some random description ' + str(i)
    description.append(string)

title = []
for i in range(300):
    string = "Random title " + str(i)
    title.append(string)

sf_field = ['Physics', 'Maths', 'Computer science', 'Art', 'Medicine']

end_dates = []
project_dates = []
for i in range(200):
    a = randint(2017, 2020)
    b = randint(1, 13)
    c = randint(1, 29)
    date = str(a) + '/' + str(b) + '/' + str(c)
    end_date = str(a + randint(1, 5)) + '/' + str(b) + '/' + str(c)
    project_dates.append(date)
    end_dates.append(end_date)

birth_dates = []
for i in range(400):
    a = randint(1970, 1995)
    b = randint(1, 13)
    c = randint(1, 29)
    birth_date = str(a) + '/' + str(b) + '/' + str(c)
    birth_dates.append(birth_date)

eval_dates = []
for i in range(200):
    a = randint(2015, 2017)
    b = randint(1, 13)
    c = randint(1, 29)
    eval_date = str(a) + '/' + str(b) + '/' + str(c)
    eval_dates.append(eval_date)

start_work_dates = []
for i in range(400):
    a = randint(2013, 2015)
    b = randint(1, 13)
    c = randint(1, 29)
    start_work_date = str(a) + '/' + str(b) + '/' + str(c)
    start_work_dates.append(start_work_date)


f = open('Scientific_field.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['id', 'name'])
id = 1
for i in sf_field:
    row = [id, i]
    id += 1
    writer.writerow(row)
f.close()

f = open('Executive.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['id', 'first_name', 'last_name'])
for i in range(10):
    row = [i, first_name[randint(1, 100)], last_name[randint(1, 100)]]
    writer.writerow(row)
f.close()

f = open('Program.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['id', 'name', 'section'])
id = 1
for i in program_names:
    row = [id, i, sections[randint(0, 4)]]
    writer.writerow(row)
    id += 1
f.close()

f = open('Organizations.csv', 'w', newline='')
u = open('University.csv', 'w', newline='')
r = open('Researc_center.csv', 'w', newline='')
c = open('Corporation.csv', 'w', newline='')
writer = csv.writer(f)
writer_u = csv.writer(u)
writer_c = csv.writer(c)
writer_r = csv.writer(r)
writer.writerow(['id', 'name', 'abbreviation', 'post code', 'street', 'city', 'type'])
writer_r.writerow(['id', 'budget', 'budget_2'])
writer_u.writerow(['id', 'budget'])
writer_c.writerow(['id', 'budget'])
id = 1
for i in range(30):
    t = org_type[randint(0, 2)]
    row = [id, org_name[i], org_abr[i], randint(10000, 99999), street[randint(0, 9)], city[randint(0, 4)], t]
    writer.writerow(row)
    if t == 'University':
        writer_u.writerow([id, randint(10000,1000000)])
    if t == 'Corporation':
        writer_c.writerow([id, randint(10000, 1000000)])
    if t == 'Research_center':
        writer_r.writerow([id, randint(10000, 1000000), randint(10000, 1000000)])
    id += 1
f.close()
u.close()
c.close()
r.close()

f = open('Organization_phones.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['phone number', 'id'])
for i in range(30):
    for j in range(randint(1, 4)):
        row = [randint(6900000000, 6999999999), i+1]
        writer.writerow(row)
f.close()

r = open('Researcher.csv', 'w', newline='')
e = open('Evaluation.csv', 'w', newline='')
p = open('Project.csv', 'w', newline='')
d = open('Deliverable.csv', 'w', newline='')
sfb = open('Sf_belongs.csv', 'w', newline='')
wp = open('Works_on_project.csv', 'w', newline='')
writer_r = csv.writer(r)
writer_e = csv.writer(e)
writer_p = csv.writer(p)
writer_d = csv.writer(d)
writer_sfb = csv.writer(sfb)
writer_wp = csv.writer(wp)
writer_r.writerow(['id', 'first_name', 'last_name', 'birthdate', 'Sex', 'org_id'])
writer_e.writerow(['id', ' date ', ' grade', 'rid', 'oid'])
writer_p.writerow(['id', 'amount', 'title', 'start_date' 'end_date', 'desc', 'exid', 'pid', 'rid', 'eid', 'oid'])
writer_d.writerow(['id', 'pid', ' title', 'desc', 'delivery_date'])
writer_sfb.writerow(['pid', 'sf id'])
writer_wp.writerow(['pid', 'rid'])
rid = 1
peid = 1
did = 1
for j in range(30):
    temp = (randint(0, 5))
    if j != 0:
        for i in range(temp):
            prow = [peid, randint(1000, 100000), title[peid], project_dates[peid], end_dates[peid], description[peid+1],
                    randint(1, 10), randint(1, 30), rid+i, peid, j+1]
            writer_p.writerow(prow)
            erow = [peid, eval_dates[peid], randint(30, 100), randint(1, 10), j+1]
            writer_e.writerow(erow)
            for k in range(randint(1, 3)):
                writer_sfb.writerow([peid, randint(1, 10)])
            peid += 1
            for k in range(randint(0, 5)):
                drow = [did, peid-1, title[did], description[did], end_dates[peid-1]]
                writer_d.writerow(drow)
                did += 1
        for i in range(temp+randint(0, 10)):
            rrow = [rid, first_name[randint(1, 100)], last_name[randint(1, 100)], sex[randint(0, 2)],
                    start_work_dates[rid], j+1]
            if temp == 1:
                works_on_row = [peid-1, rid]
                writer_r.writerow(rrow)
                writer_wp.writerow(works_on_row)
            if temp > 1:
                works_on_row = [peid - randint(1, temp), rid]
                writer_r.writerow(rrow)
                writer_wp.writerow(works_on_row)
            rid += 1
    if j == 0:
        for i in range(10):
            rrow = [rid, first_name[randint(1, 100)], last_name[randint(1, 100)], sex[randint(0, 2)],
                    start_work_dates[rid], j + 1]
            writer_r.writerow(rrow)
            rid += 1



