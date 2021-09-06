import logging
import sys
import time
from settings import *


def get_logger(name=__file__, file='./output/'+str(time.strftime("%Y%m%d-%H%M%S"))+'_'+network[0]+'_log.txt', encoding='utf-8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log

log = get_logger()
print = log.debug