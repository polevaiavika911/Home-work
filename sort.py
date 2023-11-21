import os
import shutil
import sys
from pathlib import Path

def create_directories(folder_path, categories):
        for category in categories:
             category_path = os.path.join(folder_path, category)
             os.makedirs(category_path, exist_ok=True)


def normalize(name):   # всі файли та папки перейменовуються за допомогою функції normalize.
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh',
        'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    base_name, file_extension = os.path.splitext(name)

    transliterated_name = ''.join(transliteration_dict.get(char, char) for char in base_name)
    normalize_name = ''.join('_' if not char.isalnum() else char for char in transliterated_name)

    return f"{normalize_name}{file_extension}"

def move_file(source_filepath, destination_folder):
    _, filename = os.path.split(source_filepath)
    destination_path = os.path.join(destination_folder, normalize(filename))
    shutil.move(source_filepath, destination_path)

    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension in {'.jpeg', '.png', '.jpg', '.svg'}:
        category = 'images'
    elif file_extension in {'.avi', '.mp4', '.mov', '.mkv'}:
        category = 'video'
    elif file_extension in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
        category = 'documents'
    elif file_extension in {'.mp3', '.ogg', '.wav', '.amr'}:
        category = 'audio'
    elif file_extension in {'.zip', '.gz', '.tar'}:
        category = 'archives'
    else:
        category = 'other'

    files_by_category[category].append(destination_path)

    if category == 'other':
        unknown_extensions.add(file_extension)
    else:
        known_extensions.add(file_extension)
    

def sort_folders(folder_path):
    categories = ["images", "video", "documents", "audio", "archives", "other"]
    create_directories(folder_path, categories)

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            source_filepath = os.path.join(dirpath, filename)

            normalized_name = normalize(filename)
            file_extension = os.path.splitext(filename)[1].lower()
           

            if file_extension in {'.jpeg', '.png', '.jpg', '.svg'}:
                move_file(source_filepath, os.path.join(folder_path, 'images'))
            elif file_extension in {'.avi', '.mp4', '.mov', '.mkv'}:
                move_file(source_filepath, os.path.join(folder_path, 'video'))
            elif file_extension in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
                move_file(source_filepath, os.path.join(folder_path, 'documents'))
            elif file_extension in {'.mp3', '.ogg', '.wav', '.amr'}:
                move_file(source_filepath, os.path.join(folder_path, 'audio'))
            elif file_extension in {'.zip', '.gz', '.tar'}:
                move_file(source_filepath, os.path.join(folder_path, 'archives'))
            else:
                move_file(source_filepath, os.path.join(folder_path, 'other'))

            if file_extension == 'other':
                unknown_extensions.add(file_extension)
            else:
                known_extensions.add(file_extension)
        

    for category, files in files_by_category.items():
        print(f"Files in {category}:")
        for file_path in files:
            print(f"- {file_path}")

    print("\nKnown extensions:")
    for ext in known_extensions:
        print(f"- {ext}")

    print("\nUnknown extensions:")
    for ext in unknown_extensions:
        print(f"- {ext}")

    for dirpath, dirnames, filenames in os.walk(folder_path, topdown=False):
        for dirname in dirnames:
            current_dir = os.path.join(dirpath, dirname)
            if not os.listdir(current_dir):
                os.rmdir(current_dir)

known_extensions = set()
unknown_extensions = set()

files_by_category = {
    'images': [],
    'video': [],
    'documents': [],
    'audio': [],
    'archives': [],
    'other': []
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_to_sort = sys.argv[1]

    if not os.path.isdir(folder_to_sort):
        print(f"{folder_to_sort} is not a directory.")
        sys.exit(1)

    sort_folders(folder_to_sort)
