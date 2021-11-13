from flask import Flask

from application.rest import snippet


def create_app(config_name):
    
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    app.register_blueprint(snippet.blueprint)

    return app