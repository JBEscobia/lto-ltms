# Entry point for the LTO IMS terminal application.

from app import db_connection
from app import driver, vehicle, registration, violation, reports

#helper functions for printing tables and pausing
def pause():
    input("\nPress Enter to continue...")

def print_separator():
    print("-" * 60)

def print_rows(rows, headers):
    if not rows:
        print("No records found.")
        return
    print_separator()
    print("  ".join(f"{h:<20}" for h in headers))
    print_separator()
    for row in rows:
        print("  ".join(f"{str(col):<20}" for col in row))
    print_separator()
    print(f"{len(rows)} record(s) found.")



#menu for driver management
def menu_driver(conn):
    while True:
        print("\n--- Driver Management ---")
        print("1. Add Driver")
        print("2. Update Driver")
        print("3. Delete Driver")
        print("4. Search Drivers")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n-- Add Driver --")
            license_number  = input("License Number (e.g. N01-12-123456): ").strip()
            full_name       = input("Full Name: ").strip()
            date_of_birth   = input("Date of Birth (YYYY-MM-DD): ").strip()
            sex             = input("Sex (M/F): ").strip().upper()
            address         = input("Address: ").strip()
            license_type    = input("License Type (Student Permit / Non-Professional / Professional): ").strip()
            license_status  = input("License Status (Valid / Expired / Suspended / Revoked): ").strip()
            issuance_date   = input("Issuance Date (YYYY-MM-DD): ").strip()
            expiration_date = input("Expiration Date (YYYY-MM-DD): ").strip()
            if not all([license_number, full_name, date_of_birth, sex, address,
                        license_type, license_status, issuance_date, expiration_date]):
                print("All fields are required. Please try again.")
                pause()
                continue
            ok, msg = driver.add_driver(conn, license_number, full_name, date_of_birth,
                                        sex, address, license_type, license_status,
                                        issuance_date, expiration_date)
            print(msg)
            pause()

        elif choice == "2":
            print("\n-- Update Driver --")
            print("Enter the license number of the driver to update.")
            print("Leave fields blank to keep them unchanged.")
            license_number  = input("License Number: ").strip()
            full_name       = input("New Full Name (blank to skip): ").strip() or None
            date_of_birth   = input("New Date of Birth (blank to skip): ").strip() or None
            sex             = input("New Sex M/F (blank to skip): ").strip().upper() or None
            address         = input("New Address (blank to skip): ").strip() or None
            license_type    = input("New License Type (blank to skip): ").strip() or None
            license_status  = input("New License Status (blank to skip): ").strip() or None
            issuance_date   = input("New Issuance Date (blank to skip): ").strip() or None
            expiration_date = input("New Expiration Date (blank to skip): ").strip() or None
            ok, msg = driver.update_driver(conn, license_number, full_name, date_of_birth,
                                           sex, address, license_type, license_status,
                                           issuance_date, expiration_date)
            print(msg)
            pause()

        elif choice == "3":
            print("\n-- Delete Driver --")
            license_number = input("License Number of driver to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{license_number}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                ok, msg = driver.delete_driver(conn, license_number)
                print(msg)
            else:
                print("Cancelled.")
            pause()

        elif choice == "4":
            print("\n-- Search Drivers --")
            keyword = input("Search by name or license number (blank for all): ").strip() or None
            ok, result = driver.search_drivers(conn, keyword)
            if ok:
                headers = ["License No.", "Full Name", "DOB", "Sex",
                           "Address", "Type", "Status", "Issued", "Expires"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "0":
            break


#menu for vehicle management
def menu_vehicle(conn):
    while True:
        print("\n--- Vehicle Management ---")
        print("1. Add Vehicle")
        print("2. Update Vehicle")
        print("3. Delete Vehicle")
        print("4. Search Vehicles")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n-- Add Vehicle --")
            plate_number   = input("Plate Number (e.g. ABC-1234): ").strip()
            license_number = input("Owner's License Number: ").strip()
            engine_number  = input("Engine Number: ").strip()
            chassis_number = input("Chassis Number: ").strip()
            vehicle_type   = input("Vehicle Type (e.g. Private Car / Motorcycle / PUV): ").strip()
            make           = input("Make/Brand (e.g. Toyota): ").strip()
            model_name     = input("Model (e.g. Vios): ").strip()
            year_model     = input("Year Model (e.g. 2022): ").strip()
            color          = input("Color: ").strip()
            if not all([plate_number, license_number, engine_number, chassis_number,
                        vehicle_type, make, model_name, year_model, color]):
                print("All fields are required. Please try again.")
                pause()
                continue
            if not year_model.isdigit():
                print("Year Model must be a number. Please try again.")
                pause()
                continue
            ok, msg = vehicle.add_vehicle(conn, plate_number, license_number, engine_number,
                                          chassis_number, vehicle_type, make, model_name,
                                          int(year_model), color)
            print(msg)
            pause()

        elif choice == "2":
            print("\n-- Update Vehicle --")
            print("Enter the plate number of the vehicle to update.")
            print("Leave fields blank to keep them unchanged.")
            plate_number   = input("Plate Number: ").strip()
            license_number = input("New Owner License Number (blank to skip): ").strip() or None
            engine_number  = input("New Engine Number (blank to skip): ").strip() or None
            chassis_number = input("New Chassis Number (blank to skip): ").strip() or None
            vehicle_type   = input("New Vehicle Type (blank to skip): ").strip() or None
            make           = input("New Brand (blank to skip): ").strip() or None
            model_name     = input("New Model (blank to skip): ").strip() or None
            year_input     = input("New Year Model (blank to skip): ").strip()
            year_model     = int(year_input) if year_input else None
            color          = input("New Color (blank to skip): ").strip() or None
            ok, msg = vehicle.update_vehicle(conn, plate_number, license_number, engine_number,
                                             chassis_number, vehicle_type, make, model_name,
                                             year_model, color)
            print(msg)
            pause()

        elif choice == "3":
            print("\n-- Delete Vehicle --")
            plate_number = input("Plate Number of vehicle to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{plate_number}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                ok, msg = vehicle.delete_vehicle(conn, plate_number)
                print(msg)
            else:
                print("Cancelled.")
            pause()

        elif choice == "4":
            print("\n-- Search Vehicles --")
            keyword = input("Search by plate number, make, or model (blank for all): ").strip() or None
            ok, result = vehicle.search_vehicles(conn, keyword)
            if ok:
                headers = ["Plate No.", "License No.", "Engine No.", "Chassis No.",
                           "Type", "Make", "Model", "Year", "Color"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "0":
            break


# menu for regustration management
def menu_registration(conn):
    while True:
        print("\n--- Registration Management ---")
        print("1. Add Registration")
        print("2. Update Registration")
        print("3. Delete Registration")
        print("4. Search Registrations")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n-- Add Registration --")
            registration_number = input("Registration Number (e.g. REG-2024-00001): ").strip()
            plate_number        = input("Plate Number of vehicle: ").strip()
            registration_date   = input("Registration Date (YYYY-MM-DD): ").strip()
            expiration_date     = input("Expiration Date (YYYY-MM-DD): ").strip()
            reg_status          = input("Status (Active / Expired / Suspended): ").strip()
            if not all([registration_number, plate_number, registration_date,
                        expiration_date, reg_status]):
                print("All fields are required. Please try again.")
                pause()
                continue
            ok, msg = registration.add_registration(conn, registration_number, plate_number,
                                                    registration_date, expiration_date, reg_status)
            print(msg)
            pause()

        elif choice == "2":
            print("\n-- Update Registration --")
            print("Enter the registration number to update.")
            print("Leave fields blank to keep them unchanged.")
            registration_number = input("Registration Number: ").strip()
            plate_number        = input("New Plate Number (blank to skip): ").strip() or None
            registration_date   = input("New Registration Date (blank to skip): ").strip() or None
            expiration_date     = input("New Expiration Date (blank to skip): ").strip() or None
            reg_status          = input("New Status (blank to skip): ").strip() or None
            ok, msg = registration.update_registration(conn, registration_number, plate_number,
                                                       registration_date, expiration_date, reg_status)
            print(msg)
            pause()

        elif choice == "3":
            print("\n-- Delete Registration --")
            registration_number = input("Registration Number to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{registration_number}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                ok, msg = registration.delete_registration(conn, registration_number)
                print(msg)
            else:
                print("Cancelled.")
            pause()

        elif choice == "4":
            print("\n-- Search Registrations --")
            print("All filters are optional — leave blank to skip.")
            keyword     = input("Search by registration number keyword: ").strip() or None
            plate_number = input("Filter by plate number (exact): ").strip() or None
            reg_status  = input("Filter by status (Active / Expired / Suspended): ").strip() or None
            ok, result = registration.search_registrations(conn, keyword, plate_number, reg_status)
            if ok:
                headers = ["Reg. Number", "Plate No.", "Reg. Date", "Exp. Date", "Status"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "0":
            break


#menu for violation management
def menu_violation(conn):
    while True:
        print("\n--- Violation Management ---")
        print("1. Add Violation")
        print("2. Update Violation")
        print("3. Delete Violation")
        print("4. Search Violations")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n-- Add Violation --")
            ticket_number  = input("Ticket Number (e.g. VIO-2024-00001): ").strip()
            license_number = input("Driver's License Number: ").strip()
            plate_number   = input("Vehicle Plate Number: ").strip()
            v_type         = input("Violation Type (must exist in system, e.g. Overspeeding): ").strip()
            v_date         = input("Violation Date (YYYY-MM-DD): ").strip()
            location       = input("Location (e.g. Calamba, Laguna): ").strip()
            v_status       = input("Status (Unpaid / Paid / Contested): ").strip()
            officer        = input("Apprehending Officer (blank if unknown): ").strip() or None
            if not all([ticket_number, license_number, plate_number,
                        v_type, v_date, location, v_status]):
                print("All fields are required. Please try again.")
                pause()
                continue
            ok, msg = violation.add_violation(conn, ticket_number, license_number, plate_number,
                                              v_type, v_date, location, v_status, officer)
            print(msg)
            pause()

        elif choice == "2":
            print("\n-- Update Violation --")
            print("Enter the ticket number to update.")
            print("Leave fields blank to keep them unchanged.")
            ticket_number  = input("Ticket Number: ").strip()
            license_number = input("New License Number (blank to skip): ").strip() or None
            plate_number   = input("New Plate Number (blank to skip): ").strip() or None
            v_type         = input("New Violation Type (blank to skip): ").strip() or None
            v_date         = input("New Violation Date (blank to skip): ").strip() or None
            location       = input("New Location (blank to skip): ").strip() or None
            officer        = input("New Apprehending Officer (blank to skip): ").strip() or None
            v_status       = input("New Status (blank to skip): ").strip() or None
            ok, msg = violation.update_violation(conn, ticket_number, license_number, plate_number,
                                                 v_type, v_date, location, officer, v_status)
            print(msg)
            pause()

        elif choice == "3":
            print("\n-- Delete Violation --")
            ticket_number = input("Ticket Number to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{ticket_number}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                ok, msg = violation.delete_violation(conn, ticket_number)
                print(msg)
            else:
                print("Cancelled.")
            pause()

        elif choice == "4":
            print("\n-- Search Violations --")
            print("All filters are optional — leave blank to skip.")
            keyword        = input("Search by ticket number keyword: ").strip() or None
            license_number = input("Filter by driver's license number (exact): ").strip() or None
            plate_number   = input("Filter by plate number (exact): ").strip() or None
            v_status       = input("Filter by status (Unpaid / Paid / Contested): ").strip() or None
            v_type         = input("Filter by violation type (exact): ").strip() or None
            ok, result = violation.search_violations(conn, keyword, license_number,
                                                     plate_number, v_status, v_type)
            if ok:
                headers = ["Ticket No.", "License No.", "Plate No.", "Type",
                           "Fine (PHP)", "Date", "Location", "Officer", "Status"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "0":
            break


#menu of reports
def menu_reports(conn):
    while True:
        print("\n--- Reports ---")
        print("1. Drivers filtered by type / status / age / sex")
        print("2. Vehicles owned by a driver")
        print("3. Vehicles with expired registrations as of a date")
        print("4. Drivers with expired or suspended licenses")
        print("5. Violations by a driver within a date range")
        print("6. Total violations per type for a given year")
        print("7. Vehicles in violations within a city or region")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print("\n-- Report: Drivers (filtered) --")
            print("Leave any filter blank to skip it.")
            license_type   = input("License Type: ").strip() or None
            license_status = input("License Status: ").strip() or None
            age_min_input  = input("Min Age: ").strip()
            age_max_input  = input("Max Age: ").strip()
            sex            = input("Sex (M/F): ").strip().upper() or None
            age_min = int(age_min_input) if age_min_input else None
            age_max = int(age_max_input) if age_max_input else None
            ok, result = reports.report_drivers_filtered(conn, license_type, license_status,
                                                         age_min, age_max, sex)
            if ok:
                headers = ["License No.", "Name", "DOB", "Age", "Sex",
                           "Address", "Type", "Status", "Issued", "Expires",
                           "Vehicles", "Violations"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "2":
            print("\n-- Report: Vehicles by Driver --")
            license_number = input("Driver's License Number: ").strip()
            ok, result = reports.report_vehicles_by_driver(conn, license_number)
            if ok:
                headers = ["Plate No.", "Engine No.", "Chassis No.",
                           "Type", "Make", "Model", "Year", "Color"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "3":
            print("\n-- Report: Expired Registrations --")
            as_of_date = input("As of date (YYYY-MM-DD): ").strip()
            ok, result = reports.report_expired_registrations(conn, as_of_date)
            if ok:
                headers = ["Reg. No.", "Plate No.", "Type", "Make", "Model",
                           "Year", "Color", "Owner", "License No.",
                           "Reg. Date", "Exp. Date", "Status"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "4":
            print("\n-- Report: Expired/Suspended Drivers --")
            ok, result = reports.report_expired_suspended_drivers(conn)
            if ok:
                headers = ["License No.", "Full Name", "License Type",
                           "Status", "Expiration Date"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "5":
            print("\n-- Report: Violations by Driver --")
            license_number = input("Driver's License Number: ").strip()
            date_from      = input("From date (YYYY-MM-DD): ").strip()
            date_to        = input("To date (YYYY-MM-DD): ").strip()
            ok, result = reports.report_violations_by_driver(conn, license_number,
                                                             date_from, date_to)
            if ok:
                headers = ["Ticket No.", "Plate No.", "Type", "Fine (PHP)",
                           "Date", "Location", "Officer", "Status"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "6":
            print("\n-- Report: Violations per Type by Year --")
            year = input("Year (e.g. 2024): ").strip()
            ok, result = reports.report_violations_per_type(conn, int(year))
            if ok:
                headers = ["Violation Type", "Total Violations", "Total Fines (PHP)"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "7":
            print("\n-- Report: Vehicles in Violations by Location --")
            location_keyword = input("City or region keyword (e.g. Laguna): ").strip()
            ok, result = reports.report_vehicles_in_violations_by_location(conn, location_keyword)
            if ok:
                headers = ["Plate No.", "Make", "Model",
                           "Driver Name", "License No.", "Violation Count"]
                print_rows(result, headers)
            else:
                print(f"Error: {result}")
            pause()

        elif choice == "0":
            break


def main():
    print("=" * 60)
    print("   LTO Information Management System")
    print("   CMSC 127 — 2nd Semester AY 2025-2026")
    print("=" * 60)

    try:
        conn = db_connection.get_connection()
        print("Connected to database.\n")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    while True:
        print("\n===== Main Menu =====")
        print("1. Driver Management")
        print("2. Vehicle Management")
        print("3. Registration Management")
        print("4. Violation Management")
        print("5. Reports")
        print("0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            menu_driver(conn)
        elif choice == "2":
            menu_vehicle(conn)
        elif choice == "3":
            menu_registration(conn)
        elif choice == "4":
            menu_violation(conn)
        elif choice == "5":
            menu_reports(conn)
        elif choice == "0":
            print("Goodbye!")
            db_connection.close_connection(conn)
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()