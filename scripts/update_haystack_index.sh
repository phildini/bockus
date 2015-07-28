source .bashrc
workon booksonas
cd bockus
python manage.py update_index --age=1 --settings=bockus.prod_settings
deactivate