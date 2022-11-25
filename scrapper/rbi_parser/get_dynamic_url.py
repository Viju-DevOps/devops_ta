from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import platform
from webdriver_manager.chrome import ChromeType
import time
from selenium.webdriver.support.wait import WebDriverWait


def get_rbi_dynamic_url(rbi_url):
    """ Function to get dynamic rbi url

    Args:
        rbi_url: main url of the RBI

    Returns: returns the dynamic url of the RBI

    """
    # driver = __setup_chrome()
    driver = __setup_firefox()
    rbi_dynamic_url = ''
    driver.get(rbi_url)
    html_button_element = '//a[@class="documentlinks uw-link-btn" and contains(text(), "HTML")] | //a[@class="documentlinks uw-link-btn" and contains(text(), "Html")] | //*[@id="node-677589"]/div/div/div/p[2]/span/span/span/span/span/span/a[3]'
    if WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH, html_button_element)):
        html_button = driver.find_elements(By.XPATH, html_button_element)[0]
        html_button.send_keys(Keys.ENTER)
        dynamic_page_table_element = '//table[@id="sanctions"]'
        if WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH, dynamic_page_table_element)):
            rbi_dynamic_url = driver.current_url
    driver.close()
    return rbi_dynamic_url


def __setup_chrome() -> webdriver:
    """Setup Chrome web driver.

    Returns: A new local chrome driver.
    """
    chrome_prefs = {}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--window-size={1440,900}")
    chrome_options.add_argument("--incognito")
    if platform.system() == "Darwin" or platform.system() == "Linux":
        chrome_options.add_argument("--kiosk")
    else:
        chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"popups": 1}
    chrome_options = Options()
    chrome_options.add_argument('-headless')
    return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                            chrome_options=chrome_options)


def __setup_firefox() -> webdriver:
    """Setup firefox web driver.

    Returns: A new local firefox driver
    """
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    firefox_profile.set_preference("dom.disable_open_during_load", False)
    firefox_profile.accept_untrusted_certs = True
    firefox_options = Options()
    # firefox_options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=firefox_profile,
                               options=firefox_options)
    driver.maximize_window()
    return driver
