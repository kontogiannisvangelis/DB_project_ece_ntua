# Hellenic Foundation For Research & Innovation database
This is a project for the Databases class in NTUA Electrical and Computer Engineering

## Contributors
Listed alphabetically: <br />
1.Kontogiannis Evangelos (03119104)<br />
2.Babanis Georgios (03119094)<br />
3.Boutsini Theodora (03119083)<br />

## Tools
- Mysql server 8.0.29	
- Flask 2.0.1
- MySQL Workbench 8.0.29
- Visual Studio Code
## Requirements
- Mysql server 8.0.29	
- Flask 2.0.1

## ER-Diagram
![](https://github.com/kontogiannisvangelis/DB_project_ece_ntua/blob/main/ER_model/ER_model.png)

## Relational Model
![](https://github.com/kontogiannisvangelis/DB_project_ece_ntua/blob/main/Relational%20schema/Relational%20schema.png)

## Database Setup
1. Create the database with name: 'hfri' password: 'root' and then open a local server on Mysql Workbench and run the Query Schema.
2. Data import
Enable the appearance of hidden files in Windows <br />
(Select the Start button, then select Control Panel > Appearance and Personalization.<br />Select Folder Options, then select the View tab.Under Advanced settings, select Show hidden files, folders, and drives, and then select OK) <br />
Copy the file data to the directory C:\ProgramData\MySQL\MySQL Server 8.0\Uploads.<br />
To manually import data with Mysql workbench select schema under the navigator tab, then right click the table you wish to configure. Select data import wizard and then open the appropriate csv file from the folder data. <br />
Inserting the data into the database:
    1. Insert manually the data for the tables Executives, Organizations, Programs, Scientific fields.
    2. Run query data import 1
    3. Insert manually the data for the table Works on Project
    4. Run query data import 2
    5. Insert manually the data for the table Sf belongs

## Application Setup
1. Open with vscode the file [frontend](https://github.com/kontogiannisvangelis/DB_project_ece_ntua/tree/main/frontend)
2. run in vscode terminal,
 ```bash
     pip install virtualenv
     set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     env/Scripts/activate
     pip install Flask
     pip install flask-mysqldb
     pip install pyyaml
     python app.py
 ```
