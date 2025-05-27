from flask import Flask
from .gpio_controller import GPIOController

def create_app():
    app = Flask(__name__)
    app.config['GPIO'] = GPIOController(mock=True)

    from . import routes
    app.register_blueprint(routes.bp)

    return app