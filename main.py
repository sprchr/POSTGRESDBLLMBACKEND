#main.py
from fastapi import FastAPI
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="NL-to-SQL API", description="Convert natural language to SQL queries.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
