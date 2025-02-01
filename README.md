
# school-wp
School WordPress Playground is a Docker-based project that sets up multiple isolated WordPress instances for educational purposes.<br>
It automatically creates site directories and databases (site1, site2, etc.), providing an overview of their status via a centralized dashboard.<br>
The dashboard checks database connectivity and detects whether WordPress has been initialized in each instance.

## Fast configuration:
Add the zip required as installed themes and plugins (installed but not activated) inside of the specific folder that you'll find under `./wp-content`.

```
.
├── LICENSE                  ------> Specifies the terms under which the project can be used or modified.
├── README.md                ------> Provides detailed documentation and instructions for the project setup.
├── clean.py                 ------> A script for cleaning up temporary or unneeded files/folders in the project.
├── docker-compose.yml       ------> Defines and configures the Docker services (web, db, phpmyadmin) for the project.
├── htdocs                   ------> The folder containing web-accessible files for the WordPress sites.
│   ├── favicon.ico          ------> A small icon displayed in the browser tab for the site.
│   ├── index.php            ------> A basic PHP entry point file for the site.
│   └── phpinfo.php          ------> A PHP script displaying server and PHP configuration details.
├── main.py                  ------> The main Python script for automating WordPress setup and database configuration.
├── mysql_data               ------> Stores the MariaDB database data persistently for the project.
├── requirements.txt         ------> Lists Python dependencies needed to run the scripts in the project.
└── wp-content               ------> Directory for WordPress content such as plugins and themes.
    ├── plugins              ------> Stores WordPress plugins to extend site functionality.
    └── themes               ------> Stores WordPress themes to define the visual appearance of the site.
```

Then simply execute in order the following commands:
```
docker compose up           ------> Starts all services defined in docker-compose.yml for the project.
python3 main.py             ------> You need to pip install requirements.py first (I suggest to run it throught PyCharm)
```


Read below for a complete comment on each command.

### 1. Docker Compose 
```
docker compose up
```

This is a Docker Compose configuration that sets up a simple environment with three services:
1) *web*: An Apache server running PHP 8.2 using the `webdevops/php-apache:8.2-alpine` image. It maps port `8000` on the host to port `80` inside the container and serves PHP pages from the local htdocs folder.

2) *db*: A `MariaDB database` (version 10.5), which persists data in the local mysql_data folder. It restarts automatically and exposes port `3306` on the host as port `8002` inside the container. The `root` password is set to `password`.

3) *phpmyadmin*: A PhpMyAdmin service that provides a web interface to manage the MariaDB database. It depends on the db service and exposes port `80` inside the container to port `8001` on the host. It connects to the database using the `root` password `password`.

This setup allows you to run a PHP web application with a MariaDB backend, easily accessible and manageable via PhpMyAdmin.

### 2. Db and htdocs configurations
```
python3 main.py
```
This Python script automates the setup of multiple WordPress sites, performing the following steps:

#### 1. User Input
   - The script prompts the user for the number of WordPress sites to create (`num_sites`).

#### 2. Database Creation
   - It creates `num_sites` databases under MariaDB, naming them sequentially as `site1`, `site2`, `site3`, etc.

#### 3. Download WordPress
   - The script downloads the latest WordPress version from [WordPress.org](https://wordpress.org/latest.zip).
   - It displays a progress bar while downloading the file.

#### 4. Unzip WordPress
   - After downloading, the script unzips the WordPress archive and extracts the `wordpress` folder.

#### 5. Copy WordPress Files
   - It copies the contents of the `wordpress` folder `num_sites` times, creating a separate directory for each site under `/htdocs/site1`, `/htdocs/site2`, `/htdocs/site3`, etc.

#### 6. Modify Configuration
   - In each folder, the script modifies the `wp-config-sample.php` file by replacing:
     - `username_here` with `"root"`
     - `password_here` with `"password"`
     - `database_name_here` with the corresponding folder name (e.g., `site1`, `site2`, etc.).

#### 7. Rename Configuration
   - The script renames the modified `wp-config-sample.php` file to `wp-config.php` after making the necessary changes.

#### 8. Auto Plugins
   - The script automatically copies any specified plugins (in ZIP format) into each site's `wp-content/plugins` directory.
     - Example plugin ZIP files to be copied:
       - `example-plugin.zip`
       - `another-plugin.zip`

#### 9. Auto Themes
   - The script automatically copies any specified themes (in ZIP format) into each site's `wp-content/themes` directory.
     - Example theme ZIP files to be copied:
       - `example-theme.zip`
       - `another-theme.zip`

---

This script sets up multiple WordPress sites, configures them with their respective databases, and modifies their configuration files accordingly.

### 3. Port Forwarding
To make your WordPress sites accessible externally, configure your router to forward port `xyzw` to the local PC running the Docker container. 

#### Steps:
1. Log in to your router's administration panel.
2. Locate the "Port Forwarding" section (this may vary depending on the router).
3. Create a new port forwarding rule:
    - Internal IP: The IP address of the PC running the container
    - Internal Port: `8000`
    - External Port: `xyzw`
4. Save the rule.

After setting up port forwarding, you can access your WordPress sites using your public IP address or domain, appending `:xyzw` to the URL.

Example:
```
http://<your-public-ip>:xyzw
```


### 4. Clean

The `clean.py` script is used to remove all the WordPress sites and their associated databases that were created by the setup automation script. This is useful for cleaning up your environment when the sites are no longer needed.

#### What the script does:

1. **Delete Site Folders**:
   - The script deletes all WordPress site folders that start with the prefix `site` in the `htdocs` directory.
   - It uses the `os` module to iterate through the folders in the `htdocs` directory and removes any folder named `site1`, `site2`, etc., by calling `rm -rf` on them.

2. **Delete Site Databases**:
   - The script connects to a MariaDB server using `mysql.connector`.
   - It retrieves all the databases and drops those that start with the prefix `site`, effectively deleting all the databases associated with the sites.
   - It performs a `DROP DATABASE` operation for each identified site database.

### Execution Flow:

- The script first deletes all the site folders located in the `htdocs` directory.
- Then, it proceeds to remove all databases named `site1`, `site2`, etc., from the MariaDB server.
- After the execution, all site folders and databases are completely removed from your system.

This script ensures that your environment is cleaned up and free of any previously created sites and their data.


