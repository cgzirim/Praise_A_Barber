from app.api.app import app


@app.errorhandler(404)
def not_found(error):
    pass


@app.errorhandler(500)
def server_error(error):
    pass


@app.errorhandler(400)
def bad_request(error):
    pass
