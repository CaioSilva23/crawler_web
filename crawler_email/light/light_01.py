import logging
import email
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import base
from time import sleep


class CrawlerLightEmail(base.BaseCrawler):
    ID = 2

    def __init__(self):
        logging.info('Inicializando Crawler Email (Light).')
        self.conexao = self.make_service_email()  # noqa
        self.baixar_fatura()

    def processa_resultados(self):
        logging.info('Buscando os emails...')
        emails = list()
        self.conexao.select_folder("INBOX")
        resultados = self.conexao.search(["SUBJECT", 'sua fatura'])
        for _, data in self.conexao.fetch(resultados, ["RFC822"]).items():  # noqa
            mensagem = data[b"RFC822"]
            # Criar um objeto de mensagem do email
            msg = email.message_from_bytes(mensagem)

            if 'Light' in msg["Subject"]:
                emails.append(msg)
        return emails

    def baixar_fatura(self):
        links_faturas = list()

        # Processar o corpo do email
        emails = self.processa_resultados()
        if emails:
            logging.info('Baixando faturas...')
            for msg in emails:
                corpo = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            corpo = part.get_payload(decode=True).decode("latin-1", errors="replace")  # noqa
                            break
                else:
                    corpo = msg.get_payload(decode=True).decode("utf-8")
                links_faturas.append(BeautifulSoup(corpo, "html.parser").find_all("a")[0].get('href'))  # noqa

            self.driver = self.make_chrome_driver()
            for link in links_faturas:
                self.driver.get(link)
                self.wait_and_click(By.ID, 'download-button')
            logging.info(f'{len(emails)} faturas baixadas com sucesso.')
            sleep(2)
            self.driver.quit()
            self.conexao.logout()
        else:
            logging.info('Nenhuma fatura foi encontrada.')
