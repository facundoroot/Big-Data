import logging

logging.basicConfig(
    format='%(name)s-%(asctime)s::%(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger('Dag generator')
