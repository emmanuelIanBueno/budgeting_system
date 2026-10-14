-- Seed Data for Thesis Demonstration Accounts
-- Target Forecasting Month: October 2026 (2026-10)

CREATE DATABASE IF NOT EXISTS budgeting_db;
USE budgeting_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    contact_number VARCHAR(30),
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    monthly_income DECIMAL(10, 2) NOT NULL,
    budget_limit DECIMAL(10, 2) NOT NULL,
    month_year VARCHAR(7) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    username VARCHAR(50) NOT NULL,
    user_role VARCHAR(20) DEFAULT 'user',
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- User: Sophia Santos (@sophia)
DELETE FROM expenses WHERE user_id IN (SELECT id FROM users WHERE username = 'sophia');
DELETE FROM budgets WHERE user_id IN (SELECT id FROM users WHERE username = 'sophia');
DELETE FROM users WHERE username = 'sophia';
INSERT INTO users (username, full_name, email, contact_number, password, role) VALUES ('sophia', 'Sophia Santos', 'sophia@trimex.edu.ph', '09171234567', 'scrypt:32768:8:1$JTMNOFJajLYlj5zQ$003081e175c70494e33c338e45205a6960b8a9935a7b5e1a6b43eb66e9f3a018aaed9ad713e5f3afd1f1d47b34ab18b2357eccc646e76b132a2b1af9cfea2c6f', 'user');
SET @user_sophia_id = LAST_INSERT_ID();
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_sophia_id, 35000.0, 25000.0, '2026-07');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_sophia_id, 35000.0, 25000.0, '2026-08');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_sophia_id, 35000.0, 25000.0, '2026-09');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_sophia_id, 35000.0, 25000.0, '2026-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 2145.5, 'SM Supermarket Monthly Grocery', '2026-07-05');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 1680.0, 'Puregold Pantry Restock', '2026-07-18');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 940.0, 'Campus Lunch & Snacks', '2026-07-25');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 1420.0, 'Monthly Commute / Bus Card Reload', '2026-07-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 980.0, 'Jeepney & Tricycle Fares', '2026-07-20');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 2385.0, 'Meralco Electric Bill', '2026-07-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 1499.0, 'PLDT Home Fiber Internet', '2026-07-15');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Entertainment', 1380.0, 'Netflix & Cinema Weekend', '2026-07-22');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Other', 1495.0, 'School Supplies & Personal Care', '2026-07-28');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 2290.0, 'Robinsons Supermarket Grocery', '2026-08-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 1845.0, 'Puregold Meat & Veggies', '2026-08-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 1120.0, 'Campus Lunch & Meals', '2026-08-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 1550.0, 'Commute Beep Card Reload', '2026-08-02');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 1050.0, 'Jeepney & Commute Fare', '2026-08-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 2640.0, 'Meralco Electric Bill', '2026-08-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 1499.0, 'PLDT Home Fiber Internet', '2026-08-15');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Entertainment', 1495.0, 'Weekend Outing & Cafe', '2026-08-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Other', 1395.0, 'School Project Supplies', '2026-08-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 2185.0, 'SM Supermarket Monthly Grocery', '2026-09-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 1782.0, 'Puregold Mid-month Restock', '2026-09-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Food', 980.0, 'Campus Lunch & Snacks', '2026-09-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 1480.0, 'Monthly Bus & Transit Pass', '2026-09-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Transportation', 970.0, 'Tricycle & Jeepney Fares', '2026-09-20');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 2490.0, 'Meralco Electric Bill', '2026-09-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Utilities', 1499.0, 'PLDT Home Fiber Internet', '2026-09-15');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Entertainment', 1510.0, 'Streaming & Cinema Outing', '2026-09-22');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_sophia_id, 'Other', 1490.0, 'Personal Care Essentials', '2026-09-28');

