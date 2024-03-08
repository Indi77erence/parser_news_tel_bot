import datetime
import random
import time
from multiprocessing import Pool

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import schedule

from config import work_period, work_days, work_time, work_start_time, work_end_time, proxy, URL
from service import text_editing


def parse_website(url):
    try:
        random_proxy = random.choice(proxy).split(":")
        proxy_host, proxy_port, proxy_username, proxy_password = random_proxy[0], random_proxy[1], random_proxy[2], random_proxy[3]
        proxy_options = {
            'proxy': {
                'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
                'no_proxy': 'localhost:127.0.0.1'
            }
        }
        driver = webdriver.Chrome(seleniumwire_options=proxy_options, service=ChromeService(ChromeDriverManager().install()))
        actions = ActionChains(driver)
        driver.get(url=url)
        element = driver.find_element(By.CLASS_NAME, "cell")
        actions.move_to_element(element).perform()
        element.click()
        article_title = driver.find_element(By.CLASS_NAME, "post_content").find_element(By.TAG_NAME, "h1").text
        parent_element = driver.find_element(By.CLASS_NAME, "post_content").find_element(By.TAG_NAME,
                                                                                         "h1").find_element(By.XPATH,
                                                                                          "..")
        tags = driver.find_element(By.CLASS_NAME, 'post_tags_top').find_element(By.TAG_NAME, "a").text
        post_content_element = driver.find_element(By.CLASS_NAME, "post_content")
        text_article = post_content_element.find_elements(By.TAG_NAME, "p")[:-1:]
        text_editing(article_title, tags, text_article, parent_element)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


def run_parser():
    p = Pool(processes=len(URL))
    p.map(parse_website, URL)


def start_parser():
    current_day = datetime.datetime.now().strftime("%A").lower()
    if current_day in work_days:
        for wt in work_time:
            schedule.every().day.at(wt).do(run_parser)
    else:
        schedule.clear()


def start_parser_period():
    cron_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    cron_time_str = cron_time.strftime("%H:%M")
    current_day = datetime.datetime.now().strftime("%A").lower()
    if current_day in work_days:
        schedule.every().day.at(cron_time_str).do(run_parser)
    else:
        schedule.clear()


def parser_main():
    if work_period == "off":
        schedule.every().day.at(work_start_time).do(start_parser)
        schedule.every().day.at(work_end_time).do(schedule.clear)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        schedule.every(work_period).minutes.do(start_parser_period)
        schedule.every().day.at(work_end_time).do(schedule.clear)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    parser_main()


