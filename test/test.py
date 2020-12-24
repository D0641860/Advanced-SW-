import unittest
import urllib.request
 
from selenium import webdriver
import pymysql 
import time

from pymysql import connect
#import chromedriver_binary

db= pymysql.connect(host="127.0.0.1",port=3307,user="advancedsw",password="advancedsw",db="advancedsw") #鉦淩的

#db = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="test")
#db= pymysql.connect(host="127.0.0.1",port=3306,user="root",password="advancesw",db="advancedsw")
#db= pymysql.connect(host="140.134.26.99",port=34586,user="root",password="advancesw",db="advancedsw") #邱一號

cursor=db.cursor()

test_username = ["admin","test1","test2","test3"]
test_password = ["admin2016","1test2020","2test2020","3test2020"] 

class test(unittest.TestCase):

    db.ping(reconnect=True)

    def setUp(self): #每一次執行測試方法"前"會執行
        self.browser = webdriver.Chrome()
        #self.f = open('test_record.txt', 'w')

    def test_register_login(self):
        i = 0
        browser = self.browser
        #f = self.f
        while i<4:
            #browser.get("https://haiya.kainull.com/register")
            browser.get("http://localhost:5000/register")    
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
            
            #select DB
            ID = test_username[i]
            pwd = test_password[i]
            ID=ID.upper()
            print(ID,pwd)
            select="SELECT * FROM `user` WHERE account='%s' and password='%s'"%(ID,pwd)
            print(select)
            cursor.execute(select)
            db.commit()
            data=cursor.fetchone()
            self.assertIsNotNone(data,msg="Failed!")
            print("{} Successful!".format(test_username[i]))
            #f.write("{} Successful!\n".format(test_username[i]))
            i += 1
      
    def test_index(self):
        browser = self.browser
        browser.get("http://localhost:5000")
        browser.find_element_by_id('check_home').click()
        time.sleep(3)

        home = browser.current_url
        self.assertEqual(home,"http://localhost:5000/index")

    def test_refig(self):
        browser = self.browser
        browser.get("http://localhost:5000")
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
        browser = self.browser
        browser.get("http://localhost:5000")
        browser.find_element_by_id('check_menu').click()
        time.sleep(3)
        menu = browser.current_url
        self.assertEqual(menu,"http://localhost:5000/menu")
    
    def tearDown(self): #每一次執行測試方法後會執行
        self.browser.close()
        #self.f.close()

if __name__ == "__main__":
    unittest.main()
