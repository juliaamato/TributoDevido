import sqlite3

def connect(): 
    return sqlite3.connect('desafiotributodevido.db')

def disconnect(conn): 
    conn.close()

def set_cursor(conn):
    return conn.cursor()

def create_table(conn):
    cursor = set_cursor(conn)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment TEXT,
            payment_method TEXT,
            contract TEXT,
            experience TEXT,
            project TEXT,
            work TEXT,
            description TEXT,
            tags TEXT
        )
    ''')
    conn.commit()

def insert(conn, data):
    create_table(conn)
    cursor = set_cursor(conn)
    tags_string = ', '.join(data['tags']) if data['tags'] else None
    cursor.execute('''
        INSERT INTO oportunities (payment, payment_method, contract, experience, project, work, description, tags) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['payment'], 
        data['payment_method'], 
        data['contract'], 
        data['experience'], 
        data['project'], 
        data['work'], 
        data['description'], 
        tags_string
    ))
    conn.commit()

def select(conn):
    cursor = set_cursor(conn)
    cursor.execute('''
        DELETE FROM oportunities
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM oportunities
            GROUP BY payment, payment_method, contract, experience, project, work, description, tags
        )
    ''')
    conn.commit()
    cursor.execute("SELECT * FROM oportunities")
    return cursor.fetchall()

def init():
    conn = connect()
    create_table(conn)
    return conn

if __name__ == "__main__":
    conn = init()
    
    print (select(conn))
    disconnect(conn)
