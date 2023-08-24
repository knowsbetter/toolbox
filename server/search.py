import re

data_csv_file = "server/templates/static/data.csv"
bookmarks_csv_file = "server/templates/static/bookmarks.csv"

# Search starts here
def search(search_word: str):
    with open(data_csv_file, "r") as csv_file:
        csv_data = csv_file.read()
        results = process_csv(csv_data, search_word)
        return results

# Main search loop
def process_csv(csv_data, search_word):
    rows = csv_data.split("\n")
    results = {}

    for row in rows:
        row_elements = row.split(",")
        word = row_elements[0]
        chapters = row_elements[1:]

        regex = re.compile(search_word, re.I)
        if regex.search(word):
            results[word] = {}
            links = []
            for chapter in chapters:
                links.append([f'{chapter}', pdf_link(chapter.split(" ")[0])])
            results[word] = links
    return results

# Returns a link to a given chapter code
def pdf_link(chapter_code: str):
    full_name = get_full_name(chapter_code)
    pdf_link = f"static/aipc/{chapter_code[:5]}___104.pdf{full_name}"
    return pdf_link

# Returns a specific number of page for a given chapter code processing bookmarks
def get_full_name(chapter_code):
    with open(bookmarks_csv_file, "r") as bookmarks_file:
        lines = bookmarks_file.readlines()
        for line in lines:
            if chapter_code in line:
                return "#page=" + line.split(";")[1][:-1]
    return ""