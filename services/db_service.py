from database.repository.statements import get_sections

class DatabaseService:

    def __init__(self, search_word=""):
        self._search_word = search_word
        self.index = 0

    def set_search_word(self, search_word):
        self._search_word = search_word
        self.index = 0

    def get_result(self):
        result = get_sections(self._search_word, self.index)
        response = {}
        if result:
            response = {'words': list(result.keys()), 'results': list(result.values())}
            self.index += 1
        return response
    
def get_current_db_service():
    global _database_service
    if not _database_service:
        _database_service = DatabaseService()
    return _database_service
    
_database_service = None