from selenium import webdriver


class WebClient:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self._driver = webdriver.Chrome(chrome_options=chrome_options)

    def get_rendered_content(self):
        return self._driver.page_source

    def render_url(self, url):
        self._driver.get(url)

    def close_page(self):
        self._driver.close()

    def close_browser(self):
        self._driver.quit()
