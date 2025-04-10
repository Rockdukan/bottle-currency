from app import app, log
from app.controllers import html, static
from app.extensions import db
from app.models.currency import CurrencyRate
from config import HOST, PORT, DEBUG, RELOADER


db.connect()
db.create_tables([CurrencyRate])

if __name__ == "__main__":
    app.run(
    	host=HOST,
    	port=PORT,
    	debug=DEBUG,
    	reloader=RELOADER)
