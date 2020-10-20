import UtilsProject as up
import os
from pathlib import Path

def find_and_add_dossiers(db, dict_query):
    start_entry = 0
    newentries = True
    
    while newentries:
        
        xml_return, query = up.get_xml_query(dict_query, start_entry)
        db.add_records(xml_return[2], query)
                
        next_entry = xml_return.find('{http://www.loc.gov/zing/srw/}nextRecordPosition')
        
        if next_entry is None:
            newentries = False
        else:
            start_entry = next_entry.text
            print(start_entry)
        db.commit_db()



def download_files (db, dir_files, downloaded = 'N'):
    to_download = db.show_to_download(downloaded)
    len_todownload = len(to_download)
    
    dir_path = Path(dir_files)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    counter = 0
    for entry in to_download :
        counter += 1
        print(counter, '/', len_todownload, " : ",  entry['identifier'])
        db.downloadFile(entry, dir_path)
    
    print('Finished')