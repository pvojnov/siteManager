# create app
python manage.py startapp servers


# run server
python manage.py runserver

python manage.py migrate



python manage.py sqlall servers
python manage.py syncdb



python manage.py dumpdata servers > temp_data.json
python manage.py sqlclear servers | python manage.py dbshell
python manage.py syncdb
python manage.py loaddata temp_data.json