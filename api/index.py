from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Create a lightweight FastAPI app for Vercel
app = FastAPI(title="API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "incision-metric-data-uploader-api"}

@app.get("/organizations")
async def get_organizations():
    # Mock data for demo purposes
    return [
        {"id": 1, "name": "Demo Hospital", "type": "NHS"},
        {"id": 2, "name": "Demo Clinic", "type": "Private"},
        {"id": 3, "name": "Demo Medical Center", "type": "Community"}
    ]

@app.post("/organizations")
async def create_organization(organization: dict):
    # Mock creation for demo
    return {"message": "Organization created", "id": 123, "data": organization}

# Create handler for Vercel
handler = Mangum(app, lifespan="off")
