import unittest
import urllib.request
 
from selenium import webdriver
import pymysql 
import time


#db = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="test")
db= pymysql.connect(host="127.0.0.1",port=3307,user="advancedsw",password="advancedsw",db="advancedsw")
cursor=db.cursor()

test_username = ["admin","test1","test2","test3"]
test_password = ["admin2016","1test2020","2test2020","3test2020"] 

class test(unittest.TestCase):
    
    def setUp(self): #每一次執行測試方法"前"會執行
        self.browser = webdriver.Chrome()
    
    def test_register_login(self):
        i = 0
        browser = self.browser
        while i<4:
            browser.get("http://localhost:5000/register")    
            time.sleep(1)

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
            select="SELECT * FROM `user` WHERE account='%s' and password='%s'"%(ID,pwd)
            #time.sleep(2)        
            cursor.execute(select)
            data=cursor.fetchone()
            if(data!=None):
                print("{} Successful!".format(test_username[i]))
            else:
                print("Fucking failed!")
            i += 1

        def tearDown(self): #每一次執行測試方法後會執行
            self.browser.close()

if __name__ == "__main__":
    unittest.main()
