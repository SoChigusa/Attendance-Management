#!/usr/local/bin/python3
# coding: utf-8
import yaml
import numpy as np
import datetime
from datetime import timedelta

def openGoogleForm(cf):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait

    chrome = webdriver.Chrome(cf['webdriver'])

    # 日付を取得しフォームにプリセット
    today = datetime.date.today()

    # Googleフォームを開く
    chrome.get(cf['URL']+'&entry.'+cf['entry-date']+'='+str(today))

    # タブが閉じられるのを待つ
    WebDriverWait(chrome, 60*60*24).until(lambda d: len(d.window_handles) == 0)

    # 終了処理
    chrome.quit()

def Mood2Num(input):
    if input == 'Cheerful':
        out = 2
    elif input == 'Soso':
        out = 1
    else:
        out = 0
    return out

def Workload2Num(input):
    if input == 'None':
        out = 0
    elif input == '0 -- 1 hour':
        out = 1
    elif input == '1 -- 2 hours':
        out = 2
    elif input == '2 -- 3 hours':
        out = 3
    elif input == '3 -- 4 hours':
        out = 4
    elif input == '4 -- 5 hours':
        out = 5
    elif input == '5 -- 6 hours':
        out = 6
    elif input == '6 -- 7 hours':
        out = 7
    elif input == '7 -- 8 hours':
        out = 8
    elif input == '8 -- 9 hours':
        out = 9
    elif input == '9 -- 10 hours':
        out = 10
    elif input == '10 -- 11 hours':
        out = 11
    elif input == '11 -- 12 hours':
        out = 12
    else:
        out = 13
    return out

def readFromSpread(cf):
    import gspread
    import json

    #ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
    from oauth2client.service_account import ServiceAccountCredentials

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cf['json'], scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = cf['spreadsheet-key']

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    #セルの値を受け取る
    c2 = worksheet.col_values(2)
    c3 = worksheet.col_values(3)
    c4 = worksheet.col_values(4)
    for c in [c2, c3, c4]:
        c.pop(0)
    date = list(map(lambda l: datetime.datetime.strptime(l, '%Y/%m/%d').date(), c2))
    serial = list(map(lambda l: (l - datetime.date(1970,1,1)).days, date))
    color = np.vectorize(Mood2Num)(c3)
    y = np.vectorize(Workload2Num)(c4)

    # 戻り値
    date = np.array(date)
    data = np.array([serial, y, color]).transpose()
    return date, data

def plot(cf, date, data):
    import matplotlib.pyplot as plt

    # figure settings and data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Workloads and Moods : So Chigusa', size=20)

    # line plot
    ax.plot(data[:,0], data[:,1], zorder=1)

    # scatter plot
    color = ['red', 'orange', 'blue']
    def plotFeeling(array):
        ax.scatter(array[0], array[1], color=color[int(array[2])], zorder=2)
    np.apply_along_axis(plotFeeling, 1, data)

    # x-axis
    center1 = (int)(np.floor(date.size/3))
    center2 = (int)(np.floor(2*date.size/3))
    ax.set_xlabel('Date', size=15)
    ax.set(xticks=[data[0,0],data[center1,0],data[center2,0],data[-1,0]],\
           xticklabels=[date[0],date[center1],date[center2],date[-1]])

    # y-axis
    ax.set_ylim(-0.1, 13.1)
    ax.set_ylabel('How long did you work?', size=15)
    ax.set(yticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13], yticklabels=['None', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '12h+'])

    # legend
    ax.scatter(data[0,0], 100, color=color[2], label='cheerful')
    ax.scatter(data[0,0], 100, color=color[1], label='soso')
    ax.scatter(data[0,0], 100, color=color[0], label='depressed')
    ax.legend(fontsize=15, loc='best')

    plt.tight_layout()
    plt.savefig(cf['plot'], bbox_inches='tight')

def update():
    import os
    import subprocess
    import shutil
    os.chdir('/Users/SoChigusa/works/Attendance-Management/')
    subprocess.run(['git','pull'])
    subprocess.run(['git','commit','-a','-m','"Auto commit by autoupdate.py"'])
    subprocess.run(['git','push'])
    shutil.copy('plot.png', '/Users/SoChigusa/works/sochigusa.bitbucket.org/')
    os.chdir('/Users/SoChigusa/works/sochigusa.bitbucket.org/')
    subprocess.run(['git','pull'])
    subprocess.run(['git','commit','-a','-m','"Auto commit by mental health update"'])
    subprocess.run(['git','push'])

# 設定ファイルの読み込み
with open('/Users/SoChigusa/works/Attendance-Management/config.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)

openGoogleForm(config)
date, data = readFromSpread(config)
plot(config, date, data)
update()
