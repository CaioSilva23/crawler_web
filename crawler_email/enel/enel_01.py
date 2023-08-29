import logging
import email
from base import BaseCrawler
from time import sleep


class CrawlerEnelEmail(BaseCrawler):
    ID = 1

    def __init__(self):
        logging.info('Inicializando Crawler Email (Enel).')
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

            if 'Enel' in msg["Subject"]:
                emails.append(msg)
        return emails

    def baixar_fatura(self):
        # Processar o corpo do email
        emails = self.processa_resultados()
        if emails:
            logging.info('Baixando faturas...')
            for msg in emails:
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() != "text/html":
                            filename = part.get_filename()
                            if filename:
                                attachment = part.get_payload(decode=True)
                                with open(f'faturas/{filename}', "wb") as f:
                                    f.write(attachment)
            logging.info(f'{len(emails)} faturas baixadas com sucesso.')
            sleep(2)
            self.conexao.logout()
        else:
            logging.info('Nenhuma fatura foi encontrada.')
