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

def setup_sites(num_sites, wordpress_source, htdocs_path, plugin_source):
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

#             SNIPPET = """<?php
# define('.COOKIE_DOMAIN.', 'REPLACEME1');
# define('.SITECOOKIEPATH.', '.');
# if(isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
#         $list = explode(',',$_SERVER['HTTP_X_FORWARDED_FOR']);
#         $_SERVER['REMOTE_ADDR'] = $list[0];
# }
# define( 'WP_HOME', 'https://REPLACEME2' );
# define( 'WP_SITEURL', 'https://REPLACEME2' );
# $_SERVER['HTTP_HOST'] = 'REPLACEME1';
# $_SERVER['REMOTE_ADDR'] = 'https://REPLACEME1';
# $_SERVER[ 'SERVER_ADDR' ] = 'REPLACEME1';
# """
#             SNIPPET = SNIPPET.replace("REPLACEME1", "eb9a-2a01-e11-200f-d80-4d46-c120-b1d2-3efa.ngrok-free.app")
#             SNIPPET = SNIPPET.replace("REPLACEME2", f"eb9a-2a01-e11-200f-d80-4d46-c120-b1d2-3efa.ngrok-free.app/site{i}")
#
#            config_content = config_content.replace("<?php", SNIPPET)
            config_content = config_content.replace("localhost", "db")
            config_content = config_content.replace("username_here", "root")
            config_content = config_content.replace("password_here", "password")
            config_content = config_content.replace("database_name_here", f"site{i}")

            # Add plugin activation snippet
            plugin_activation = "\n// Activate plugins\ndefine('WP_AUTO_UPDATE_CORE', false);\nif (file_exists(ABSPATH . 'wp-admin/includes/plugin.php')) {\n    include_once(ABSPATH . 'wp-admin/includes/plugin.php');\n    activate_plugin('relative-url/relative-url.php');\n}\n"
            config_content += plugin_activation

            with open(config_file, "w") as file:
                file.write(config_content)

            os.rename(config_file, os.path.join(site_folder, "wp-config.php"))

        # Install the plugin
        plugin_dest = os.path.join(site_folder, "wp-content", "plugins")
        os.makedirs(plugin_dest, exist_ok=True)
        os.system(f"cp -r {plugin_source}/* {plugin_dest}")

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

    # Step 4: Download the plugin
    plugin_zip = "relative-url.zip"
    download_file("https://downloads.wordpress.org/plugin/relative-url.0.1.8.zip", plugin_zip, "Downloading Plugin")

    # Step 5: Extract the plugin
    plugin_extract_path = "plugin_temp"
    os.makedirs(plugin_extract_path, exist_ok=True)
    extract_zip(plugin_zip, plugin_extract_path)

    # Step 6: Setup sites
    htdocs_path = "htdocs"
    os.makedirs(htdocs_path, exist_ok=True)
    setup_sites(num_sites, extract_path, htdocs_path, plugin_extract_path)

    # Cleanup
    os.remove(wordpress_zip)
    os.remove(plugin_zip)
    os.system(f"rm -rf {extract_path}")
    os.system(f"rm -rf {plugin_extract_path}")

    print("All WordPress sites set up successfully.")
