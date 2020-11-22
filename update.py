import os
import subprocess
import shutil
subprocess.run(['src/a.out'])
import plot
print('Now updating...')
shutil.copy('plot.png', '/Users/SoChigusa/works/homepage/')
shutil.copy('atm.dat', '/Users/SoChigusa/works/homepage/')
shutil.copy('plot.png', '/Users/SoChigusa/works/sochigusa.bitbucket.org/')
os.chdir('/Users/SoChigusa/works/sochigusa.bitbucket.org/')
subprocess.run(['git','commit','-a','-m','"Auto commit by mental health update"'])
subprocess.run(['git','push','origin','master'])
