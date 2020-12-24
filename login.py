from selenium import webdriver
from selenium.webdriver import ChromeOptions


def login(url):
    path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=path, options=option)
    driver.get(url)
    driver.find_element_by_css_selector(
        '#root > div:nth-child(2) > div.container-pc > div > div.modal > div > a.kw-icon-input-close.close').click()
    driver.find_element_by_class_name('wrap-not-login').click()
    driver.find_element_by_css_selector('#root > div:nth-child(2) > div.wrap > div:nth-child(2) > div > div > div.account-container > ul > li:nth-child(2) > span').click()
    driver.find_element_by_xpath(
        '//*[@id="root"]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/form[2]/div[1]/input').send_keys('18735123416')
    driver.find_element_by_css_selector('#root > div:nth-child(2) > div.wrap > div:nth-child(2) > div > div > div.account-container > div > div > div > form:nth-child(2) > div:nth-child(2) > input').send_keys('74108520!')
    driver.find_element_by_css_selector('#root > div:nth-child(2) > div.wrap > div:nth-child(2) > div > div > div.account-container > div > div > button').click()
    quit()


if __name__ == '__main__':
    login('https://edu.lagou.com/')
