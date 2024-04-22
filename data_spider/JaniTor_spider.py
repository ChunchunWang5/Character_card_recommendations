import json
import os

import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from tqdm import tqdm


def fetch_character_data(base_url, start_page, end_page):
    all_characters = []
    for page in tqdm(range(start_page, end_page)):
        url = f"{base_url}&page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; YourApp/1.0; +http://yourapp.com)',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for character in data.get('data', []):
                # Extract tag names for each character
                character['tag_names'] = [tag["name"] for tag in character.get("tags", [])]
            all_characters.extend(data.get('data', []))
        else:
            print(f"Failed to fetch data for page {page}")
    return all_characters

def get_detials(input_file_path, output_file_path, key):

    with open(input_file_path, 'r', encoding='utf-8') as file:
        characters = json.load(file)

    new_characters = []
    for character in tqdm(characters):
        url = f'https://kim.janitorai.com/characters/{character["id"]}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; YourApp/1.0; +http://yourapp.com)',
            'Accept': 'application/json',
            'Authorization': key   
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            new_characters.append(response.json())
        else:
            print(f'Failed to fetch character with id {character["id"]}')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(new_characters, file, ensure_ascii=False, indent=4)
    print('>>>Get_detials Completed.')


def insert_image(new_file_path, images_dir):

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    with open(new_file_path, 'r', encoding='utf-8') as file:
        new_characters = json.load(file)
    wb = Workbook()
    ws = wb.active
    ws.append(['Image', 'ID', 'Name', "description", "personality", "scenario", "example_dialogs", "first_message", "total_chat", "total_message", "tags"])  # 添加表头

    for character in tqdm(new_characters):
        avatar_url = f"https://pics.janitorai.com/cdn-cgi/image/width=600,quality=70,format=webp/bot-avatars/{character['avatar']}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; YourApp/1.0; +http://yourapp.com)',
            'Accept': 'application/json',
        }
        response = requests.get(avatar_url,headers=headers)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            image_extension = 'jpg' if 'jpeg' in content_type else 'png'  
            image_path = os.path.join(images_dir, f"{character['id']}.{image_extension}")
            with open(image_path, 'wb') as f:
                f.write(response.content)
            row = ['', character['id'], character['name'], character['description'], character['personality'], character["scenario"], character["example_dialogs"], character["first_message"], character["total_chat"], character["total_message"], ", ".join(char["name"] for char in character["tags"])]
            ws.append(row)
            img = Image(image_path)
            ws.add_image(img, f'A{ws._current_row}') 
        else:
            print(f"Failed to download image for character {character['id']}")

    excel_file_path = 'characters_with_images.xlsx'
    wb.save(excel_file_path)
    print('>>>Excel file with images has been created.')


def main():
    start = int(input("请输入起始页码："))
    end = start + 5
    key = str(input("请输入动态的key:"))

    base_url = "https://kim.janitorai.com/characters?sort=popular&mode=sfw"
    characters = fetch_character_data(base_url, start, end) 
    json_file_name = "characters_data_{}-{}.json".format(start, end-1)
    with open(json_file_name, 'w') as f:
        json.dump(characters, f, ensure_ascii=False, indent=4)

    df = pd.DataFrame(characters)
    excel_file_name = "characters_data_{}-{}.xlsx".format(start, end-1)
    df.to_excel(excel_file_name, index=False)

    out_file_name = "characters_data_with_detials_{}-{}.json".format(start, end-1)
    get_detials(json_file_name, out_file_name, key)
    
    image_path = "download_images_{}-{}".format(start, end-1)
    insert_image(out_file_name, image_path)


if __name__ == "__main__":
    main()