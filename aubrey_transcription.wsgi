import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(BASE_DIR, 'env')

# This app may not be installed, so add the project path to the system path.
sys.path.insert(0, BASE_DIR)

# Activate the virtual environment.
activate_this = os.path.join(ENV, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# Initialize the app.
from aubrey_transcription import create_app
application = create_app()
