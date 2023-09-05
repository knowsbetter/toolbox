from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.db_service import get_current_db_service, DatabaseService
import socket

app = FastAPI()
#db_service = DatabaseService()

# Place static folder of the project to the root of server app
app.mount("/static", StaticFiles(directory="server/templates/static"), name="static")
# Location of html templates
templates = Jinja2Templates(directory="server/templates")

@app.on_event('startup')
async def start():
    hostname = socket.getfqdn()
    print("Started at:",f'{socket.gethostbyname_ex(hostname)[2][-1]}:8000')

@app.get('/js')
async def index(request: Request):
    """Work with frontend version"""
    return templates.TemplateResponse("index.html", {'request': request})

@app.get('/')
async def index(request: Request):
    """Work with backend version"""
    return templates.TemplateResponse("search.html", {'request': request})

@app.get('/search')
async def search_word(search_word: str, db_service: DatabaseService=Depends(get_current_db_service)):
    db_service.set_search_word(search_word)
    return {'detail': 'ok'}

@app.get('/iterate_results')
async def iterate_table(db_service: DatabaseService=Depends(get_current_db_service)):
    return db_service.get_result()

# uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload