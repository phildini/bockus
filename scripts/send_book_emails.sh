#! /bin/bash
source /home/deploy/.bashrc
cd /home/deploy/Env/booksonas
source bin/activate
cd /home/deploy/bockus
python manage.py email_books --settings=bockus.prod_settings
deactivate