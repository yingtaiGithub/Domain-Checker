import os

from crontab import CronTab

from config import *


current_directory = os.getcwd()

user_cron   = CronTab(user=UserForCronJob)
job  = user_cron.new(command='python %s' %os.path.join(current_directory, 'cron_task.py'), comment='domain checker')
job.day.every(interval_days)

user_cron.write()

# cron = CronTab(tabfile='cron.tab')
# job  = cron.new(command='python %s' %os.path.join(current_directory, 'cron_task.py'), comment='domain checker')
# job.minute.every(interval_minutes)
# cron.write()
