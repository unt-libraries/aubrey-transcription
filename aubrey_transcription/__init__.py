import os
import re

from flask import Flask

from . import aubrey_transcription


def create_app(test_config=None, instance_path=None):
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    # Try to create the instance directory. Put a settings file here to override default config.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set configuration. Ascending priority is test_config, then config file, then default config.
    app.config.from_object('aubrey_transcription.default_settings')  # Load default settings first.
    filename = os.path.join(app.instance_path, 'settings.py')
    app.config.from_pyfile(filename, silent=True)  # Override with settings file if it exists.
    # Override with test_config settings if provided.
    if test_config:
        app.config.from_mapping(test_config)

    app.register_blueprint(aubrey_transcription.bp)

    # Compile and save the regex pattern so we don't have to do it for every request.
    app.config['FILENAME_REGEX'] = re.compile(app.config['FILENAME_PATTERN'])

    return app
