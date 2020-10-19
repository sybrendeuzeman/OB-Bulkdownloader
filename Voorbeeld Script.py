import UtilsProject as up
import wrappers as w

# Configure to right "metadata-database"
db = up.DatabaseDocuments("voorbeeld.db")

# Geef de keywords op waar naar gezocht moet worden
keywords = [
    'dodo',
    'mammoet',
    'tijger'
]

# Geef vervaardigers van de documenten op
creators = [
    'Tweede Kamer',
    'Eerste Kamer'
]

# Zoek naar keywords en vervaardigers binnen handelingen
for keyword in keywords:
    for creator in creators:
        dict_query = {
            'keyword' : keyword,
            'creator' : creator,
            'type' : 'handeling'
        }
        w.find_and_add_dossiers(db, keyword, dict_query)       

# Download de geselecteerde files
w.download_files(db, 'C:/Werk/TK/Voorbeeld')

