import numpy as np
import datetime
from datetime import timedelta

def openGoogleForm():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait

    chrome = webdriver.Chrome("./driver/chromedriver")

    # Googleフォームを開く
    chrome.get('https://docs.google.com/forms/d/e/1FAIpQLSdJelnqnhninHvi4U2tw1BpDdjYi7yAQnRH_UPqhNt7inX8JQ/viewform?usp=sf_link')

    # タブが閉じられるのを待つ
    WebDriverWait(chrome, 60*60*24).until(lambda d: len(d.window_handles) == 0)

    # 終了処理
    chrome.quit()

def readFromSpread():
    import gspread
    import json

    #ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
    from oauth2client.service_account import ServiceAccountCredentials

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('secrets/workloads-and-moods-091ba6839e7b.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '1Z0ks-Bo9pe_lJGla17NQgUz3y8Om_PpK9Dictinu_jA'

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    #セルの値を受け取る
    c2 = worksheet.col_values(2)
    c5 = worksheet.col_values(5)
    c6 = worksheet.col_values(6)
    for c in [c2, c5, c6]:
        c.pop(0)
    date = list(map(lambda l: datetime.datetime.strptime(l, '%Y/%m/%d').date(), c2))
    serial = list(map(lambda l: (l - datetime.date(1970,1,1)).days, date))
    color = list(map(int, c5))
    y = list(map(int, c6))

    # 戻り値
    date = np.array(date)
    data = np.array([serial, y, color]).transpose()
    return date, data

def plot(date, data):
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
    ax.set_ylim(-0.1, 3.1)
    ax.set_ylabel('How hard did you work?', size=15)
    ax.set(yticks=[0,1,2,3], yticklabels=['hardly', 'a little', 'well', 'hard'])

    # legend
    ax.scatter(data[0,0], 100, color=color[2], label='cheerful')
    ax.scatter(data[0,0], 100, color=color[1], label='soso')
    ax.scatter(data[0,0], 100, color=color[0], label='depressed')
    ax.legend(fontsize=15, loc='best')

    plt.tight_layout()
    plt.savefig('plot.png', bbox_inches='tight')

def update():
    import os
    import subprocess
    import shutil
    subprocess.run(['git','pull'])
    subprocess.run(['git','commit','-a','-m','"Auto commit by update.py"'])
    subprocess.run(['git','push'])
    shutil.copy('plot.png', '/Users/SoChigusa/works/sochigusa.bitbucket.org/')
    os.chdir('/Users/SoChigusa/works/sochigusa.bitbucket.org/')
    subprocess.run(['git','pull'])
    subprocess.run(['git','commit','-a','-m','"Auto commit by mental health update"'])
    subprocess.run(['git','push'])

openGoogleForm()
date, data = readFromSpread()
plot(date, data)
update()
