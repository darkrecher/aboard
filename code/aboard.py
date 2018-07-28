# -*- coding: UTF-8 -*-

# Pour lancer ce code dans une console MingW32, utiliser la commande :
# winpty python aboard.py
# Et non pas :
# python aboard.py
# C'est une contrainte liée à MingW32. Les scripts python interactifs, ou qui envoient de l'utf-8 sur la sortie standard,
# doivent être lancé avec "winpty".

import sys
import logging

# https://stackoverflow.com/questions/2302315/how-can-info-and-debug-logging-message-be-sent-to-stdout-and-higher-level-messag

class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        #non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0

#Get the root logger
logger = logging.getLogger()
#Have to set the root logger level, it defaults to logging.WARNING
logger.setLevel(logging.NOTSET)

logging_handler_out = logging.StreamHandler(sys.stdout)
logging_handler_out.setLevel(logging.INFO)
logger.addHandler(logging_handler_out)

logging_handler_err = logging.StreamHandler(sys.stderr)
logging_handler_err.setLevel(logging.DEBUG)
logging_handler_err.addFilter(LessThanFilter(logging.INFO))
logger.addHandler(logging_handler_err)

#demonstrate the logging levels
#logger.debug('DEBUG')
#logger.info('INFO')
#logger.warning('WARNING')
#logger.error('ERROR')
#logger.critical('CRITICAL')

# Alias de fonction
debug = logger.debug
answer = logger.info
log = logger.info

debug("debug. Avéc des àccents. Hââ ha. αβ")
answer("answer. Avéc des àccents. Hââ ha. αβ")

#class
