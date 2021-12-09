from selenium import webdriver
from datetime import datetime
from email.mime.text import MIMEText
import time
import smtplib


class color:
   BOLD = '\033[1m'
   END = '\033[0m'

now = datetime.now()
current_time = now.strftime("%Y.%m.%d")

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome('/Users/galbae/chromedriver', options=options)

D_url = "https://www.melon.com/new/album/index.htm"
O_url = "https://www.melon.com/new/album/index.htm#params%5BareaFlg%5D=O&params%5BorderBy%5D=&po=pageObj&startIndex=1"

print('\n\nDATE:' + current_time)
print("------------------------------------------------------------------------------------")
albumlist = []
artistlist = []
def check(URL):
    driver.get(URL)
    time.sleep(2)
    for i in range(2):
        a = driver.find_elements_by_class_name("reg_date")
        
        for i in range(len(a)):
            album = driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[3]/form/div/ul/li["+str(i+1)+"]/div[2]/div[1]/a")
            artist = driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[3]/form/div/ul/li["+str(i+1)+"]/div[2]/div[1]/span[2]")
            if a[i].text == current_time:
                print(album.text, end="  ")
                albumlist.append(album.text)
                print(color.BOLD+ artist.text + color.END)
                artistlist.append(artist.text)
        driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[4]/div/span/a[1]").click()
        time.sleep(2)

print(color.BOLD+ "국내신곡\n" + color.END)
check(D_url)
albumlist.append("\n")
artistlist.append("해외신곡")
print("------------------------------------------------------------------------------------")
print(color.BOLD+ "해외신곡\n" + color.END)
check(O_url)
print("------------------------------------------------------------------------------------\n")
print("바로가기:"+D_url)
print("------------------------------------------------------------------------------------\n")
driver.quit()

now = datetime.now()
current =  ("%s-%s-%s" %(now.year, now.month, now.day))
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('@gmail.com','password')

contents = "-국내신곡"+'\n' +albumlist[0] +" - "+ artistlist[0]
for i in range(1, len(albumlist)):
    contents += '\n' + albumlist[i] + ' - ' + artistlist[i]
contents += '\n'+ '\n' + "국내신곡 바로가기:" + D_url
contents += '\n' + "해외신곡 바로가기:" + O_url

msg = MIMEText(contents)

msg['Subject'] = str(current)+' 신곡'
s.sendmail("@gmail.com", "@gmail.com", msg.as_string())
s.quit()