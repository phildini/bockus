#! /bin/bash
source /home/deploy/.bashrc
cd /home/deploy/Env/booksonas
source bin/activate
cd /home/deploy/bockus
python manage.py send_invites --settings=bockus.prod_settings
deactivate