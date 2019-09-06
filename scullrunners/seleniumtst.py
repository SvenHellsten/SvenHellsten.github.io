import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import argparse
import os
from datetime import date
from datetime import timedelta


def date_to_nth_day():
		return (date.today()-date(2019,1,1))


class Webdriver():

	def progressBar(self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		return('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))

	

	def get_km(self,driv,idnr):
		driv.get('https://www.strava.com/athletes/'+ idnr)
		time.sleep(0.5)
		results = driv.find_elements_by_xpath("//*[@id='running-ytd']/tr[1]/td[2]")
		# results = driver.find_elements_by_xpath('//[@id="running-ytd"]/tr[1]/td[2]')
		# print(results[0].get_attribute('innerHTML'))
		print(results)
		if results is None:               #Sometimes it does not register so do it again and wait a little longer.
			print("oops a little hickup.")
			driv.get('https://www.strava.com/athletes/'+ idnr)
			time.sleep(1.5)
			results = driv.find_elements_by_xpath("//*[@id='running-ytd']/tr[1]/td[2]")

		strdistans = results[0].get_attribute('outerHTML')
		dist = int((''.join(filter(lambda x: x.isdigit(), strdistans))))

		# print (dist)
		return dist
	def get_memb(self,driv):
		driv.get('https://www.strava.com/clubs/495789/members')
		html = driv.page_source
		soup = BeautifulSoup(html)
		text = soup.get_text()
		if 'members:' in text:
			junk, tail = text.split('members:')
			last_char = tail.find(']]')
			first_char = tail.find('[[')
			member_list = tail[first_char:last_char+2]
			mem_array_raw = eval(member_list)
			mem_array = []
			for member in mem_array_raw:
				mem_array.append([member[0], member[1]])
			lst = [str(item[0]) for item in mem_array]
			fst = [str(item[1]) for item in mem_array]
			print (fst)
			return (lst,fst)

		return 

	def login(self):
		
		urlpage = 'https://www.strava.com/login' 
		print(urlpage)
		# run firefox webdriver from executable path of your choice
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.set_preference('permissions.default.image', 2)
		firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

		driver = webdriver.Firefox()
		# get web page
		driver.get(urlpage)
		driver.find_element_by_id("email").send_keys("sven.hellsten@gmail.com")
		driver.find_element_by_id ("password").send_keys("xxxxxxxxx")
		driver.find_element_by_id("login-button").click()
		time.sleep(1)
		members = self.get_memb(driver)
		print (members[0])
		members[0].remove('8446399')
		res = ([self.get_km(driver, x) for x in members[0]])
		km_debt = ((date_to_nth_day().days)*51-sum(res)/10)
		if km_debt > 0:
			kmOutput = ("Vi ligger " + "{0:.2f}".format(km_debt)+'km efter, ajaj.. ')
		else:
			kmOutput = ("Vi ligger " + "{0:.2f}".format(abs(km_debt))+'km före, Hurra!! ')
		daysleft = 186400/(sum(res)/date_to_nth_day().days)
		print (daysleft)
		target = "I denna takt så kommer Poweradebålen att flöda:  " + str(timedelta(days=daysleft)+date(2019,1,1))
		# print (sum(res)/10)
		# time.sleep(7)
		# find elements by xpath
		#results = driver.find_elements_by_xpath("//*[@id='componentsContainer']//*[contains(@id,'listingsContainer')]//*[@class='product active']//*[@class='title productTitle']")
		#print('Number of results', len(results))
		b=open("before.txt", 'r')
		a=open("after.txt",'r')
		pbar= self.progressBar(sum(res)/100, 1864, prefix = 'Progress:', suffix = 'Klart', length = 30)
		cont = b.read() + '<p>'+str(sum(res)/10) +'km </p>' + "\n<h1>" + pbar +'</h1>' + "\n<h1>" + kmOutput +'</h1>' + target +'</h1>' + a.read()
		b.close()
		a.close()
		f=open('index.html','w')
		f.write(cont)
		f.close()
		c=open("stats.txt",'a+')
		c.write(str(date.today()) + ' '+str(sum(res)/10))
		c.close()
		os.system("git add index.html")
		os.system("git commit -m 'auto update'")
		os.system("git push origin master")

		driver.quit() 



def main():
	scraper = Webdriver()
	scraper.login()

if __name__ == '__main__':
    main()