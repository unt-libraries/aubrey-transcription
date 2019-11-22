import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(BASE_DIR, 'env')

# This app may not be installed, so add the project path to the system path.
sys.path.insert(0, BASE_DIR)

# Initialize the app.
from aubrey_transcription import create_app
application = create_app()
