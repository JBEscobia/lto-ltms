# LTO Information Management System
**CMSC 127 — 2nd Semester AY 2025-2026**

A terminal-based system for managing LTO records — drivers, vehicles, registrations, and violations. Built with Python and MariaDB.

---

## What it can do

- **Drivers** — add, update, delete, and search driver license records
- **Vehicles** — manage vehicle info linked to a driver's license number
- **Registrations** — track vehicle registration status and expiration dates
- **Violations** — record traffic violations and their payment status
- **Reports** — 7 pre-built reports using database views and stored procedures

---

## Setup

### 1. Install MariaDB and add it to PATH
Download from [mariadb.org](https://mariadb.org). Then add this to your system PATH:
```
C:\Program Files\MariaDB 12.2\bin
```

### 2. Create the database and user
```bash
mysql -u root -p
```
```sql
CREATE DATABASE lto_ims;
CREATE USER 'lto_user'@'localhost' IDENTIFIED BY 'pass1234';
GRANT ALL PRIVILEGES ON lto_ims.* TO 'lto_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Run the SQL files (in this order)
From inside the `lto-ims/` folder:
```bash
mysql -u lto_user -p lto_ims < sql/schema.sql
mysql -u lto_user -p lto_ims < sql/seed_data.sql
mysql -u lto_user -p lto_ims < sql/db_objects.sql
```

### 4. Set up your config file
```bash
cp config/db_config.example.py config/db_config.py
```
Then open `db_config.py` and fill in your password. **Don't commit this file to Git.**

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Run the app
```bash
python -m app.main
```

---

## Project Structure

```
lto-ims/
├── app/
│   ├── main.py          # entry point and all menus
│   ├── driver.py        # driver CRUD
│   ├── vehicle.py       # vehicle CRUD
│   ├── registration.py  # registration CRUD
│   ├── violation.py     # violation CRUD
│   ├── reports.py       # report queries
│   ├── db_connection.py # database connection
│   └── ascii_art.py     # pepe art for feedback
├── config/
│   └── db_config.example.py
├── sql/
│   ├── schema.sql       # table definitions
│   ├── seed_data.sql    # sample data
│   └── db_objects.sql   # views, stored procedures, triggers
└── requirements.txt
```

---

## Notes

- Dates must be entered as `YYYY-MM-DD`
- Violation types must already exist in the database before you can use them
- Deleting a driver with linked vehicles or violations will fail (intentional — foreign key constraint)
- The database automatically marks registrations and licenses as expired if their expiration date has passed (handled by triggers)

---

*UPLB CMSC 127*