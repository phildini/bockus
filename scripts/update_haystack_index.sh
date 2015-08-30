#! /bin/bash
source /home/deploy/.bashrc
cd /home/deploy/Env/booksonas
source bin/activate
cd /home/deploy/bockus
python manage.py update_index --remove --age=1 --settings=bockus.prod_settings
deactivate