from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="server/templates/static"))
templates = Jinja2Templates(directory="server/templates")

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html",{'request': request})