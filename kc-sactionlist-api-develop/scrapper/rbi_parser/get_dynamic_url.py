from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import platform
from webdriver_manager.chrome import ChromeType
import time


def get_rbi_dynamic_url(rbi_url):
    """ Function to get dynamic rbi url

    Args:
        rbi_url: main url of the RBI

    Returns: returns the dynamic url of the RBI

    """
    # driver = __setup_chrome()
    driver = __setup_firefox()
    driver.get(rbi_url)
    time.sleep(5)
    html_button = driver.find_elements(By.XPATH, '//a[@class="documentlinks uw-link-btn" and contains(text(), '
                                                 '"HTML")]')[0]
    html_button.send_keys(Keys.ENTER)
    time.sleep(2)
    rbi_dynamic_url = driver.current_url
    driver.close()
    return rbi_dynamic_url


def __setup_chrome() -> webdriver:
    """Setup Chrome web driver.

    Returns: A new local chrome driver.
    """
    chrome_prefs = {}
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("headless")
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
    firefox_options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=firefox_profile,
                               options=firefox_options)
    driver.maximize_window()
    return driver
