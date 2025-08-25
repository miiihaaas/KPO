import logging
import os
from logging.handlers import RotatingFileHandler

# Kreiraj logs direktorijum ako ne postoji
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Konfiguriši logger
logger = logging.getLogger('kpo_test')
logger.setLevel(logging.DEBUG)

# Postavi formater
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Konfigurišemo rotating file handler
file_handler = RotatingFileHandler('logs/kpo_test.log', maxBytes=1024*1024, backupCount=9)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Konfigurišemo stream handler za konzolni izlaz
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Dodajemo handlere loggeru
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def test_logger():
    """
    Jednostavna funkcija za testiranje loggera kroz različite nivoe logovanja.
    """
    logger.debug('Ovo je DEBUG poruka iz simple_logger_test.py')
    logger.info('Ovo je INFO poruka iz simple_logger_test.py')
    logger.warning('Ovo je WARNING poruka iz simple_logger_test.py')
    logger.error('Ovo je ERROR poruka iz simple_logger_test.py')
    logger.critical('Ovo je CRITICAL poruka iz simple_logger_test.py')
    
    # Simuliramo različite događaje u aplikaciji
    logger.info('Korisnik se prijavio na sistem')
    logger.warning('Neuspešan pokušaj prijave')
    logger.error('Greška prilikom pristupa bazi podataka')
    
    print('Test logovanja je završen. Proverite logs/kpo_test.log fajl za rezultate.')

if __name__ == '__main__':
    test_logger()
