# Console input of workload/mood data
import datetime
date = datetime.date.today() - datetime.timedelta(hours=3)
print('Input date (default: '+date.strftime('%Y/%m/%d')+')')
strin = input('>> ')
if(strin != ''):
    date = datetime.datetime.strptime(strin, '%Y/%m/%d').date()
dd = date - datetime.date(1970,1,1)
x = dd.days
print('How hard did you work? (rate by [0-3])')
strin = input('>> ')
y = int(strin)
print('How was your mood? (rate by [0-2])')
strin = input('>> ')
z = int(strin)
with open('atm.dat', mode='a') as f:
    f.write(str(x)+'\t'+str(y)+'\t'+str(z)+'\n')

# Plot and update
import os
import subprocess
import shutil
import plot
print('Now updating...')
subprocess.run(['git','commit','-a','-m','"Auto commit by update.py"'])
subprocess.run(['git','push','origin','main'])
shutil.copy('plot.png', '/Users/SoChigusa/works/sochigusa.bitbucket.org/')
os.chdir('/Users/SoChigusa/works/sochigusa.bitbucket.org/')
subprocess.run(['git','commit','-a','-m','"Auto commit by mental health update"'])
subprocess.run(['git','push','origin','master'])
