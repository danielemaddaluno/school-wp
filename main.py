import os
import zipfile
import requests
from tqdm import tqdm

def create_databases(num_sites):
    import mysql.connector
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        port=8002
    )
    cursor = connection.cursor()
    for i in range(1, num_sites + 1):
        db_name = f"site{i}"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database {db_name} created.")
    cursor.close()
    connection.close()

def download_file(url, destination, description):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(destination, "wb") as file, tqdm(
        desc=description,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def extract_zip(source, destination):
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(destination)

def unzip_and_prepare(source_path):
    extracted_folders = []
    for file in os.listdir(source_path):
        if file.endswith(".zip"):
            file_path = os.path.join(source_path, file)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(source_path)

    for item in os.listdir(source_path):
        item_path = os.path.join(source_path, item)
        if os.path.isdir(item_path):
            extracted_folders.append(item_path)

    return extracted_folders

def remove_extracted_folders(folders):
    for folder in folders:
        if os.path.isdir(folder):
            os.system(f"rm -rf {folder}")

def setup_sites(num_sites, wordpress_source, htdocs_path, plugins_list, themes_list):
    wordpress_folder = os.path.join(wordpress_source, "wordpress")
    for i in range(1, num_sites + 1):
        site_folder = os.path.join(htdocs_path, f"site{i}")
        os.makedirs(site_folder, exist_ok=True)

        # Copy WordPress files
        for item in os.listdir(wordpress_folder):
            s = os.path.join(wordpress_folder, item)
            d = os.path.join(site_folder, item)
            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
                os.system(f"cp -r {s}/* {d}")
            else:
                os.system(f"cp {s} {d}")

        # Configure wp-config.php
        config_file = os.path.join(site_folder, "wp-config-sample.php")
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config_content = file.read()

            config_content = config_content.replace("localhost", "db")
            config_content = config_content.replace("username_here", "root")
            config_content = config_content.replace("password_here", "password")
            config_content = config_content.replace("database_name_here", f"site{i}")

            with open(config_file, "w") as file:
                file.write(config_content)

            os.rename(config_file, os.path.join(site_folder, "wp-config.php"))

            # Copy plugins and themes
            plugins_target = os.path.join(site_folder, "wp-content", "plugins")
            os.makedirs(plugins_target, exist_ok=True)
            for plugin in plugins_list:
                os.system(f"cp -r {plugin} {plugins_target}")

            themes_target = os.path.join(site_folder, "wp-content", "themes")
            os.makedirs(themes_target, exist_ok=True)
            for theme in themes_list:
                os.system(f"cp -r {theme} {themes_target}")

if __name__ == "__main__":
    num_sites = int(input("Enter the number of WordPress sites to create: "))

    # Step 1: Create databases
    create_databases(num_sites)

    # Step 2: Download WordPress
    wordpress_zip = "wordpress.zip"
    download_file("https://wordpress.org/latest.zip", wordpress_zip, "Downloading WordPress")

    # Step 3: Extract WordPress
    extract_path = "wordpress_temp"
    os.makedirs(extract_path, exist_ok=True)
    extract_zip(wordpress_zip, extract_path)

    # Step 4: Handle plugins and themes
    plugins_source = "wp-content/plugins"
    themes_source = "wp-content/themes"

    plugins_list = unzip_and_prepare(plugins_source)
    themes_list = unzip_and_prepare(themes_source)

    # Step 5: Setup sites
    htdocs_path = "htdocs"
    os.makedirs(htdocs_path, exist_ok=True)
    setup_sites(num_sites, extract_path, htdocs_path, plugins_list, themes_list)

    # Cleanup
    remove_extracted_folders(plugins_list)
    remove_extracted_folders(themes_list)
    os.remove(wordpress_zip)
    os.system(f"rm -rf {extract_path}")

    print("All WordPress sites set up successfully.")
