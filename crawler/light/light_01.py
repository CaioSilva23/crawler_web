from time import sleep
import logging
from decouple import config

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base import BaseCrawler


class CrawlerLight(BaseCrawler):
    ID = 2
    LOGIN = config('LOGIN', str)
    PASSWORD = config('PASSWORD', str)
    URL = config('PORTAL_LIGHT', str)

    def __init__(self):
        logging.info('Inicializando Crawler Light.')

    def run(self):
        self.driver = self.make_chrome_driver()
        self.login()
        self.download_faturas_atual()
        self.download_faturas()
        sleep(10)
        self.driver.quit()

    def login(self):
        logging.info('Realizando login no sistema.')
        self.driver.get(self.URL)

        # botão entrar 
        self.wait_and_click(By.XPATH, "(//div[@class='btn-default btn-menu transition'])[1]")  # noqa

        # Aceitando os cookies para nao sobrepor os outros elementos
        self.wait_and_click(By.ID, 'onetrust-accept-btn-handler')

        # inserindo login de usuário
        input_login = self.driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input')  # noqa
        input_login.send_keys(self.LOGIN)

        # inserindo senha
        input_password = self.driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/input')  # noqa
        input_password.send_keys(self.PASSWORD)
        input_password.send_keys(Keys.ENTER)

    def download_faturas_atual(self):
        logging.info('Realizando download da fatura atual.')
        # card segunda via de fatura
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div[1]/div[1]/div/div[1]/div[1]/span/span/div/span/div[1]/a')  # noqa

        # exibindo fatura disponível
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div[2]/span/div/div[2]/div[1]/div/div/div[3]/span/span/div')  # noqa

        # botão download
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div[2]/span/div/div[2]/div[1]/div/div/div[3]/span/span/div/div/div[2]/div[2]/div[1]/span/span/div/div/div[2]/div[2]/div/div[2]/a')  # noqa

        # selecionando o motivo para download
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div[2]/span/div/div[2]/div[1]/div/div/div[3]/span/span/div/div/div[2]/div[2]/div[1]/div[2]/span[2]/div/div/div[2]/span/div[3]/div[1]/div[3]/div/select/option[2]')  # noqa
        sleep(1)

        # baixando fatura
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div[2]/span/div/div[2]/div[1]/div/div/div[3]/span/span/div/div/div[2]/div[2]/div[1]/div[2]/span[2]/div/div/div[2]/span/div[3]/div[2]/div/div[2]/div/div/div/span/input')  # noqa
        logging.info('Fatura atual foi baixada com sucesso.')

        # aguarda o modal fechar para seguir
        self.wait(By.XPATH, '//*[@id="AGV_UI_th_wt23_block_OutSystemsUIWeb_wt25_block_wtContent_wtMainContent_OutSystemsUIWeb_wt29_block_wtTabs_Content_OutSystemsUIWeb_wt20_block_wtContent_wt26_wtInstalacaoListRecords_ctl00_OutSystemsUIWeb_wt15_block_wtContent_AGV_Componentes_comuns_wt20_block_wtContent_wt4_OutSystemsUIWeb_wtModalDownloadFatura_block_wtContent_wtModalDownloadFaturaWb_wt3_OutSystemsUIWeb_wt14_block_wtMainContent_wtTitulo"]')

        sleep(2)
        # voltando para tela de home
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div[1]/div/div/div/div[1]/a')  # noqa

    def download_faturas(self):
        logging.info('Realizando downloads das faturas pagas.')
        # card faturas pagas
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div[1]/div[1]/div/div[1]/div[1]/span/span/div/span/div[7]/a')  # noqa
        # input check box
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div/div[2]/div/span/div/div[2]/div[1]/div[1]/div[2]/div/span/span/div/div[1]/div/div[1]/input')  # noqa
        sleep(2)
        # botao downloads faturas pagas
        self.wait_and_click(By.XPATH, '/html/body/form/div[4]/div/div/main/div/div[1]/div/div/div/div[2]/div/span/div/div[2]/div[1]/div[1]/div[2]/div/span/span/div/div[1]/div/div[1]/a[1]')  # noqa
        logging.info('Faturas baixadas com sucesso.')
