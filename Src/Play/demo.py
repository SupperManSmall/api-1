#!/usr/bin/env python
# coding=utf-8

from pyvirtualdisplay import Display
from selenium import webdriver
import platform
import sys, os
print sys.argv

def ABSpath():
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH)
    return ABSPATH

os.environ["PATH"] += (os.pathsep + ABSpath() + '/../../bin')

display = Display(visible=0, size=(800, 600))
display.start() # now Firefox will run in a virtual display. you will not see the driver.

# 因为在CentOS上安装Chrome折腾了一宿没有成功，看网上也是说“没有简单的办法”，而firefox就简单很多。所以，在CentOS上就用firefox吧
# 本地开发时用Chrome，比firefox响应速度快好多（2-4倍据说）

if ('firefox' in sys.argv):
	print 'use firefox'
	driver = webdriver.Firefox()
elif (('phantom' in sys.argv) or ('phantomjs' in sys.argv)):
	print 'use phantomjs'
	driver = webdriver.PhantomJS('phantomjs')
else:
	print 'use chrome'	
	driver = webdriver.Chrome()

driver.get('http://www.xxtao.com')
#print driver.title
assert u'万屏汇' in driver.title


# >> click "提交"
submit = driver.find_element_by_id('bd_10ssignup_submit')
submit.click()

# << check track
js = 'document.getElementById("Track").className = ""' 
driver.execute_script(js)
iframe = driver.find_elements_by_id('TrackFrame')[0]

# 1. <iframe src='${url}'>
url = '/track/10ssignup_submit.html' 
src = iframe.get_attribute('src')
#print src
assert url in src

# 2. <p id='c'>${url}</p>
driver.switch_to_frame(iframe)
text = driver.find_element_by_id('c').text
#print text
assert url in text 

print '.'
driver.quit()
display.stop()
