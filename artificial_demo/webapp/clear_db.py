import os
import subprocess

os.system('python manage.py migrate webapp zero')
os.system('python manage.py migrate')

#os.system("cd ..")
#os.system("rm db.sqlite3")
#os.system("python manage.py migrate")