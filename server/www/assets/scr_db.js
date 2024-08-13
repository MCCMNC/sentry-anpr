function fetchCreateShit(id, url) {

    const targetElement = document.getElementById(id);

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response err');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.length > 0) {
            createTable(id, data);
        } else {
            targetElement.textContent = 'No rows';
        }
    })
    .catch(error => {
        console.error('Fetch err:', error);
    });
}

function createTable(id, data) {
    const targetElement = document.getElementById(id);
    const table = document.createElement('table');
    table.id = "content_table";
    const headerRow = table.createTHead().insertRow();

    const headers = Object.keys(data[0]);

    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText.toUpperCase();
        headerRow.appendChild(th);
    });

    
    const tbody = table.createTBody();

    data.forEach((rowData, row_index) => {
        const row = tbody.insertRow();
        Object.keys(rowData).forEach((key, index) => {
            const cell = row.insertCell();
            if ((index === Object.keys(rowData).length - 1) && id != "timetable") {
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'DELETE';
                deleteButton.classList.add('delete-button');
                deleteButton.id = row_index
                if(id == "history" && rowData[key] != null){
                    cell.innerHTML = `<a href="/view/${rowData[key]}">${rowData[key]}</a>`
                }else{
                    cell.textContent = rowData[key];
                }
                cell.append(deleteButton)
            } else cell.textContent = rowData[key];
        });
    });

    document.getElementById(id).innerHTML = ""
    targetElement.appendChild(table);
}

document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById(`${tableid}`);

    table.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-button')) {

        const row = event.target.closest('tr');
        const firstCellText = row.cells[0].textContent;

        var ans = window.confirm(`DELETE ENTRY '${firstCellText}' ?`)
        if (ans){ deleteEntry(dbname, firstCellText); location.reload() }
            else console.log("cancelled")
        }
    });
});

function deleteEntry(db, val){
    fetch(`/delete_entry/${db}/value/${val}`, {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    })
    .catch(error => {
        console.error('Form submission error:', error);
    });
}