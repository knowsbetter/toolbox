from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from server.search import *
from database.repository.statements import get_sections

app = FastAPI()

# Place static folder of the project to the root of server app
app.mount("/static", StaticFiles(directory="server/templates/static"), name="static")
# Location of html templates
templates = Jinja2Templates(directory="server/templates")

@app.get('/js')
async def index(request: Request):
    """Work with frontend version"""
    return templates.TemplateResponse("index.html", {'request': request})

@app.get('/')
async def index(request: Request):
    """Work with backend version"""
    return templates.TemplateResponse("search.html", {'request': request})

@app.get('/search')
async def search_word(search_word: str):
    """Search for a part number in index and return results"""
    #results = search(search_word)
    results = get_sections(search_word)
    response = {'words': list(results.keys()), 'results': list(results.values())}
    return response

# uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload