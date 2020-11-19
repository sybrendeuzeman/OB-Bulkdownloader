import UtilsProject as up
import wrappers as w
import pandas as pd

# Configure to right "metadata-database"
db = up.DatabaseDocuments('../voorbeeld.db')

# Geef de keywords op waar naar gezocht moet worden
keywords = [
    'dodo',
    'mammoet'
]

# Geef vervaardigers van de documenten op
creators = [
    'Tweede Kamer',
    'Eerste Kamer',
    'Verenigde Vergadering'
]

# Zoek naar keywords en vervaardigers binnen het type handelingen
dict_query = {
    'keyword' : keywords,
    'creator' : creators,
    'type' : ['handeling', 'kamerstuk']
}

query = up.make_query(dict_query)
print(query)
w.find_and_add_dossiers(db, query)       

# Download de geselecteerde files
print("Te downloaden documenten:", len(db.show_to_download('N')))
w.download_files(db, '../Voorbeeld')

# Voor XML gebruik je de volgende code
#w.download_files(db, '../Voorbeeld', extension = 'xml')

pd.DataFrame(db.show_all()).to_excel('../overzicht_stukken.xlsx')