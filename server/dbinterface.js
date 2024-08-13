dbn = "vehicles.db"

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database(dbn, sqlite3.OPEN_READWRITE, (err) => {
        if (err) return console.error(err.message)
});


function execQuery(query, params){
    db.run(query, params, (err) => {
        if (err) return console.error(err.message);
    })
}

function getRows(query, params) {
    return new Promise((resolve, reject) => {
        db.all(query, params, (err, rows) => {
            if (err) {
                reject(err);
            } else {
                resolve(rows);
            }
        });
    });
}

/*
getRows("SELECT * FROM history", [])
    .then(rows => {
        rows.forEach(row => {
            const jsonString = JSON.stringify(row);
            console.log(jsonString + "\n");
    })})
    .catch(err => {
        console.error('Error:', err);
    });

*/

module.exports = { execQuery, getRows };
