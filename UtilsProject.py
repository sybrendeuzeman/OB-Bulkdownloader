import Models as m
import Utilities as u
from pathlib import Path
import tkinter.filedialog as fd
import xml.etree.ElementTree as ET
import re
import pysftp


###########################
### Database Connection ###
###########################

class DatabaseDocuments:
    # Initialize database
    def __init__(self, database = None):
        if database is None:
            database = fd.askopenfilename(filetypes = [('Database-file', '*.db')])

        # Setup connection and tables (if necessary)
        m.Schema(database = database)

        # Connect to database
        self.db = m.DocumentModel(database = database)

    # Command to commit the database
    def commit_db(self):
        self.db.commit_database()

    # Management of record adding
    def add_record(self, list_entry):
        exist = self.db.exist_document([list_entry[1]])
        if (not exist):
            self.db.add_document(list_entry)

    def add_keyword(self, list_entry, query):
        exist = self.db.exist_keyword(list_entry[1], query)
        if (not exist):
            self.db.add_keyword(list_entry[1], query)

    def add_records(self, data, query):
        data_in =list(map(find_variables, data) ) 
        for list_entry in data_in:
            self.add_record(list_entry)
            self.add_keyword(list_entry, query)

    # Manage download indicators
    def set_downloaded(self, identifier, YF):
        self.db.set_downloaded(identifier, YF)

    # Show data in database
    def show_all(self):
        result = self.db.select_all()
        return [dict(row) for row in result.fetchall()]

    def show_keyword(self, keyword):
        result = self.db.select_keyword(keyword)
        return [dict(row) for row in result.fetchall()]

    def show_to_download(self, downloaded):
        result = self.db.select_to_download(downloaded)
        return [dict(row) for row in result.fetchall()]


    # Escape to query the database (for special operations)
    def execute_query(self, query):
        result = self.db.execute_query(query)
        try:
            return [dict(row) for row in result.fetchall()]
        except:
            print('No table returned from query')
    
    # Download files to the system
    def downloadFile (self, db_entry, dir_local):
        # Get important information
        locationURI = db_entry['locationURI']
        identifier = db_entry['identifier']
        
        # Remove some redundant information from locationURI
        actual_url = Path(re.sub('ftps://bestanden.officielebekendmakingen.nl/', '', locationURI))

        # Filename
        filename = identifier + ".pdf"

        # Make URLs to document of interest.
        stuk_url = actual_url / filename           
        print(stuk_url)
        
        # Set location
        # Removing protection against man-in-the-middle attacks :(
        host = "bestanden.officielebekendmakingen.nl"
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
            

        try:
            with pysftp.Connection(host, username = 'anonymous', password = 'anonymous', cnopts=cnopts) as sftp:
                file_local = dir_local / filename
                print(file_local)
                sftp.get(str(stuk_url), str(dir_local / filename))
            self.set_downloaded(db_entry['identifier'], 'Y')
        except:
            self.set_downloaded(db_entry['identifier'], 'F')
            print("Fail")
            
        self.commit_db()


###############
# Parsing XML #
###############

def find_variables(record):
    def find_owmskern (record, element):
        return record[2][0][0][0][0].find('{http://purl.org/dc/terms/}' + element).text
    
    def find_owmsmantel (record, element):
        return record[2][0][0][0][1].find('{http://purl.org/dc/terms/}' + element).text
    
    def find_opmeta (record, element):
        return record[2][0][0][0][2].find('{http://standaarden.overheid.nl/product/terms/}' + element).text
    
    def find_enrichedData(record, element):
        return record[2][0][1].find('{http://standaarden.overheid.nl/sru}' + element).text

    title = find_owmskern(record, 'title')
    identifier = find_owmskern(record, 'identifier')
    type_doc = find_owmskern(record, 'type')
    creator = find_owmskern(record, 'creator')
    date = find_owmsmantel(record, 'date')
    subrubriek = find_opmeta(record, 'subrubriek')
    dossier = find_opmeta(record, 'dossiernummer')
    ondernummer = find_opmeta(record, 'ondernummer')
    vergaderjaar = find_opmeta(record, 'vergaderjaar')
    locationURI = find_enrichedData(record, 'locationURI')
    url = find_enrichedData(record, 'url')
    
    return_list = [
        title,
        identifier,
        type_doc,
        creator,
        date,
        subrubriek,
        dossier,
        ondernummer,
        vergaderjaar,
        locationURI,
        url
    ]

    return return_list

###############
# Getting XML #
###############

def get_xml_query (dict_query, startRecord):
    url, query = make_url(dict_query, startRecord)
    return u.getxml(url), query

def make_url (dict_query, startRecord):
    # Make the query
    query = make_query(dict_query)
    
    # Make query parts
    url_start = "https://zoek.officielebekendmakingen.nl/sru/Search?version=1.2&operation=searchRetrieve&x-connection=cvdr"
    url_maxrecords = "&maximumRecords=100"
    url_startrecord = "&startRecord=" + str(startRecord) 
    url_query = '&query=' + query
    
    # Combine query
    url = url_start + url_startrecord + url_maxrecords + url_query
    
    return url, query

def make_query (dict_query):
    start_and = True
    for key, values in dict_query.items():
        if start_and == True:
            query = '(' 
            start_and = False
        else:
            query = query + 'AND(' 

        start_or = True
        for value in values:
            # Only at start, the query should not start with an 'AND'
            if start_or == True:
                query = query + '(' + key + ' = "' + value + '")' 
                start_or = False
            else:
                query = query + 'OR' +  '(' + key + ' = "' + value + '" )' 
        query = query + ')'
    return query

