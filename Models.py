import sqlite3

class Schema:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row
        self.create_document_table()
        self.create_keyword_table()
        self.conn.commit()
    
    def create_document_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "documenten" (
            id INTEGER PRIMARY KEY,
            title TEXT,
            identifier TEXT,
            type TEXT,
            creator TEXT,
            date TEXT,
            subrubriek TEXT,
            dossiernummer TEXT,
            ondernummer TEXT,
            vergaderjaar TEXT,
            locationURI TEXT,
            url TEXT,
            downloaded TEXT default 'N',
            date_added TEXT default (date('now'))
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def create_keyword_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "keyword" (
            id INTEGER PRIMARY KEY,
            identifier TEXT,
            keyword TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

class DocumentModel:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row
    
    def add_documents(self, data):
        self.conn.executemany(
        """
        INSERT INTO documenten
        (
            title,
            identifier,
            type,
            creator,
            date,
            subrubriek,
            dossiernummer,
            ondernummer,
            vergaderjaar,
            locationURI,
            url,
            date_added
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ? ?, ?)
        """,
        data)

    def select_all(self):
        return self.conn.execute(
        """
        SELECT *
        FROM documenten
        """
        )

    def select_to_download(self, downloaded):
        return self.conn.execute(
            """
            SELECT *
            FROM documenten
            WHERE 
                downloaded = ?
            """,
            [downloaded]
        )

    def select_keyword(self, keyword):
        return self.conn.execute(
            """
            SELECT 
                *
            FROM keyword
            INNER JOIN documenten ON keyword.identifier = documenten.identifier
            WHERE keyword = ?
            """,
            [keyword]
        )

    def add_document(self, data):
        self.conn.execute(
        """
        INSERT INTO documenten
        (
            title,
            identifier,
            type,
            creator,
            date,
            subrubriek,
            dossiernummer,
            ondernummer,
            vergaderjaar,
            locationURI,
            url
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data)
        
    def add_keyword(self, identifier, keyword):
        self.conn.execute(
        """
        INSERT INTO keyword
        (
            identifier,
            keyword
        )
        values (?, ?)
        """,
        [keyword, identifier])

    def exist_document(self, identifier):
        result = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM documenten
            WHERE identifier = ?
            """,
            identifier
        )
        
        count = dict(result.fetchone())['COUNT(*)']
        if (count == 0):
            return False
        elif (count > 0):
            return True

    def exist_keyword(self, identifier, keyword):
        result = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM keyword
            WHERE 
                identifier = ? 
                AND keyword = ?
            """,
            [identifier, keyword]
        )
        
        count = dict(result.fetchone())['COUNT(*)']
        if (count == 0):
            return False
        elif (count > 0):
            return True

    def set_downloaded(self, identifier, YF):
        query ="""
        UPDATE documenten
        SET
            downloaded = ?
        WHERE
            identifier == ?
        """
        self.conn.execute(
            query,
            [YF, identifier]
        )

    def set_downloaded_failed(self, identifier):
        query ="""
        UPDATE documenten
        SET
            downloaded = 'F'
        WHERE
            identifier == ?
        """
        self.conn.execute(
            query,
            [identifier]
        )

    def commit_database(self):
        self.conn.commit()

    def execute_query(self, query):
        return self.conn.execute(query)