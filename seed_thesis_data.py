"""
Seed script for FYP Budgeting System
Creates 3 demonstration accounts with realistic transaction histories for thesis defense:
1. Sophia Santos (sophia) - 3 months history (Jul-Sep 2026), Low Risk (Safe ~58% pace)
2. Marcus Reyes (marcus) - 6 months history (Apr-Sep 2026), High Risk (Will Overspend ~135% pace)
3. Elena Cruz (elena) - 12 months history (Oct 2025 - Sep 2026), Medium Risk (Safe close to limit ~86% pace)
"""

import sys
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
import mysql.connector

# Import database connection from app
import app

def run_seed():
    conn = app.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("=" * 60)
    print("SEEDING THESIS DEMONSTRATION DATA")
    print("=" * 60)
    
    # 1. User Profiles definition
    users_data = [
        {
            "username": "sophia",
            "full_name": "Sophia Santos",
            "email": "sophia@trimex.edu.ph",
            "contact_number": "09171234567",
            "password_plain": "Trimex1",
            "target_income": 35000.0,
            "target_limit": 25000.0,
            # 3 months: July, August, September 2026 (Varied irregular amounts)
            "months": ["2026-07", "2026-08", "2026-09"],
            "monthly_expenses": {
                "2026-07": [
                    ("Food", 2145.50, "SM Supermarket Monthly Grocery", 5),
                    ("Food", 1680.00, "Puregold Pantry Restock", 18),
                    ("Food", 940.00, "Campus Lunch & Snacks", 25),
                    ("Transportation", 1420.00, "Monthly Commute / Bus Card Reload", 3),
                    ("Transportation", 980.00, "Jeepney & Tricycle Fares", 20),
                    ("Utilities", 2385.00, "Meralco Electric Bill", 12),
                    ("Utilities", 1499.00, "PLDT Home Fiber Internet", 15),
                    ("Entertainment", 1380.00, "Netflix & Cinema Weekend", 22),
                    ("Other", 1495.00, "School Supplies & Personal Care", 28),
                ],
                "2026-08": [
                    ("Food", 2290.00, "Robinsons Supermarket Grocery", 4),
                    ("Food", 1845.00, "Puregold Meat & Veggies", 16),
                    ("Food", 1120.00, "Campus Lunch & Meals", 24),
                    ("Transportation", 1550.00, "Commute Beep Card Reload", 2),
                    ("Transportation", 1050.00, "Jeepney & Commute Fare", 19),
                    ("Utilities", 2640.00, "Meralco Electric Bill", 11),
                    ("Utilities", 1499.00, "PLDT Home Fiber Internet", 15),
                    ("Entertainment", 1495.00, "Weekend Outing & Cafe", 21),
                    ("Other", 1395.00, "School Project Supplies", 27),
                ],
                "2026-09": [
                    ("Food", 2185.00, "SM Supermarket Monthly Grocery", 6),
                    ("Food", 1782.00, "Puregold Mid-month Restock", 17),
                    ("Food", 980.00, "Campus Lunch & Snacks", 23),
                    ("Transportation", 1480.00, "Monthly Bus & Transit Pass", 3),
                    ("Transportation", 970.00, "Tricycle & Jeepney Fares", 20),
                    ("Utilities", 2490.00, "Meralco Electric Bill", 12),
                    ("Utilities", 1499.00, "PLDT Home Fiber Internet", 15),
                    ("Entertainment", 1510.00, "Streaming & Cinema Outing", 22),
                    ("Other", 1490.00, "Personal Care Essentials", 28),
                ],
            }
        },
        {
            "username": "marcus",
            "full_name": "Marcus Reyes",
            "email": "marcus@trimex.edu.ph",
            "contact_number": "09187654321",
            "password_plain": "Trimex2",
            "target_income": 30000.0,
            "target_limit": 20000.0,
            # 6 months: April to September 2026 (Varied irregular overspending)
            "months": ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"],
            "monthly_expenses": {
                "2026-04": [
                    ("Food", 4250.00, "Weekly Grocery & Meat Shop", 4),
                    ("Food", 2890.00, "GrabFood & FoodPanda Orders", 16),
                    ("Food", 1780.00, "Restaurant Dining with Friends", 26),
                    ("Transportation", 2750.00, "Grab Car & Taxi Rides", 8),
                    ("Transportation", 1380.00, "Fuel & Toll Fees", 21),
                    ("Utilities", 2895.00, "Electric Bill (Aircon)", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3240.00, "Online Gaming & Steam Purchases", 11),
                    ("Entertainment", 1860.00, "Weekend Bar & Night Out", 24),
                    ("Other", 3101.00, "Online Shopping Gadgets / Shopee", 27),
                ],
                "2026-05": [
                    ("Food", 4680.00, "Supermarket Grocery & Meat Shop", 4),
                    ("Food", 3210.00, "GrabFood Late Night Orders", 16),
                    ("Food", 2150.00, "Buffet & Dining with Friends", 26),
                    ("Transportation", 3120.00, "Grab Car & Surge Rides", 8),
                    ("Transportation", 1580.00, "Fuel & Toll Expenses", 21),
                    ("Utilities", 3180.00, "Electric Bill (Heavy Aircon)", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3650.00, "Gaming Peripherals & Steam", 11),
                    ("Entertainment", 2240.00, "Weekend Bar & Night Out", 24),
                    ("Other", 2180.00, "Shopee & Lazada Shopping", 27),
                ],
                "2026-06": [
                    ("Food", 4390.00, "S&R Grocery & Meat Shop", 4),
                    ("Food", 2850.00, "FoodPanda & Grab Delivery", 16),
                    ("Food", 1890.00, "Restaurant Dinner with Friends", 26),
                    ("Transportation", 2880.00, "Grab Rides & Taxi Commute", 8),
                    ("Transportation", 1440.00, "Gasoline Fill-up", 21),
                    ("Utilities", 2940.00, "Meralco Electric Bill", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3380.00, "Steam Summer Sale Games", 11),
                    ("Entertainment", 1820.00, "KTV & Weekend Drinks", 24),
                    ("Other", 3109.00, "Shopee Electronics & Accessories", 27),
                ],
                "2026-07": [
                    ("Food", 4820.00, "Monthly Grocery & Meat Supply", 4),
                    ("Food", 3450.00, "GrabFood Premium Orders", 16),
                    ("Food", 2280.00, "Samgyupsal Dinner with Friends", 26),
                    ("Transportation", 3250.00, "Grab Car Rides & Toll", 8),
                    ("Transportation", 1620.00, "Fuel & Highway Tolls", 21),
                    ("Utilities", 3310.00, "Electric Bill (Peak Usage)", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3790.00, "Console Games & In-game Skins", 11),
                    ("Entertainment", 2310.00, "Nightclub & Weekend Bar", 24),
                    ("Other", 1999.00, "Wireless Earbuds Shopee", 27),
                ],
                "2026-08": [
                    ("Food", 4450.00, "Weekly Grocery & Fresh Meat", 4),
                    ("Food", 2980.00, "GrabFood Lunch Deliveries", 16),
                    ("Food", 1950.00, "Casual Dining with Friends", 26),
                    ("Transportation", 2940.00, "Grab Car & Taxi Rides", 8),
                    ("Transportation", 1510.00, "Fuel & Parking Fees", 21),
                    ("Utilities", 3050.00, "Electric Bill (Aircon)", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3420.00, "Steam Games & Subscriptions", 11),
                    ("Entertainment", 2050.00, "Billiards & Bar Night", 24),
                    ("Other", 3015.00, "Shopee Gadget Accessories", 27),
                ],
                "2026-09": [
                    ("Food", 4580.00, "Supermarket Grocery Supply", 4),
                    ("Food", 3120.00, "FoodPanda & Grab Delivery", 16),
                    ("Food", 2080.00, "Weekend Dining Out", 26),
                    ("Transportation", 3050.00, "Grab Car Surge Rides", 8),
                    ("Transportation", 1560.00, "Fuel & Toll Fees", 21),
                    ("Utilities", 3140.00, "Electric Bill (Aircon)", 10),
                    ("Utilities", 1499.00, "Converge Fiber Internet", 14),
                    ("Entertainment", 3580.00, "Gaming Battle Pass & Titles", 11),
                    ("Entertainment", 2190.00, "Bar Outing with Friends", 24),
                    ("Other", 2811.00, "Shopee 9.9 Mega Sale Purchases", 27),
                ],
            }
        },
        {
            "username": "elena",
            "full_name": "Elena Cruz",
            "email": "elena@trimex.edu.ph",
            "contact_number": "09199887766",
            "password_plain": "Trimex3",
            "target_income": 28000.0,
            "target_limit": 22000.0,
            # 12 months: Oct 2025 to Sep 2026 (Varied irregular baseline ~86% pace)
            "months": [
                "2025-10", "2025-11", "2025-12",
                "2026-01", "2026-02", "2026-03",
                "2026-04", "2026-05", "2026-06",
                "2026-07", "2026-08", "2026-09"
            ],
            "monthly_expenses": {
                m: [
                    ("Food", round(3400.0 + ((i * 47) % 320), 2), "Public Market & Grocery Run", 3),
                    ("Food", round(2400.0 + ((i * 63) % 250), 2), "Weekly Meal Prep Ingredients", 14),
                    ("Food", round(950.0 + ((i * 31) % 180), 2), "Coffee & Occasional Dining", 23),
                    ("Transportation", round(1920.0 + ((i * 53) % 210), 2), "MRT & Bus Commute Allowance", 6),
                    ("Transportation", round(1450.0 + ((i * 41) % 160), 2), "Motorcycle Angkas/MoveIt Trips", 19),
                    ("Utilities", round(2900.0 + ((i * 71) % 280), 2), "Meralco Electric & Water Bill", 12),
                    ("Utilities", 1499.00, "Globe Postpaid & WiFi Plan", 17),
                    ("Entertainment", round(2400.0 + ((i * 59) % 260), 2), "Streaming & Weekend Outing", 21),
                    ("Other", round(1450.0 + ((i * 37) % 170), 2), "Medicines & Household Supplies", 27),
                ]
                for i, m in enumerate([
                    "2025-10", "2025-11", "2025-12",
                    "2026-01", "2026-02", "2026-03",
                    "2026-04", "2026-05", "2026-06",
                    "2026-07", "2026-08", "2026-09"
                ])
            }
        }
    ]

    sql_statements = []
    sql_statements.append("-- Seed Data for Thesis Demonstration Accounts")
    sql_statements.append("-- Target Forecasting Month: October 2026 (2026-10)\n")

    for u in users_data:
        uname = u["username"]
        # Remove existing user records for clean seed
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (uname, u["email"]))
        existing = cursor.fetchone()
        if existing:
            uid = existing["id"]
            cursor.execute("DELETE FROM expenses WHERE user_id = %s", (uid,))
            cursor.execute("DELETE FROM budgets WHERE user_id = %s", (uid,))
            cursor.execute("DELETE FROM users WHERE id = %s", (uid,))
            conn.commit()
            print(f"[CLEANUP] Removed existing records for user '{uname}' (ID: {uid})")

        # Insert User
        pwd_hash = generate_password_hash(u["password_plain"])
        cursor.execute(
            """
            INSERT INTO users (username, full_name, email, contact_number, password, role)
            VALUES (%s, %s, %s, %s, %s, 'user')
            """,
            (uname, u["full_name"], u["email"], u["contact_number"], pwd_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        print(f"\n[CREATED USER] {u['full_name']} (@{uname}) | ID: {user_id} | Password: {u['password_plain']}")

        sql_statements.append(f"-- User: {u['full_name']} (@{uname})")
        sql_statements.append(
            f"INSERT INTO users (username, full_name, email, contact_number, password, role) "
            f"VALUES ('{uname}', '{u['full_name']}', '{u['email']}', '{u['contact_number']}', '{pwd_hash}', 'user');"
        )
        sql_statements.append(f"SET @user_{uname}_id = LAST_INSERT_ID();")

        # Insert Budgets for all historical months + Target month (2026-10)
        all_months = u["months"] + ["2026-10"]
        for m in all_months:
            cursor.execute(
                """
                INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, u["target_income"], u["target_limit"], m)
            )
            sql_statements.append(
                f"INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) "
                f"VALUES (@user_{uname}_id, {u['target_income']}, {u['target_limit']}, '{m}');"
            )
        conn.commit()
        print(f"  -> Created budgets for {len(all_months)} months (including 2026-10)")

        # Insert Expenses for each historical month
        total_expense_records = 0
        for m in u["months"]:
            y, mo = m.split("-")
            month_expenses = u["monthly_expenses"].get(m, [])
            for cat, amt, desc, day in month_expenses:
                # Ensure valid day format
                exp_date = f"{y}-{mo}-{day:02d}"
                cursor.execute(
                    """
                    INSERT INTO expenses (user_id, category, amount, description, expense_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, cat, amt, desc, exp_date)
                )
                sql_statements.append(
                    f"INSERT INTO expenses (user_id, category, amount, description, expense_date) "
                    f"VALUES (@user_{uname}_id, '{cat}', {amt}, '{desc}', '{exp_date}');"
                )
                total_expense_records += 1

        conn.commit()
        print(f"  -> Created {total_expense_records} expense records across {len(u['months'])} historical months.")

    cursor.close()
    conn.close()

    # Save SQL file
    sql_path = os.path.join(os.path.dirname(__file__), "seed_thesis_data.sql")
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements) + "\n")
    print(f"\n[SUCCESS] Seed SQL script exported to: {sql_path}")
    print("=" * 60)

if __name__ == "__main__":
    run_seed()

