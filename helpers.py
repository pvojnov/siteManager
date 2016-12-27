# create the project
django-admin startproject siteManager

# create app
python manage.py startapp servers


# run server
python manage.py runserver

# migrate
python manage.py makemigrations servers

# print sql comands for migration
python manage.py sqlmigrate servers 0001
	# django 1.6
	python manage.py sqlall servers
# migrate changes to DB
python manage.py migrate
	# django 1.6
	python manage.py syncdb

# check migrations	
python manage.py showmigrations


# create superuser
python manage.py createsuperuser



python manage.py collectstatic



python manage.py dumpdata servers > temp_data.json
python manage.py sqlclear servers | python manage.py dbshell
python manage.py syncdb
python manage.py loaddata temp_data.json