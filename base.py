from pathlib import Path
from decouple import config
from imapclient import IMAPClient

# selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ROOT_FOLDER = Path(__file__).parent


class BaseCrawler:
    ID = None
    LOGIN = None
    PASSWORD = None
    URL = None

    def make_chrome_driver(self, *options: str, path_dowload=None) -> webdriver.Chrome:  # noqa
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Executar em modo headless  # noqa
        chrome_options.add_argument("--disable-gpu")  # Desativar aceleração de GPU  # noqa

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": str(ROOT_FOLDER / 'faturas'),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        })

        chrome_browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )
        return chrome_browser

    def make_service_email(self, username=None, password=None):
        # estabelecendo conexao e autenticando usuário
        conexao = IMAPClient(config('SERVER', str))
        conexao.login(username=config('EMAIL', str), password=config('EMAIL_PASSWORD', str))  # noqa
        return conexao

    def wait_and_click(self, by, value):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((by, value))).click()  # noqa

    def wait(self, by, value):
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((by, value)))  # noqa