#!/bin/bash

logfile="/home/mloss/tmp/update_feeds.log"
cp /dev/null $logfile
echo "This is a message from update_feeds.sh `date`" >> $logfile
cd ~/django/mloss
export PYTHONPATH=/home/mloss/django:
python update_feeds.py --settings='mloss.settings' >> $logfile 2>&1
