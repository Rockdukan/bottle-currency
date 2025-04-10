from bottle import static_file

from app import app


@app.get(r"/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="app/static/css")


@app.get(r"/static/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="app/static/fonts")


@app.get(r"/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="app/static/img")


@app.get(r"/static/js/<filepath:re:.*\.(js|json)>")
def js(filepath):
    return static_file(filepath, root="app/static/js")
