import os
import importlib
import sys
import logging


def main():
    if len(sys.argv) != 2:
        print("Uso: python arquivo.py <ID>")
        return

    id_modulo = sys.argv[1]
    buscar_e_executar_modulo(id_modulo)


def buscar_e_executar_modulo(id_modulo):
    for pasta_raiz, subpastas, arquivos in os.walk("crawler"):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(".py") and not nome_arquivo.startswith('__') and not nome_arquivo.startswith('base'):
                caminho_arquivo = os.path.join(pasta_raiz, nome_arquivo)
                modulo = importar_modulo(caminho_arquivo)
                executar_modulo_por_id(modulo, id_modulo)


def importar_modulo(caminho_arquivo):
    modulo_path = caminho_arquivo.replace(os.path.sep, ".")[:-3]
    return importlib.import_module(modulo_path)


def executar_modulo_por_id(modulo, id_modulo):
    for nome_classe in dir(modulo):
        if nome_classe.startswith('Crawler'):
            classe = getattr(modulo, nome_classe)
            if hasattr(classe, "ID") and classe.ID == int(id_modulo):
                crawler = classe()
                crawler.run()
                return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # noqa
    main()