-- User: Marcus Reyes (@marcus)
DELETE FROM expenses WHERE user_id IN (SELECT id FROM users WHERE username = 'marcus');
DELETE FROM budgets WHERE user_id IN (SELECT id FROM users WHERE username = 'marcus');
DELETE FROM users WHERE username = 'marcus';
INSERT INTO users (username, full_name, email, contact_number, password, role) VALUES ('marcus', 'Marcus Reyes', 'marcus@trimex.edu.ph', '09187654321', 'scrypt:32768:8:1$3BpR9DPUMi0b6oKJ$b45f09d5c41c9f16ae69821b88a124bb23219ab35f344604a668c78fd01ee8c6551877a396ec3d8e90db01b4cae35e9dfabdb51a73bd2d40526addbc84326f0a', 'user');
SET @user_marcus_id = LAST_INSERT_ID();
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-04');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-05');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-06');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-07');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-08');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-09');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_marcus_id, 30000.0, 20000.0, '2026-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4250.0, 'Weekly Grocery & Meat Shop', '2026-04-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2890.0, 'GrabFood & FoodPanda Orders', '2026-04-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 1780.0, 'Restaurant Dining with Friends', '2026-04-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 2750.0, 'Grab Car & Taxi Rides', '2026-04-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1380.0, 'Fuel & Toll Fees', '2026-04-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 2895.0, 'Electric Bill (Aircon)', '2026-04-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-04-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3240.0, 'Online Gaming & Steam Purchases', '2026-04-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 1860.0, 'Weekend Bar & Night Out', '2026-04-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 3101.0, 'Online Shopping Gadgets / Shopee', '2026-04-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4680.0, 'Supermarket Grocery & Meat Shop', '2026-05-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 3210.0, 'GrabFood Late Night Orders', '2026-05-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2150.0, 'Buffet & Dining with Friends', '2026-05-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 3120.0, 'Grab Car & Surge Rides', '2026-05-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1580.0, 'Fuel & Toll Expenses', '2026-05-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 3180.0, 'Electric Bill (Heavy Aircon)', '2026-05-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-05-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3650.0, 'Gaming Peripherals & Steam', '2026-05-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 2240.0, 'Weekend Bar & Night Out', '2026-05-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 2180.0, 'Shopee & Lazada Shopping', '2026-05-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4390.0, 'S&R Grocery & Meat Shop', '2026-06-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2850.0, 'FoodPanda & Grab Delivery', '2026-06-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 1890.0, 'Restaurant Dinner with Friends', '2026-06-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 2880.0, 'Grab Rides & Taxi Commute', '2026-06-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1440.0, 'Gasoline Fill-up', '2026-06-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 2940.0, 'Meralco Electric Bill', '2026-06-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-06-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3380.0, 'Steam Summer Sale Games', '2026-06-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 1820.0, 'KTV & Weekend Drinks', '2026-06-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 3109.0, 'Shopee Electronics & Accessories', '2026-06-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4820.0, 'Monthly Grocery & Meat Supply', '2026-07-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 3450.0, 'GrabFood Premium Orders', '2026-07-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2280.0, 'Samgyupsal Dinner with Friends', '2026-07-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 3250.0, 'Grab Car Rides & Toll', '2026-07-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1620.0, 'Fuel & Highway Tolls', '2026-07-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 3310.0, 'Electric Bill (Peak Usage)', '2026-07-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-07-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3790.0, 'Console Games & In-game Skins', '2026-07-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 2310.0, 'Nightclub & Weekend Bar', '2026-07-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 1999.0, 'Wireless Earbuds Shopee', '2026-07-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4450.0, 'Weekly Grocery & Fresh Meat', '2026-08-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2980.0, 'GrabFood Lunch Deliveries', '2026-08-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 1950.0, 'Casual Dining with Friends', '2026-08-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 2940.0, 'Grab Car & Taxi Rides', '2026-08-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1510.0, 'Fuel & Parking Fees', '2026-08-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 3050.0, 'Electric Bill (Aircon)', '2026-08-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-08-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3420.0, 'Steam Games & Subscriptions', '2026-08-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 2050.0, 'Billiards & Bar Night', '2026-08-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 3015.0, 'Shopee Gadget Accessories', '2026-08-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 4580.0, 'Supermarket Grocery Supply', '2026-09-04');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 3120.0, 'FoodPanda & Grab Delivery', '2026-09-16');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Food', 2080.0, 'Weekend Dining Out', '2026-09-26');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 3050.0, 'Grab Car Surge Rides', '2026-09-08');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Transportation', 1560.0, 'Fuel & Toll Fees', '2026-09-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 3140.0, 'Electric Bill (Aircon)', '2026-09-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Utilities', 1499.0, 'Converge Fiber Internet', '2026-09-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 3580.0, 'Gaming Battle Pass & Titles', '2026-09-11');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Entertainment', 2190.0, 'Bar Outing with Friends', '2026-09-24');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_marcus_id, 'Other', 2811.0, 'Shopee 9.9 Mega Sale Purchases', '2026-09-27');

