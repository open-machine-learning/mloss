#!/bin/bash

logfile="/tmp/update_feeds.log"
cp /dev/null $logfile
echo "This is a message from update_feeds.sh `date`" >> $logfile
cd ~/mloss
export PYTHONPATH=/home/mloss/:/home/mloss/lib/python2.5/site-packages/:
python update_feeds.py --settings='mloss.settings' >> $logfile 2>&1
