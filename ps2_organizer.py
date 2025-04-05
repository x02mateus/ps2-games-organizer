import pycdlib
import csv
import os

# database (PS2.data.tsv)
db_path = os.path.join(os.getcwd(), 'PS2.data.tsv')
db = {}

# gamedata
game_name = ''
game_id = ''
game_region = ''

# regions list
regions = ['SCPS', 'SCPM', 'SLPS', 'SLPM', 'SCUS', 'SLUS', 'SCES', 'SCED', 'SLES', 'SLED', 'PAPX', 'PBPX', 'PCPX']

def read_db():
    with open(db_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            db[row['ID']] = {'title': row['title'], 'region': row['region']}

def search_for_isos():
    found_isos = []
    for i in os.listdir(os.getcwd()):
        if i.endswith('.iso'):
            found_isos.append(i)
    
    return found_isos

def open_iso():
    iso_file = pycdlib.PyCdlib()
    iso_file.open(i)
    format_iso(iso_file, i)

def format_gameid(string):
    # replace characters and remove suffix
    formatted = string.replace('.', '')
    formatted = formatted.replace('_', '-')
    formatted = formatted.split(';')[0]
    return formatted

def format_iso(iso_file, iso_name):
    for child in iso_file.list_children(iso_path='/'):
        child_name = child.file_identifier().decode('utf-8')
        if any(region in child_name for region in regions):
            game_id = format_gameid(child_name)

            if game_id in db:
                game_name = db[game_id]['title']
                game_region = db[game_id]['region']
                print(f"Game ID: {game_id}")
                print(f"Game Name: {game_name}")
                print(f"Game Region: {game_region}")

                # close ISO before renaming it
                iso_file.close()

                # rename ISO
                new_iso_name = f"[{game_id}] {game_name} ({game_region}).iso"
                new_iso_name = new_iso_name.replace(':', '')  # remove invalid characters
                current_path = os.path.join(os.getcwd(), iso_name)
                new_path = os.path.join(os.getcwd(), new_iso_name)

                try:
                    os.rename(current_path, new_path)
                    print(f"file renamed to: {new_iso_name}")
                except Exception as e:
                    print(f"error renaming the file: {e}")
            else:
                print(f"game ID {game_id} not found on database.")

if not os.path.exists(db_path):
    print("ps2 games database file is missing. database file: 'PS2.data.tsv'")
    exit()
else:
    read_db()

isos = search_for_isos()
print('found isos!')
for i in isos:
    print(i)
    open_iso() # now the script do everything automatically