from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase

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

    def __str__(self) -> str:
        return f"partnumber_id: {self.partnumber_id}, partnumber: {self.partnumber}, " + \
                f"position_number: {self.position_number}"

# Определение модели для таблицы "Bookmarks"
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    section_id = Column(Integer, primary_key=True)
    section_number = Column(String)
    section_name = Column(String)
    page = Column(Integer)
    
    partnumbers = relationship("PartNumber", secondary='part_section_association', back_populates="sections")

    def __str__(self) -> str:
        return f"section_id: {self.section_id}, section_number: {self.section_number}, " + \
                f"section_name: {self.section_name}"

# Создание связующей таблицы для связи многие-ко-многим
part_section_association = Table(
    'part_section_association',
    Base.metadata,
    Column('partnumber_id', Integer, ForeignKey('partnumbers.partnumber_id')),
    Column('section_id', Integer, ForeignKey('bookmarks.section_id'))
)