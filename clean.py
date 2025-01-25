import os
import mysql.connector

def delete_site_folders(htdocs_path):
    for folder in os.listdir(htdocs_path):
        folder_path = os.path.join(htdocs_path, folder)
        if folder.startswith("site") and os.path.isdir(folder_path):
            os.system(f"rm -rf {folder_path}")
            print(f"Deleted folder: {folder_path}")

def delete_site_databases():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        port=8002
    )
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()

    for (db_name,) in databases:
        if db_name.startswith("site"):
            cursor.execute(f"DROP DATABASE {db_name};")
            print(f"Deleted database: {db_name}")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    htdocs_path = "htdocs"

    # Step 1: Delete all site folders
    delete_site_folders(htdocs_path)

    # Step 2: Delete all site databases
    delete_site_databases()

    print("All site folders and databases have been deleted.")
