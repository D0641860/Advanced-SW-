import unittest
import urllib.request
 
from selenium import webdriver
import pymysql 
import time


db = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="test")
cursor=db.cursor()

test_username = ["admin","test1","test2","test3"]
test_password = ["admin2016","1test2020","2test2020","3test2020"]

# Set test variables for test admin user
test_admin_username = "admin"
test_admin_password = "admin2016"
 
# Set test variables for test 1
test_employee1_username = "test1"
test_employee1_password = "1test2020"
 
# Set test variables for test 2
test_employee2_username = "test2"
test_employee2_password = "2test2020"

# Set test variables for test 3
test_employee2_username = "test3"
test_employee2_password = "3test2020"
 

class test(unittest.TestCase):
    i = 0
    browser = webdriver.Chrome()
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
    browser.close()

if __name__ == "__main__":
    unittest.main()
