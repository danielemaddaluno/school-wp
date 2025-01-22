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

def download_wordpress(destination):
    url = "https://wordpress.org/latest.zip"
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(destination, "wb") as file, tqdm(
        desc="Downloading WordPress",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def extract_wordpress(source, destination):
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(destination)

def setup_sites(num_sites, wordpress_source, htdocs_path):
    wordpress_folder = os.path.join(wordpress_source, "wordpress")
    for i in range(1, num_sites + 1):
        site_folder = os.path.join(htdocs_path, f"site{i}")
        os.makedirs(site_folder, exist_ok=True)

        for item in os.listdir(wordpress_folder):
            s = os.path.join(wordpress_folder, item)
            d = os.path.join(site_folder, item)
            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
                os.system(f"cp -r {s}/* {d}")
            else:
                os.system(f"cp {s} {d}")

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

if __name__ == "__main__":
    num_sites = int(input("Enter the number of WordPress sites to create: "))

    # Step 1: Create databases
    create_databases(num_sites)

    # Step 2: Download WordPress
    wordpress_zip = "wordpress.zip"
    download_wordpress(wordpress_zip)

    # Step 3: Extract WordPress
    extract_path = "wordpress_temp"
    os.makedirs(extract_path, exist_ok=True)
    extract_wordpress(wordpress_zip, extract_path)

    # Step 4: Setup sites
    htdocs_path = "htdocs"
    os.makedirs(htdocs_path, exist_ok=True)
    setup_sites(num_sites, extract_path, htdocs_path)

    # Cleanup
    os.remove(wordpress_zip)
    os.system(f"rm -rf {extract_path}")

    print("All WordPress sites set up successfully.")