-- User: Elena Cruz (@elena)
DELETE FROM expenses WHERE user_id IN (SELECT id FROM users WHERE username = 'elena');
DELETE FROM budgets WHERE user_id IN (SELECT id FROM users WHERE username = 'elena');
DELETE FROM users WHERE username = 'elena';
INSERT INTO users (username, full_name, email, contact_number, password, role) VALUES ('elena', 'Elena Cruz', 'elena@trimex.edu.ph', '09199887766', 'scrypt:32768:8:1$VMzDjXGjEkVSLRI3$5f2bdf7aa84bdc183f0a164c1a704eb9a3cd3b30ef62b2e9583fd8ab8524d95bdefd56ded9ef06a5ae16191497ebcc20c73e5cd9b89ff2a3685868c0cdc62ed5', 'user');
SET @user_elena_id = LAST_INSERT_ID();
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2025-10');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2025-11');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2025-12');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-01');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-02');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-03');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-04');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-05');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-06');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-07');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-08');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-09');
INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (@user_elena_id, 28000.0, 22000.0, '2026-10');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3400.0, 'Public Market & Grocery Run', '2025-10-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2400.0, 'Weekly Meal Prep Ingredients', '2025-10-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 950.0, 'Coffee & Occasional Dining', '2025-10-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1920.0, 'MRT & Bus Commute Allowance', '2025-10-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1450.0, 'Motorcycle Angkas/MoveIt Trips', '2025-10-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2900.0, 'Meralco Electric & Water Bill', '2025-10-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2025-10-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2400.0, 'Streaming & Weekend Outing', '2025-10-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1450.0, 'Medicines & Household Supplies', '2025-10-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3447.0, 'Public Market & Grocery Run', '2025-11-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2463.0, 'Weekly Meal Prep Ingredients', '2025-11-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 981.0, 'Coffee & Occasional Dining', '2025-11-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1973.0, 'MRT & Bus Commute Allowance', '2025-11-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1491.0, 'Motorcycle Angkas/MoveIt Trips', '2025-11-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2971.0, 'Meralco Electric & Water Bill', '2025-11-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2025-11-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2459.0, 'Streaming & Weekend Outing', '2025-11-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1487.0, 'Medicines & Household Supplies', '2025-11-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3494.0, 'Public Market & Grocery Run', '2025-12-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2526.0, 'Weekly Meal Prep Ingredients', '2025-12-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1012.0, 'Coffee & Occasional Dining', '2025-12-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2026.0, 'MRT & Bus Commute Allowance', '2025-12-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1532.0, 'Motorcycle Angkas/MoveIt Trips', '2025-12-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3042.0, 'Meralco Electric & Water Bill', '2025-12-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2025-12-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2518.0, 'Streaming & Weekend Outing', '2025-12-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1524.0, 'Medicines & Household Supplies', '2025-12-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3541.0, 'Public Market & Grocery Run', '2026-01-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2589.0, 'Weekly Meal Prep Ingredients', '2026-01-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1043.0, 'Coffee & Occasional Dining', '2026-01-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2079.0, 'MRT & Bus Commute Allowance', '2026-01-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1573.0, 'Motorcycle Angkas/MoveIt Trips', '2026-01-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3113.0, 'Meralco Electric & Water Bill', '2026-01-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-01-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2577.0, 'Streaming & Weekend Outing', '2026-01-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1561.0, 'Medicines & Household Supplies', '2026-01-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3588.0, 'Public Market & Grocery Run', '2026-02-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2402.0, 'Weekly Meal Prep Ingredients', '2026-02-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1074.0, 'Coffee & Occasional Dining', '2026-02-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1922.0, 'MRT & Bus Commute Allowance', '2026-02-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1454.0, 'Motorcycle Angkas/MoveIt Trips', '2026-02-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2904.0, 'Meralco Electric & Water Bill', '2026-02-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-02-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2636.0, 'Streaming & Weekend Outing', '2026-02-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1598.0, 'Medicines & Household Supplies', '2026-02-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3635.0, 'Public Market & Grocery Run', '2026-03-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2465.0, 'Weekly Meal Prep Ingredients', '2026-03-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1105.0, 'Coffee & Occasional Dining', '2026-03-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1975.0, 'MRT & Bus Commute Allowance', '2026-03-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1495.0, 'Motorcycle Angkas/MoveIt Trips', '2026-03-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2975.0, 'Meralco Electric & Water Bill', '2026-03-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-03-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2435.0, 'Streaming & Weekend Outing', '2026-03-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1465.0, 'Medicines & Household Supplies', '2026-03-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3682.0, 'Public Market & Grocery Run', '2026-04-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2528.0, 'Weekly Meal Prep Ingredients', '2026-04-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 956.0, 'Coffee & Occasional Dining', '2026-04-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2028.0, 'MRT & Bus Commute Allowance', '2026-04-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1536.0, 'Motorcycle Angkas/MoveIt Trips', '2026-04-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3046.0, 'Meralco Electric & Water Bill', '2026-04-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-04-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2494.0, 'Streaming & Weekend Outing', '2026-04-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1502.0, 'Medicines & Household Supplies', '2026-04-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3409.0, 'Public Market & Grocery Run', '2026-05-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2591.0, 'Weekly Meal Prep Ingredients', '2026-05-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 987.0, 'Coffee & Occasional Dining', '2026-05-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2081.0, 'MRT & Bus Commute Allowance', '2026-05-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1577.0, 'Motorcycle Angkas/MoveIt Trips', '2026-05-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3117.0, 'Meralco Electric & Water Bill', '2026-05-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-05-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2553.0, 'Streaming & Weekend Outing', '2026-05-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1539.0, 'Medicines & Household Supplies', '2026-05-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3456.0, 'Public Market & Grocery Run', '2026-06-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2404.0, 'Weekly Meal Prep Ingredients', '2026-06-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1018.0, 'Coffee & Occasional Dining', '2026-06-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1924.0, 'MRT & Bus Commute Allowance', '2026-06-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1458.0, 'Motorcycle Angkas/MoveIt Trips', '2026-06-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2908.0, 'Meralco Electric & Water Bill', '2026-06-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-06-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2612.0, 'Streaming & Weekend Outing', '2026-06-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1576.0, 'Medicines & Household Supplies', '2026-06-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3503.0, 'Public Market & Grocery Run', '2026-07-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2467.0, 'Weekly Meal Prep Ingredients', '2026-07-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1049.0, 'Coffee & Occasional Dining', '2026-07-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1977.0, 'MRT & Bus Commute Allowance', '2026-07-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1499.0, 'Motorcycle Angkas/MoveIt Trips', '2026-07-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 2979.0, 'Meralco Electric & Water Bill', '2026-07-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-07-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2411.0, 'Streaming & Weekend Outing', '2026-07-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1613.0, 'Medicines & Household Supplies', '2026-07-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3550.0, 'Public Market & Grocery Run', '2026-08-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2530.0, 'Weekly Meal Prep Ingredients', '2026-08-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1080.0, 'Coffee & Occasional Dining', '2026-08-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2030.0, 'MRT & Bus Commute Allowance', '2026-08-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1540.0, 'Motorcycle Angkas/MoveIt Trips', '2026-08-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3050.0, 'Meralco Electric & Water Bill', '2026-08-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-08-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2470.0, 'Streaming & Weekend Outing', '2026-08-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1480.0, 'Medicines & Household Supplies', '2026-08-27');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 3597.0, 'Public Market & Grocery Run', '2026-09-03');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 2593.0, 'Weekly Meal Prep Ingredients', '2026-09-14');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Food', 1111.0, 'Coffee & Occasional Dining', '2026-09-23');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 2083.0, 'MRT & Bus Commute Allowance', '2026-09-06');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Transportation', 1581.0, 'Motorcycle Angkas/MoveIt Trips', '2026-09-19');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 3121.0, 'Meralco Electric & Water Bill', '2026-09-12');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Utilities', 1499.0, 'Globe Postpaid & WiFi Plan', '2026-09-17');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Entertainment', 2529.0, 'Streaming & Weekend Outing', '2026-09-21');
INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (@user_elena_id, 'Other', 1517.0, 'Medicines & Household Supplies', '2026-09-27');
