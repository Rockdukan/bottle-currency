from bottle import Bottle, TEMPLATE_PATH

from config import TEMPLATE_DIR


app = Bottle()

TEMPLATE_PATH.insert(0, TEMPLATE_DIR)
