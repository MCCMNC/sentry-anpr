import sqlite3

create_whitelist = """CREATE TABLE IF NOT EXISTS whitelist(
    regnum TEXT PRIMARY KEY,
    owner TEXT,
    msisdn TEXT,
    date_added DATETIME
);"""

create_history = """CREATE TABLE IF NOT EXISTS history(
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    regnum TEXT NOT NULL,
    passing_date DATETIME,
    sysmode TEXT,

    FOREIGN KEY (regnum) REFERENCES whitelist(regnum)
);"""

class DBInterface:
    _instance = None

    def __new__(cls, db_name="vehicles.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_name = db_name
            cls._instance.con = cls._instance.connect()
        return cls._instance
    
    
    def connect(self):
        try:
            con = sqlite3.connect(self.db_name)
            return con
        except sqlite3.Error as e:
            print("[SQLError]", e)
            return -1

    def exec_query(self, query, params=None):
        try:
            cur = self.con.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            self.con.commit()
            return 0
        except sqlite3.Error as e:
            print("[SQLError]", e)


    def insert(self, table, columns, values):
        try:
            cur = self.con.cursor()
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            cur.execute(query, values)
            self.con.commit()
            return 0

        except sqlite3.Error as e:
            print("[SQLError]", e)
            return -1

    def select(self, query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
            res = cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("[SQLError]", e)
            return -1