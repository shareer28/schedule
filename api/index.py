import sys
import os

# Add the back-end directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'back-end'))

from app.main import app
from mangum import Mangum

# Create a handler for AWS Lambda / Vercel
handler = Mangum(app)
