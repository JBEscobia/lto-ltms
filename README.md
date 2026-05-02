Steps para ma-run yung mariadb sa pc niyo

1. Download and install MariaDB 12.2 from mariadb.org. During install, set kayo ng personal root password.

2. After install, add this to your system PATH (so you can use mysql from anywhere): <br>
   C:\Program Files\MariaDB 12.2\bin <br>
   (Search 'Environment Variables' in Windows → System variables → Path → New) <br>
   Then close and reopen your terminal after.

3. Open terminal and log in as root: <br>
   mysql -u root -p

4. Run these one by one (type manually, don't copy paste): <br>
   CREATE DATABASE lto_ims; <br>
   CREATE USER 'lto_user'@'localhost' IDENTIFIED BY 'pass1234'; <br>
   GRANT ALL PRIVILEGES ON lto_ims.* TO 'lto_user'@'localhost'; <br>
   FLUSH PRIVILEGES; <br>
   EXIT;

5. Run the SQL files from the project folder: <br>
   mysql -u lto_user -p lto_ims < sql/schema.sql <br>
   mysql -u lto_user -p lto_ims < sql/seed_data.sql <br>
   mysql -u lto_user -p lto_ims < sql/db_objects.sql 

6. Copy config/db_config.example.py → rename to db_config.py and fill in the password 

7. Install Python dependencies: <br>
   pip install -r requirements.txt
