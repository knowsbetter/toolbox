from database.db import session
from sqlalchemy import select
from database.orm_models.models import Base, PartNumber, Bookmark, part_section_association

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
                    results[f'{pn.partnumber}'].append([bookmark.section_number, bookmark.section_name, pn.position_number, filename])
    return results
