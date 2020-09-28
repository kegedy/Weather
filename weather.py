#https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/
#https://stackoverflow.com/questions/22180930/non-polling-non-blocking-timer

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
import sched
import time
import threading
import os
s = sched.scheduler(time.time, time.sleep)

options = Options()
#options.add_argument('start-fullscreen')
#options.add_experimental_option('detach',True)
#options.add_argument('--incognito')
options.add_argument('disable-infobars')
options.add_extension('ghostery.crx')
seattle = '47.60,-122.33'
WAIT_TIME_SECONDS = 60*10

# HOURLY
def HourlyInit(driver):
    driver.set_window_position(0,-30)
    driver.set_window_size(925,990)
    driver.get('https://google.com')
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    popup = None
    # GHOSTERY POPUP
    try: 
        popup = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="ALERT_ID_6AEC0607-8CC8-4904-BDEB-00F947E5E3C2"]/div/div[1]/div[2]')))
    except:
        print('XPATH NOT FOUND: //*[@id="ALERT_ID_6AEC0607-8CC8-4904-BDEB-00F947E5E3C2"]/div/div[1]/div[2]')
    if popup: popup.click(); popup=None
    # THE WEATHER CHANNEL
    driver.get('https://weather.com/weather/hourbyhour/l/'+seattle)
    # PRIVACY 
    try:
        popup = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.NAME,'close')))
    except:
        print('NAME NOT FOUND: close')
    if popup: popup.click(); popup=None
    driver.set_window_position(0,-30)
    return driver

def HourlyRefresh(driver, sc):
    driver.refresh()
    sc.enter(WAIT_TIME_SECONDS, 1, HourlyRefresh, (driver,sc))

# RADAR
def RadarInit(driver):
    driver.set_window_position(570,-30)
    driver.set_window_size(925+(925-570),990)
    driver.get('https://google.com')
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()  
    popup = None
    # GHOSTERY POPUP
    try:
        popup = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="ALERT_ID_6AEC0607-8CC8-4904-BDEB-00F947E5E3C2"]/div/div[1]/div[2]')))
    except:
        print('XPATH NOT FOUND: //*[@id="ALERT_ID_6AEC0607-8CC8-4904-BDEB-00F947E5E3C2"]/div/div[1]/div[2]')
    if popup: popup.click(); popup=None
    # THE WEATHER CHANNEL
    driver.get('https://weather.com/weather/radar/interactive/l/'+seattle)
    # PRIVACY
    try:
        popup = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="meta-PrivacyDataNotice-317627f2-6930-4b56-bb60-ca7a20ec46e2"]/div/section/div/div[1]/span')))
    except: 
        print('ID NOT FOUND: //*[@id="meta-PrivacyDataNotice-317627f2-6930-4b56-bb60-ca7a20ec46e2"]/div/section/div/div[1]/span')
    if popup: popup.click(); popup=None
    # DRAWER
    try:
        popup = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="hero-right-MapRightRailDrawer-4461824e-b593-4644-8b19-3de2a48398c9"]/div/button' )))
    except:
        print('XPATH NOT FOUND: //*[@id="hero-right-MapRightRailDrawer-4461824e-b593-4644-8b19-3de2a48398c9"]/div/button')
    if popup: popup.click(); popup=None
	# RADAR/CLOUDS
    try:
        WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[5]/div[1]/ul/li[1]/button'))).click()
        WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[5]/div[2]/div[2]/div[4]/ul/li[3]'))).click()
        WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
        By.XPATH,'//*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[5]/div[2]/div[1]/button'))).click()
    except:
        print('XPATH NOT FOUND: //*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[5]/div[2]/div[2]/div[4]/ul/li[3]/img')
    driver.set_window_position(570,-30)
    return driver


def RadarRefresh(driver,sc,itr):
    print(datetime.now())
    # //*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[8]/div[2]/div[2]/sectio
    if itr>4:
        itr = 0
        driver.close()
        driver = RadarInit(webdriver.Chrome(options=options))
    else:
        itr = itr+1
        elem = None
        try:
            elem = WebDriverWait(driver,30).until(ec.visibility_of_element_located(( \
            By.XPATH,'//*[@id="hero-left-InteractiveMap-bb45c7ea-e210-4a23-add0-826b6506eaf8"]/div/div/div[5]/div[1]/ul/li[1]/button')))
            webdriver.ActionChains(driver).move_to_element(elem).perform()
            webdriver.ActionChains(driver).move_by_offset(50,50).perform()
        except:
            print('XPATH NOT FOUND: styles__overlay__1ntTq')
    sc.enter(WAIT_TIME_SECONDS, 1, RadarRefresh, (driver,sc,itr))

driver0 = HourlyInit(webdriver.Chrome(options=options))
driver1 = RadarInit(webdriver.Chrome(options=options))
s.enter(WAIT_TIME_SECONDS, 1, HourlyRefresh, (driver0,s))
s.enter(WAIT_TIME_SECONDS, 1, RadarRefresh, (driver1,s,0))
s.run()
#HourlyRefresh(driver0)
#RadarRefresh(driver1)
#exit()
