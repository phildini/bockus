#!/bin/bash
cd /home/deploy/Env/booksonas/
source bin/activate
cd /home/deploy/bockus/
git pull --rebase
pip install -r requirements.txt
kill -HUP `cat /tmp/booksonas-master.pid`
