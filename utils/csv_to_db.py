import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Session

# Создание базового класса для моделей
class Base(DeclarativeBase):
    pass

# Определение модели для таблицы "PartNumbers"
class PartNumber(Base):
    __tablename__ = 'partnumbers'
    
    partnumber_id = Column(Integer, primary_key=True)
    partnumber = Column(String)
    position_number = Column(Integer)
    
    sections = relationship("Bookmark", secondary='part_section_association', back_populates="partnumbers")

# Определение модели для таблицы "Bookmarks"
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    section_id = Column(Integer, primary_key=True)
    section_number = Column(String)
    section_name = Column(String)
    page = Column(Integer)
    
    partnumbers = relationship("PartNumber", secondary='part_section_association', back_populates="sections")

# Создание связующей таблицы для связи многие-ко-многим
part_section_association = Table('part_section_association', Base.metadata,
    Column('partnumber_id', Integer, ForeignKey('partnumbers.partnumber_id')),
    Column('section_id', Integer, ForeignKey('bookmarks.section_id'))
)

# Создание базы данных
engine = create_engine('sqlite:///server/templates/static/catalog.db', echo=True)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
session = Session(bind=engine)

# Чтение данных из файла bookmarks.csv и добавление в базу данных
# with open('server/templates/static/bookmarks.csv', 'r') as bookmarks_file:
#     bookmarks_reader = csv.reader(bookmarks_file, delimiter=',')
#     for row in bookmarks_reader:
#         section_number, bookmark_data = row[0], ''.join(row[1:]).split(';')
#         section_name = bookmark_data[0]
#         page_number = int(bookmark_data[1])
        
#         new_section = Bookmark(section_number=section_number, section_name=section_name, page=page_number)
#         session.add(new_section)
#         session.commit()

# Чтение данных из файла partnumbers.csv и добавление в базу данных
with open('server/templates/static/data.csv', 'r') as partnumbers_file:
    partnumbers_reader = csv.reader(partnumbers_file, delimiter=',')
    for row in partnumbers_reader:
        partnumber = row[0]
        for section_data in row[1:]:
            section_number, position_number = section_data.split()
            new_partnumber = PartNumber(partnumber=partnumber, position_number=position_number)
            session.add(new_partnumber)
            session.flush()
            session.refresh(new_partnumber)
        
            existing_section = session.query(Bookmark).filter_by(section_number=section_number).first()
            if existing_section:
                existing_section.partnumbers.append(new_partnumber)
session.commit()