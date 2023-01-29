import os
from config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
from selenium.webdriver.common.by import By



try:
	
	
	updater = Updater(token = Config.BOT_TOKEN, use_context=True)
	dp = updater.dispatcher
	options = webdriver.ChromeOptions()
	options.add_argument("-profile")
	options.add_argument(s)
	#profile = FirefoxProfile()
	#profile.set_preference("dom.webdriver.enabled", False)
	#profile.set_preference('useAutomationExtension', False)
	#profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/60.0.3112.50 Safari/537.36")
	#profile.update_preferences()
	desired = DesiredCapabilities.FIREFOX
	options.add_argument("--disable-infobars")
	#options.add_argument("--headless")
	#options.add_argument("--window-size=1200,800")
	options = Options()
	options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
	options.add_argument("--disable-blink-features=AutomationControlled")
	#browser = webdriver.Firefox(options=options, firefox_profile=profile, desired_capabilities=desired, service_args=["--marionette-port", "2828"])
	browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options ,desired_capabilities=desired, service_args=["--marionette-port", "2828"])
	#browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
except Exception as e:
	print(e)
