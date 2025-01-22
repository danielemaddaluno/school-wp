# school-wp
School Wordpress Playground

Simply execute in order the following commands:

```
docker compose up
python3 main.py
ngrok http --host-header=rewrite http://localhost:8000
```

Read below for a comment on each command.

## 1. Docker Compose 
```
docker compose up
```

This is a Docker Compose configuration that sets up a simple environment with three services:
1) *web*: An Apache server running PHP 8.2 using the `webdevops/php-apache:8.2-alpine` image. It maps port `8000` on the host to port `80` inside the container and serves PHP pages from the local htdocs folder.

2) *db*: A `MariaDB database` (version 10.5), which persists data in the local mysql_data folder. It restarts automatically and exposes port `3306` on the host as port `8002` inside the container. The `root` password is set to `password`.

3) *phpmyadmin*: A PhpMyAdmin service that provides a web interface to manage the MariaDB database. It depends on the db service and exposes port `80` inside the container to port `8001` on the host. It connects to the database using the `root` password `password`.

This setup allows you to run a PHP web application with a MariaDB backend, easily accessible and manageable via PhpMyAdmin.

## 2. Db and htdocs configurations
```
python3 main.py
```
This python script in order:

1. Takes a User Input:
    - The script asks the user how many WordPress sites to create (`num_sites`).


2. Database Creation:
    - It creates `num_sites` number of databases under MariaDB, named sequentially as `site1`, `site2`, `site3`, etc.

3. Download WordPress:
   - The script downloads the latest WordPress version zip from "https://wordpress.org/latest.zip."
   - It shows a progress bar while downloading the file.

4. Unzip WordPress
   - The script unzips the downloaded WordPress file and extracts the `wordpress` folder.

5. Copy WordPress Files
   - It copies the contents of the `wordpress` folder `num_sites` times, placing them into respective directories under `/htdocs/site1`, `/htdocs/site2`, `/htdocs/site3`, etc.

6. Modify Configuration
   - In each folder, it replaces:
     - `username_here` with "admin"
     - `password_here` with "password"
     - `database_name_here` with the corresponding folder name (e.g., `site1`, `site2`, etc.) in the `wp-config-sample.php` file.

7. Rename Configuration
   - It renames each `wp-config-sample.php` file to `wp-config.php` after the modifications.

---

This script sets up multiple WordPress sites, configures them with their respective databases, and modifies their configuration files accordingly.


## 3. Mapping the services with ngrok
```
brew install ngrok
ngrok config add-authtoken <TOKEN>
```
See https://ngrok.com/docs/getting-started/ for more

```
ngrok http --host-header=rewrite http://localhost:8000
```

This commands allows you to use ngrok with Wordpress.<br>
To make ngrok work properly with the latest Wordpress installation, you only need to tell ngrok to rewrite the host header and point to the port of your Wordpress install (for more read these: [link1](https://dashboard.ngrok.com/) and [link2](https://ngrok.com/docs/using-ngrok-with/wordpress/)).