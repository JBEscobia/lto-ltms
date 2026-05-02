# LTO IMS — Land Transportation Office Information Management System
CMSC 127 Final Project | 2nd Semester AY 2025–2026

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up MariaDB
- Install MariaDB locally
- Create the database and user (see guide below)
- Run the SQL files in order:
```bash
mysql -u lto_user -p lto_ims < sql/schema.sql
mysql -u lto_user -p lto_ims < sql/seed_data.sql
mysql -u lto_user -p lto_ims < sql/db_objects.sql
```

### 3. Configure credentials
- Copy `config/db_config.example.py` → `config/db_config.py`
- Fill in your local MariaDB credentials
- **Do not commit `db_config.py`** (it's gitignored)

### 4. Run the app
```bash
python app/main.py
```

## Project Structure
```
lto-ims/
├── app/
│   ├── main.py             # Entry point
│   ├── db_connection.py    # DB connect/disconnect
│   ├── driver.py           # Driver CRUD
│   ├── vehicle.py          # Vehicle CRUD
│   ├── registration.py     # Registration CRUD
│   ├── violation.py        # Violation CRUD
│   └── reports.py          # 7 required report queries
├── sql/
│   ├── schema.sql          # CREATE TABLE statements
│   ├── seed_data.sql       # Dummy data
│   └── db_objects.sql      # Views, procedures, triggers
├── config/
│   ├── db_config.py        # Your credentials (gitignored)
│   └── db_config.example.py
├── .gitignore
├── requirements.txt
└── README.md
```
