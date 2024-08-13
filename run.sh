#!/bin/bash

DB_FILE="vehicles.db"

if [ ! -f "$DB_FILE" ]; then
    echo "Creating database..."
    touch "$DB_FILE"
fi

echo "Checking database..."

SQL_COMMANDS="
CREATE TABLE IF NOT EXISTS whitelist(
    regnum TEXT PRIMARY KEY,
    owner TEXT,
    msisdn TEXT,
    date_added DATETIME
);

CREATE TABLE IF NOT EXISTS history(
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    regnum TEXT NOT NULL,
    passing_date DATETIME,
    sysmode TEXT,
    FOREIGN KEY (regnum) REFERENCES whitelist(regnum)
);
"

echo "$SQL_COMMANDS" | sqlite3 $DB_FILE

echo "Starting node server..."
node server/server.js &
sleep 6
echo "Starting ANPR..."
/bin/python live_detection.py &

wait