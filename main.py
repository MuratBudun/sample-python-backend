from dotenv import load_dotenv
load_dotenv()

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.splash import show_splash
from common.registry import register_app

show_splash()

app = register_app()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
   return JSONResponse(
      status_code=exc.status_code,
      content={"detail": exc.detail},
      headers=exc.headers
   )

# Debugging
import uvicorn
if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=5000)