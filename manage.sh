# #!/bin/bash
# #write out current crontab
# crontab -l > mycron
# #echo new cron into cron file
# echo "* * * * * python /app/getStatistics.py -D" >> mycron
# #install new cron file
# crontab mycron
# status=$?
# if [ $status -ne 0 ]; then
#   echo "Failed to start my_first_process: $status"
#   exit $status
# fi
# echo ' started the cron'


# python app.py
# status=$?
# if [ $status -ne 0 ]; then
#   echo "Failed to start my_second_process: $status"
#   exit $status
# fi

# while sleep 60; do
#   ps aux |grep my_first_process |grep -q -v grep
#   PROCESS_1_STATUS=$?
#   ps aux |grep my_second_process |grep -q -v grep
#   PROCESS_2_STATUS=$?
#   cat /ss.txt
  
#   if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
#     echo "One of the processes has already exited."
#     exit 1
#   fi
# done

service cron start
echo "0 * * * * /usr/local/bin/python /app/getStatistics.py" > cronjob
crontab cronjob 
python app.py
echo bye
exec "$@"
