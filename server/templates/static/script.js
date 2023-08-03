// 10.7.22.93:8000/search.html
// cd site
// python -m http.server -b 0.0.0.0 8000

function search()
{
    var input = document.getElementById("searchWord").value;
    var searchWord = input.replace(/%/g, ".*");
    searchWord = "\\b" + searchWord + "\\b";
    fetch("static/data.csv")
        .then(response => response.text())
        .then(data => processCSV(data, searchWord));
}

function processCSV(csvData, searchWord)
{
    var rows = csvData.split("\n");
    var results = {};

    for (var i = 0; i < rows.length; i++)
    {
        var rowElements = rows[i].split(",");
        var word = rowElements[0];
        var chapters = rowElements.slice(1);

        var regex = new RegExp(searchWord, "i");
        if (word.match(regex))
        {
            if (!results[word])
            {
                results[word] = [];
            }
            results[word].push(chapters);
        }
    }

    displayResults(results);
}

async function getFullName(chapterCode)
{
    // Загрузим содержимое bookmarks.csv
    return await fetch("static/bookmarks.csv")
                    .then(response => response.text())
                    .then(data => 
                    {
                        // Разобьем данные на строки
                        let lines = data.split("\n");
                        
                        // Пройдем по строкам и найдем полное имя по chapterCode
                        for (let i = 0; i < lines.length; i++)
                        {
                            //console.log(lines[i] + "---" + chapterCode);
                            if (lines[i].includes(chapterCode))
                                {
                                    return "#page=" + (lines[i].split(';'))[1];
                                }
                        }

                        return ""; // Если не найдено, вернем пустую строку
                    });
}

async function displayResults(results) 
{
    var resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    var words = Object.keys(results);
    if (words.length === 0)
    {
        resultsDiv.innerHTML = "Слово не найдено.";
        return;
    }

    var table = document.createElement("table");
    for (var i = 0; i < words.length; i++)
    {
        var word = words[i];
        var chaptersList = results[word];

        var row = table.insertRow();
        var cell = row.insertCell();
        cell.innerHTML = "<strong>" + word + "</strong>";

        for (var j = 0; j < chaptersList.length; j++)
        {
            var chapters = chaptersList[j];

            for (var k = 0; k < chapters.length; k++)
            {
                var chapterData = chapters[k].split(" ");
                var chapterCode = chapterData[0];
                var chapterPage = chapterData[1];
                
                var fullName = await getFullName(chapterCode);

                var link = document.createElement("a");
                link.href = "static/aipc/" + chapterCode.substr(0, 5) + "___104.pdf" + fullName;
                link.textContent = chapterCode;

                var row = table.insertRow();
                var cellChapter = row.insertCell();
                cellChapter.appendChild(link);
                cellChapter.innerHTML += "<br>" + chapterPage;
            }
        }
    }
    resultsDiv.appendChild(table);

    var links = document.getElementsByTagName("a");
    for (var i = 0; i < links.length; i++)
    {
        links[i].addEventListener("click", loadPDF);
    }

    //await extractAndSavePages()
}

function loadPDF(event)
{
    event.preventDefault();
    var pdfUrl = event.target.href;
    var pdfFrame = document.getElementById("pdfFrame");
    pdfFrame.src = pdfUrl;
}

async function extractAndSavePages(pdfUrl) {
    // Загрузим PDF-файл
    const loadingTask = pdfjsLib.getDocument(pdfUrl);
    const pdfDocument = await loadingTask.promise;

    // Создадим два PDF-документа для картинок и таблиц
    const imgDocument = await PDFLib.PDFDocument.create();
    const tableDocument = await PDFLib.PDFDocument.create();

    // Пройдем по каждой странице и разделим их на две группы
    for (let i = 0; i < pdfDocument.numPages; i++) {
        const page = await pdfDocument.getPage(i + 1);
        const pageLabel = await page.getDisplayLabel();

        // Получим список закладок для текущей страницы
        const bookmarks = await pdfDocument.getDestination(pageLabel);

        // Проверим, есть ли подзакладки с именами "PAGE 0"
        if (bookmarks.some(bookmark => bookmark.startsWith("PAGE 0"))) {
            // Это страница с картинками
            const copiedPage = await imgDocument.copyPages(pdfDocument, [i]);
            imgDocument.addPage(copiedPage[0]);
        } else {
            // Это страница с таблицами
            const copiedPage = await tableDocument.copyPages(pdfDocument, [i]);
            tableDocument.addPage(copiedPage[0]);
        }
    }

    // Сохраняем два документа в отдельные файлы
    const imgBytes = await imgDocument.save();
    const tableBytes = await tableDocument.save();

    // Создаем и загружаем ссылки на файлы
    const imgBlob = new Blob([imgBytes], { type: "application/pdf" });
    const tableBlob = new Blob([tableBytes], { type: "application/pdf" });

    const imgUrl = URL.createObjectURL(imgBlob);
    const tableUrl = URL.createObjectURL(tableBlob);

    // Открываем ссылки в новых окнах браузера
    window.open(imgUrl, "_blank");
    window.open(tableUrl, "_blank");
}
