from kpo import app, logger

def test_logger():
    """
    Jednostavna funkcija za testiranje loggera kroz različite nivoe logovanja.
    """
    logger.debug('Ovo je DEBUG poruka iz test_logger.py')
    logger.info('Ovo je INFO poruka iz test_logger.py')
    logger.warning('Ovo je WARNING poruka iz test_logger.py')
    logger.error('Ovo je ERROR poruka iz test_logger.py')
    logger.critical('Ovo je CRITICAL poruka iz test_logger.py')
    
    # Simuliramo različite događaje u aplikaciji
    logger.info('Korisnik se prijavio na sistem')
    logger.warning('Neuspešan pokušaj prijave')
    logger.error('Greška prilikom pristupa bazi podataka')
    
    print('Test logovanja je završen. Proverite logs/kpo.log fajl za rezultate.')

if __name__ == '__main__':
    with app.app_context():
        test_logger()
        logger.info('Test logovanja je završen')
