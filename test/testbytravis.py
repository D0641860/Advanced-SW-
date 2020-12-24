import unittest
import urllib.request
 
from selenium import webdriver
import pymysql 
import time

from pymysql import connect

#import chromedriver_binary


#db = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="test")
#db= pymysql.connect(host="127.0.0.1",port=3306,user="root",password="advancesw",db="advancedsw")
db= pymysql.connect(host="140.134.26.99",port=34586,user="root",password="advancesw",db="advancedsw")
cursor=db.cursor()

test_username = ["admin","test1","test2","test3"]
test_password = ["admin2016","1test2020","2test2020","3test2020"] 

options = webdriver.ChromeOptions()
#options.binary_location = '/usr/bin/chromium-browser'
#All the arguments added for chromium to work on selenium
options.add_argument("--no-sandbox") #This make Chromium reachable
options.add_argument("--no-default-browser-check") #Overrides default choices
options.add_argument("--no-first-run")
options.add_argument("--disable-default-apps") 
driver = webdriver.Chrome('/home/travis/virtualenv/python3.7.9/bin/chromedriver',chrome_options=options)
#driver = webdriver.Chrome("/path/to/chrome",chrome_options=options)
class test(unittest.TestCase):
    
    db.ping(reconnect=True)
    #def setUp(self): #每一次執行測試方法"前"會執行
    #    self.browser = webdriver.Chrome('./chromedriver')
    #   self.f = open('test_record.txt', 'w')
    
    def test_register_login(self):
        i = 0
        #browser=driver
        #f = self.f
        browser=driver
        while i<4:
            browser.get("https://haiya.kainull.com/register")    
            time.sleep(2)

            account = browser.find_element_by_name('account')
            password = browser.find_element_by_name('password')
            time.sleep(2)

            account.send_keys(test_username[i])
            password.send_keys(test_password[i])
            time.sleep(2)

            browser.find_element_by_name('submit').click()
            time.sleep(1)

            alert = browser.switch_to_alert()
            alert.accept()
            
            time.sleep(1)
            #select DB
            ID = test_username[i]
            pwd = test_password[i]
            ID=ID.upper()
            select="SELECT * FROM `user` WHERE account='%s' and password='%s'"%(ID,pwd)
                   
            cursor.execute(select)
            db.commit()
            data=cursor.fetchone()
            print(data)
            self.assertIsNotNone(data,msg="Failed!")
            print("{} Successful!".format(test_username[i]))
            #f.write("{} Successful!\n".format(test_username[i]))
            i += 1

    def test_index(self):
        browser=driver
        browser.get("https://haiya.kainull.com")
        browser.find_element_by_id('check_home').click()
        time.sleep(3)

        home = browser.current_url
        self.assertEqual(home,"https://haiya.kainull.com/index")

    def test_refig(self):
        browser=driver
        browser.get("https://haiya.kainull.com")
        Is_user_login = browser.find_element_by_id('check_user').text
        if (Is_user_login!=None):
            browser.find_element_by_id('check_refig').click()
            time.sleep(3)
            temp = browser.find_element_by_tag_name('body').text
            self.assertEqual(temp,"請先登入")
        else:
            browser.find_element_by_id('check_refig').click()
            time.sleep(3)
            temp = browser.find_element_by_tag_name('body').text
            self.assertNotEqual(temp,"請先登入")

    def test_menu(self):
        browser=driver
        browser.get("https://haiya.kainull.com")
        browser.find_element_by_id('check_menu').click()
        time.sleep(3)
        menu = browser.current_url
        self.assertEqual(menu,"https://haiya.kainull.com/menu")
    
    def tearDown(self): #每一次執行測試方法後會執行
        browser.close()
        #self.f.close()

if __name__ == "__main__":
    unittest.main()
