#!/bin/bash
cd /home/Env/booksonas/
source bin/activate
cd /home/deploy/bockus/
git pull --rebase
pip install -r requirements.txt
kill -HUP `cat /tmp/booksonas-master.pid`
