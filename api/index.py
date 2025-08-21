import sys
import os

# Add the back-end directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'back-end'))

try:
    from app.main import app
    from mangum import Mangum
    
    # Create a handler for AWS Lambda / Vercel
    handler = Mangum(app, lifespan="off")
    
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback handler for debugging
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Import error: {e}"
        }

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
