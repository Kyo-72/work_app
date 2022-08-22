#! python3

from email_programs import convert

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
import re
from bs4 import BeautifulSoup

# chromedriverの設定
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')





def getSchedule(days_later,myclass_id,myclass_password):



    lessons = {}    #担当講師名と実施授業をint型で管理

    #正規表現
    lesson_time_regex = re.compile(r'\d\d:\d\d')


    # ブラウザを開く。webドライバのpathを指定
    #browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)


    #urlのサイトに飛ぶ
    url = 'https://koushi.edu-beit.net/seiki/edubeit/schedule/index' 
    browser.get(url)
    

    #ログイン処理
    elem_username = browser.find_element_by_id('loginId')
    elem_username.send_keys(myclass_id)

    elem_password = browser.find_element_by_id('password')
    elem_password.send_keys(myclass_password)

    elem_loginbtn = browser.find_element_by_tag_name('button')
    elem_loginbtn.click()

    #全体のスケジュールページに飛ぶ
    browser.find_element_by_xpath('/html/body/main/div/p/a').click()

    #ページのhtmlを取得、BeautifulSoupオブジェクトへ
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    #html解析と文字列処理
                        

    schedule_table = soup.find('table',attrs={'class':'table table-bordered table-schedule02'})
    schedule_table = schedule_table.find('tbody')
    all_lessons_schedule = schedule_table.find_all('tr')
    #print(all_lessons_schedule)

    #一人につき授業を調べる

    for i in range(len(all_lessons_schedule)):
        #一人取り出す
        today_lessons_schedule = all_lessons_schedule[i].find('td',attrs = {'class':'today'})
        try:
            
            #リストの先頭にclass = todayのオブジェクトを入れる
            lessons_schedule = [today_lessons_schedule]
            #class = todayの兄弟要素をリストに入れる
            lessons_schedule +=   list( today_lessons_schedule.next_sibling.next_siblings ) 
            
            #matchオブジェクトを生成
            
            #空白を処理する
            lessons_schedule = [l for l in lessons_schedule if l != "\n"]
            
            

    
            lesson_mo = lesson_time_regex.findall(lessons_schedule[days_later].text)
            if( len(lesson_mo) ):
              lessons[ all_lessons_schedule[i].find('th').text ] = convert.Convert_To_Bit(lesson_mo)
            
        #日付欄は読み飛ばす
        except AttributeError:
            continue
                      
                        
  
    #ブラウザを閉じる
    browser.quit()

    return lessons


