from database.db import session
from sqlalchemy import select
from database.orm_models.models import PartNumber

class TableGenerator:
    
    def __init__(self, body: dict):
        self.index = -1
        self.body = body
        self.keys = list(body.keys())
        self.length = len(self.keys)

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        if self.index < self.length - 1:
            self.index += 1
            return {self.keys[self.index]: self.body[self.keys[self.index]]}
        else:
            raise StopIteration
        

def get_sections(partnumber: str):
    results = {}
    prev_pn = ""
    with session:
        query = select(PartNumber).where(PartNumber.partnumber.like(f"%{partnumber}%"))
        partnumbers: list[PartNumber] = session.scalars(query).all()
        if partnumbers:
            for pn in partnumbers:
                if prev_pn != pn.partnumber:
                    results[f'{pn.partnumber}'] = []
                prev_pn = pn.partnumber
                for bookmark in pn.sections:
                    filename = f"static/aipc/{bookmark.section_number[:5]}___104.pdf#page={bookmark.page}"
                    results[f'{pn.partnumber}'].append([bookmark.section_number, 
                                                        bookmark.section_name, 
                                                        pn.position_number, 
                                                        filename])
    return results