from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.llm_debug import router as llm_debug_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Car Recommendation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router,prefix="/api")
app.include_router(llm_debug_router, prefix="/api")

@app.get("/")
def health():
    return {
        "status": "healthy",
        "message": "AI Car Recommendation API is running"
    }