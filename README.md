First make sure you have python installed.
- py --version (this is for windows)
- python --version (this is for mac)

Then you initiate the environment
- py -m venv myenv 

Install django
- pip install django psycopg2 

Download psql from web then check the version
- psql --version 

Get inside the postrge and run these
- psql -U postgres
- CREATE DATABASE library_db;
- \l
- psql -U postgres library_db
- CREATE USER group20 WITH PASSWORD 'password';
- GRANT ALL PRIVILEGES ON DATABASE library_db TO group20;
- GRANT USAGE ON SCHEMA public TO group20;
- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO group20;
- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO group20;

Start the environment
- myenv\Scripts\activate

Get inside the library management directory
- cd library_management

  Make migrations and migrate
- python manage.py makemigrations 
- python manage.py migrate  

Run the application server
- python manage.py runserver 

