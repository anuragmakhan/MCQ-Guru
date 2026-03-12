import logging


def ERR(strn):
    logger(strn, _level =logging.ERROR)

def INF(strn):
    logger(strn, _level =logging.INFO)

def DBG(strn):
    logger(strn, _level =logging.DEBUG)

def logger(strn,_level):
    logging.basicConfig(filename='logs/app.log', filemode='a', format='[%(asctime)s][%(levelname)s][%(message)s]', level=_level)
    logging.info(strn)
    #logging.error('%s raised an error', )
