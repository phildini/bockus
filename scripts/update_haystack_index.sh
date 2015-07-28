#! /bin/bash
source /home/deploy/.bashrc
source `which virtualenvwrapper.sh`
workon booksonas
cd bockus
python manage.py update_index --age=1 --settings=bockus.prod_settings
deactivate
