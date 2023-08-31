from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.repository.statements import get_sections, TableGenerator

app = FastAPI()
table = None

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
    global table
    """Search for a part number in index and return results"""
    table = TableGenerator(get_sections(search_word))
    #response = {'words': list(results.keys()), 'results': list(results.values())}
    return {'detail': 'ok'}

@app.get('/iterate')
async def iterate_table():
    try:
        result = next(table)
        response = {'words': list(result.keys()), 'results': list(result.values())}
    except StopIteration:
        response = {}
    print(response)
    return response

# uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload