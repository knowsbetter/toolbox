async function updateTable(cont)
{
    const resultTable = document.getElementById("results");

    const response = await fetch(`/iterate`);
    const data = await response.json();

    if (data.words && data.results)
    {
        const words = data.words;
        for (let i = 0; i < words.length; i++)
        {
            const word = words[i];
            const row = resultTable.insertRow();
            const cell = row.insertCell();
            cell.innerHTML = `<b>${word}</b>`;
            cell.className = "namecell"

            const resultData = data.results[i]
            var currentItem = "";
            var currentChapter = "";
            var anchor;
            var linkCell;

            for (let j = 0; j < resultData.length; j++)
            {
                const itemInfo = resultData[j];
                if (currentChapter != itemInfo[0])
                {
                    if (currentChapter != "")
                    {
                        linkCell.appendChild(anchor);
                    }
                    currentChapter = itemInfo[0]
                    currentItem = itemInfo[2]
                    const row = resultTable.insertRow();
                    linkCell = row.insertCell();
                    anchor = document.createElement("a");
                    anchor.innerHTML = `${currentChapter}<br>${itemInfo[1]}<br>Items: ${currentItem}`;
                    anchor.href = itemInfo[3];
                    anchor.addEventListener("click", loadPDF);
                }
                else
                {
                    if (currentItem != itemInfo[2])
                    {
                        currentItem = itemInfo[2];
                        anchor.innerHTML += `, ${currentItem}`;
                    }
                }
            }
            linkCell.appendChild(anchor);
        }
        await updateTable(1);
    }
    else if (cont == 0)
    {
        const row = resultTable.insertRow();
        const cell = row.insertCell();
        cell.textContent = "Не найдено!";
    }
}

function loadPDF(event)
{
    event.preventDefault();
    var pdfUrl = event.target.href;
    var pdfFrame = document.getElementById("pdfFrame");
    pdfFrame.src = pdfUrl;
}

document.getElementById("input-form").addEventListener("submit", async function(event)
    {
        event.preventDefault();
        document.getElementById("loader").innerHTML = "Поиск...";
        const resultTable = document.getElementById("results");
        resultTable.innerHTML = "";
        const inputField = document.getElementById("search_word");
        await fetch(`/search?search_word=${inputField.value}`);
        document.getElementById("loader").innerHTML = "";
        await updateTable(0);
    });

document.getElementById("search_word").addEventListener("submit", function(event)
    {
        event.preventDefault();
        if (event.keyCode === 13)
        {
            document.getElementById("form-button").click();
        }
    });

