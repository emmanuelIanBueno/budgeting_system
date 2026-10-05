from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this_later'  # For session management

# Inject username, greeting, and admin status into all templates automatically
@app.context_processor
def inject_user_context():
    current_username = session.get('username', '')
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # RBAC State Check: is user authenticated with 'admin' role?
    is_admin = (session.get('role') == 'admin') and ('admin_id' in session)
    admin_username = session.get('admin_username', '')
    admin_name = session.get('admin_name', '')
    
    return dict(
        current_username=current_username,
        greeting=greeting,
        is_admin=is_admin,
        admin_username=admin_username,
        admin_name=admin_name
    )

# 403 Forbidden Error Handler
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

# RBAC Decorator: strictly restricts views to users with 'admin' role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin' or 'admin_id' not in session:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Activity / Audit Logging Helper
def log_activity(username, user_role, action, details='', user_id=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        ip = request.remote_addr or '127.0.0.1'
        cursor.execute(
            """
            INSERT INTO activity_logs (user_id, username, user_role, action, details, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, username or 'Anonymous', user_role or 'user', action, details, ip)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Notice: Failed to record activity log ({e})")


# Database connection function
def get_db_connection():
    kwargs = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'budgeting_db'),
        'port': int(os.environ.get('DB_PORT', 3306))
    }
    # Enable SSL when running against TiDB Cloud or secure cloud MySQL
    if os.environ.get('DB_SSL_VERIFY', '').lower() in ['1', 'true', 'yes'] or kwargs['port'] == 4000:
        kwargs['ssl_verify_cert'] = True
    return mysql.connector.connect(**kwargs)

# Home page
@app.route('/')
def home():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except mysql.connector.Error as error:
            flash(f'Error: {error}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = 'user'
                log_activity(user['username'], 'user', 'USER_LOGIN', 'User logged into client portal.', user['id'])
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                log_activity(username, 'user', 'USER_LOGIN_FAILED', f'Failed login attempt for username: {username}')
                flash('Invalid username or password!', 'error')
                return redirect(url_for('login'))
                
        except mysql.connector.Error as error:
            flash(f'Error: {error}', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Dashboard (after login)
@app.route('/dashboard')
def dashboard():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    current_now = datetime.now()
    current_month_str = current_now.strftime('%Y-%m')

    # Zero defaults for new users with no data
    monthly_income = 0.0
    budget_limit = 0.0
    total_spent = 0.0
    remaining_budget = 0.0
    savings = 0.0
    spent_percentage = 0
    remaining_percentage = 0
    savings_percentage = 0
    category_data = []
    trend_labels = []
    trend_amounts = []
    expenses_history = []
    available_months = []
    has_real_data = False

    selected_month_str = current_month_str
    selected_month_name = current_now.strftime('%B %Y')

    # Attempt to query live database values
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Fetch only months that actually have recorded expenses (dynamic, excludes empty months)
        cursor.execute(
            """
            SELECT DISTINCT DATE_FORMAT(expense_date, '%Y-%m') as month_key,
                            DATE_FORMAT(expense_date, '%M %Y') as month_label
            FROM expenses
            WHERE user_id = %s
            ORDER BY month_key DESC
            """,
            (session['user_id'],)
        )
        available_months = cursor.fetchall()
        available_keys = [m['month_key'] for m in available_months]

        # Determine active month selection:
        # Priority: Requested month if valid -> Current month if it has data -> Latest month with data -> Current month
        requested_month = request.args.get('month')
        if requested_month and requested_month in available_keys:
            selected_month_str = requested_month
        elif current_month_str in available_keys:
            selected_month_str = current_month_str
        elif available_keys:
            selected_month_str = available_keys[0]
        elif requested_month:
            selected_month_str = requested_month
        else:
            selected_month_str = current_month_str

        try:
            selected_dt = datetime.strptime(selected_month_str, '%Y-%m')
            selected_month_name = selected_dt.strftime('%B %Y')
        except Exception:
            selected_month_name = selected_month_str

        # 2. Fetch budget for the selected month (fallback to latest budget if not specifically set for that month)
        cursor.execute(
            "SELECT monthly_income, budget_limit FROM budgets WHERE user_id = %s AND month_year = %s ORDER BY id DESC LIMIT 1",
            (session['user_id'], selected_month_str)
        )
        budget_row = cursor.fetchone()
        if not budget_row:
            cursor.execute(
                "SELECT monthly_income, budget_limit FROM budgets WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (session['user_id'],)
            )
            budget_row = cursor.fetchone()

        # 3. Fetch expenses by category for the SELECTED MONTH ONLY
        cursor.execute(
            """
            SELECT category, SUM(amount) as cat_total 
            FROM expenses 
            WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s 
            GROUP BY category
            """,
            (session['user_id'], selected_month_str)
        )
        cat_rows = cursor.fetchall()

        # 4. Fetch monthly spending trends (Multi-month line graph - remains completely unchanged)
        cursor.execute(
            """
            SELECT DATE_FORMAT(expense_date, '%b') as month_name,
                   SUM(amount) as month_total,
                   DATE_FORMAT(expense_date, '%Y-%m') as sort_key
            FROM expenses
            WHERE user_id = %s
            GROUP BY sort_key, month_name
            ORDER BY sort_key ASC
            LIMIT 6
            """,
            (session['user_id'],)
        )
        trend_rows = cursor.fetchall()

        # 5. Fetch expense history for the SELECTED MONTH ONLY
        cursor.execute(
            """
            SELECT id, category, amount, description, expense_date 
            FROM expenses 
            WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s 
            ORDER BY expense_date DESC, id DESC
            """,
            (session['user_id'], selected_month_str)
        )
        raw_expenses = cursor.fetchall()
        for exp in raw_expenses:
            e_date = exp['expense_date']
            date_str = e_date.strftime('%Y-%m-%d') if hasattr(e_date, 'strftime') else str(e_date)
            date_display = e_date.strftime('%b %d, %Y') if hasattr(e_date, 'strftime') else str(e_date)
            expenses_history.append({
                'id': exp['id'],
                'category': exp['category'],
                'amount': float(exp['amount']),
                'description': exp['description'] or '',
                'date_raw': date_str,
                'date_display': date_display
            })

        cursor.close()
        connection.close()

        if budget_row or cat_rows:
            has_real_data = True
            if budget_row:
                monthly_income = float(budget_row['monthly_income'])
                budget_limit = float(budget_row['budget_limit'])
            else:
                budget_limit = monthly_income

            if cat_rows:
                db_total_spent = sum(float(r['cat_total']) for r in cat_rows)
                total_spent = db_total_spent

                color_palette = {
                    'rent': '#2563eb',
                    'food': '#f97316',
                    'transportation': '#10b981',
                    'transport': '#10b981',
                    'entertainment': '#8b5cf6',
                    'utilities': '#f59e0b',
                    'utility': '#f59e0b',
                    'healthcare': '#ec4899',
                    'education': '#6366f1',
                    'shopping': '#06b6d4',
                    'other': '#64748b',
                    'others': '#64748b'
                }
                fallback_colors = ['#2563eb', '#f97316', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899', '#06b6d4', '#64748b']

                category_data = []
                for idx, r in enumerate(cat_rows):
                    c_name = r['category'].capitalize()
                    c_amt = float(r['cat_total'])
                    c_pct = round((c_amt / total_spent * 100)) if total_spent > 0 else 0
                    c_color = color_palette.get(r['category'].lower(), fallback_colors[idx % len(fallback_colors)])
                    category_data.append({
                        'name': c_name,
                        'color': c_color,
                        'pct': c_pct,
                        'amount': c_amt
                    })

            # Calculate Remaining & Savings for the selected month
            target_base = budget_limit if budget_row else monthly_income
            remaining_budget = max(0.0, target_base - total_spent)
            savings = max(0.0, monthly_income - total_spent)

            spent_percentage = round((total_spent / target_base * 100)) if target_base > 0 else 0
            remaining_percentage = max(0, 100 - spent_percentage)
            savings_percentage = round((savings / monthly_income * 100)) if monthly_income > 0 else 0

            if trend_rows and len(trend_rows) >= 2:
                trend_labels = [r['month_name'] for r in trend_rows]
                trend_amounts = [float(r['month_total']) for r in trend_rows]

    except Exception as e:
        print(f"Notice: Could not load dashboard data ({e})")

    return render_template(
        'dashboard.html',
        username=session.get('username', 'User'),
        monthly_income=monthly_income,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        savings=savings,
        spent_percentage=spent_percentage,
        remaining_percentage=remaining_percentage,
        savings_percentage=savings_percentage,
        category_data=category_data,
        trend_labels=trend_labels,
        trend_amounts=trend_amounts,
        expenses_history=expenses_history,
        available_months=available_months,
        selected_month_str=selected_month_str,
        selected_month_name=selected_month_name,
        has_real_data=has_real_data
    )

# Logout
@app.route('/logout')
def logout():
    if 'username' in session:
        log_activity(session.get('username'), session.get('role', 'user'), 'USER_LOGOUT', 'User logged out of client portal.', session.get('user_id'))
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# Add budget
@app.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        monthly_income = request.form['monthly_income']
        budget_limit = request.form['budget_limit']
        month_year = request.form['month_year']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Check if budget already exists for this specific month
            cursor.execute(
                "SELECT id FROM budgets WHERE user_id = %s AND month_year = %s ORDER BY id DESC LIMIT 1",
                (session['user_id'], month_year)
            )
            existing_budget = cursor.fetchone()

            if existing_budget:
                cursor.execute(
                    "UPDATE budgets SET monthly_income = %s, budget_limit = %s WHERE id = %s",
                    (monthly_income, budget_limit, existing_budget['id'])
                )
            else:
                cursor.execute(
                    "INSERT INTO budgets (user_id, monthly_income, budget_limit, month_year) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], monthly_income, budget_limit, month_year)
                )
            
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Budget saved successfully!', 'success')
            return redirect(url_for('dashboard', month=month_year))
            
        except Exception as error:
            flash(f'Error: {error}', 'error')
            return redirect(url_for('add_budget'))

    # Load all user budgets by month so changing target month dynamically populates expected income
    budgets_by_month = {}
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT month_year, monthly_income, budget_limit FROM budgets WHERE user_id = %s ORDER BY id ASC",
            (session['user_id'],)
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        for r in rows:
            if r.get('month_year'):
                budgets_by_month[r['month_year']] = {
                    'monthly_income': float(r['monthly_income']),
                    'budget_limit': float(r['budget_limit'])
                }
    except Exception as e:
        print(f"Notice: Could not load user budgets ({e})")

    default_month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    return render_template(
        'add_budget.html',
        username=session.get('username', 'User'),
        budgets_by_month=budgets_by_month,
        default_month=default_month
    )

# Add expense (with Rapid Log support)
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({'success': False, 'error': 'Session expired. Please login again.'}), 401
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    current_now = datetime.now()
    today_str = current_now.strftime('%Y-%m-%d')
    current_month_str = current_now.strftime('%Y-%m')

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            category = data.get('category')
            amount = data.get('amount')
            description = data.get('description', '')
            expense_date = data.get('expense_date') or today_str
        else:
            category = request.form.get('category')
            amount = request.form.get('amount')
            description = request.form.get('description', '')
            expense_date = request.form.get('expense_date') or today_str
        
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

        if not category or not amount or not expense_date:
            if is_ajax:
                return jsonify({'success': False, 'error': 'Please provide category, amount, and date.'}), 400
            flash('Please fill in all required fields!', 'error')
            return redirect(url_for('add_expense'))

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                raise ValueError("Amount must be greater than 0")
        except ValueError:
            if is_ajax:
                return jsonify({'success': False, 'error': 'Please enter a valid expense amount.'}), 400
            flash('Invalid amount value!', 'error')
            return redirect(url_for('add_expense'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(
                "INSERT INTO expenses (user_id, category, amount, description, expense_date) VALUES (%s, %s, %s, %s, %s)",
                (session['user_id'], category, amount_val, description, expense_date)
            )
            new_id = cursor.lastrowid
            connection.commit()

            # Recalculate monthly budget impact for current month
            cursor.execute(
                "SELECT budget_limit FROM budgets WHERE user_id = %s AND month_year = %s ORDER BY id DESC LIMIT 1",
                (session['user_id'], current_month_str)
            )
            b_row = cursor.fetchone()
            if not b_row:
                cursor.execute(
                    "SELECT budget_limit FROM budgets WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (session['user_id'],)
                )
                b_row = cursor.fetchone()
            budget_limit = float(b_row['budget_limit']) if b_row else 0.0

            cursor.execute(
                "SELECT SUM(amount) as total_spent FROM expenses WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s",
                (session['user_id'], current_month_str)
            )
            spent_row = cursor.fetchone()
            total_spent = float(spent_row['total_spent'] or 0.0) if spent_row else 0.0
            remaining_budget = max(0.0, budget_limit - total_spent)
            spent_pct = round((total_spent / budget_limit * 100)) if budget_limit > 0 else 0

            cursor.close()
            connection.close()

            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': 'Transaction logged successfully!',
                    'expense': {
                        'id': new_id,
                        'category': category,
                        'amount': amount_val,
                        'description': description,
                        'expense_date': expense_date
                    },
                    'budget_limit': budget_limit,
                    'total_spent': total_spent,
                    'remaining_budget': remaining_budget,
                    'spent_pct': min(100, spent_pct)
                })

            flash('Expense added successfully!', 'success')
            return redirect(url_for('add_expense'))
            
        except mysql.connector.Error as error:
            if is_ajax:
                return jsonify({'success': False, 'error': str(error)}), 500
            flash(f'Error: {error}', 'error')
            return redirect(url_for('add_expense'))

    # GET Request: Fetch today's expenses & live monthly budget numbers
    today_expenses = []
    budget_limit = 0.0
    total_spent = 0.0
    remaining_budget = 0.0
    spent_pct = 0

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Budget for current month
        cursor.execute(
            "SELECT budget_limit FROM budgets WHERE user_id = %s AND month_year = %s ORDER BY id DESC LIMIT 1",
            (session['user_id'], current_month_str)
        )
        b_row = cursor.fetchone()
        if not b_row:
            cursor.execute(
                "SELECT budget_limit FROM budgets WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (session['user_id'],)
            )
            b_row = cursor.fetchone()
        budget_limit = float(b_row['budget_limit']) if b_row else 0.0

        # 2. Total spent for current month
        cursor.execute(
            "SELECT SUM(amount) as total_spent FROM expenses WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s",
            (session['user_id'], current_month_str)
        )
        spent_row = cursor.fetchone()
        total_spent = float(spent_row['total_spent'] or 0.0) if spent_row else 0.0
        remaining_budget = max(0.0, budget_limit - total_spent)
        spent_pct = round((total_spent / budget_limit * 100)) if budget_limit > 0 else 0

        # 3. Expenses logged today
        cursor.execute(
            """
            SELECT id, category, amount, description, expense_date 
            FROM expenses 
            WHERE user_id = %s AND expense_date = %s 
            ORDER BY id DESC
            """,
            (session['user_id'], today_str)
        )
        raw_today = cursor.fetchall()
        for r in raw_today:
            today_expenses.append({
                'id': r['id'],
                'category': r['category'],
                'amount': float(r['amount']),
                'description': r['description'] or '',
                'expense_date': str(r['expense_date'])
            })

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Notice: Error loading add_expense data: {e}")

    return render_template(
        'add_expense.html',
        username=session.get('username', 'User'),
        today_str=today_str,
        today_expenses=today_expenses,
        budget_limit=budget_limit,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        spent_pct=min(100, spent_pct)
    )

# Edit expense (from dashboard)
@app.route('/edit_expense/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    category = request.form.get('category')
    amount = request.form.get('amount')
    description = request.form.get('description', '')
    expense_date = request.form.get('expense_date')
    
    if not category or not amount or not expense_date:
        flash('Please fill in all required fields!', 'error')
        return redirect(url_for('dashboard'))
        
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE expenses 
            SET category = %s, amount = %s, description = %s, expense_date = %s 
            WHERE id = %s AND user_id = %s
            """,
            (category, amount, description, expense_date, expense_id, session['user_id'])
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash('Expense updated successfully!', 'success')
    except mysql.connector.Error as error:
        flash(f'Error updating expense: {error}', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
        
    return redirect(request.referrer or url_for('dashboard'))

# Delete expense (from dashboard)
@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
        
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = %s AND user_id = %s",
            (expense_id, session['user_id'])
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash('Expense deleted successfully!', 'success')
    except mysql.connector.Error as error:
        flash(f'Error deleting expense: {error}', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
        
    return redirect(request.referrer or url_for('dashboard'))

# Reports and Exports View
@app.route('/reports')
def reports():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    current_now = datetime.now()
    current_month_str = current_now.strftime('%Y-%m')

    available_months = []
    selected_month_str = current_month_str
    selected_month_label = current_now.strftime('%B %Y')

    monthly_income = 0.0
    budget_limit = 0.0
    total_expenses = 0.0
    top_category = "None"
    top_category_amount = 0.0
    is_within_budget = True
    category_breakdown = []
    expenses_list = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Fetch available months with recorded expenses
        cursor.execute(
            """
            SELECT DISTINCT DATE_FORMAT(expense_date, '%Y-%m') as month_key,
                            DATE_FORMAT(expense_date, '%M %Y') as month_label
            FROM expenses
            WHERE user_id = %s
            ORDER BY month_key DESC
            """,
            (session['user_id'],)
        )
        available_months = cursor.fetchall()
        available_keys = [m['month_key'] for m in available_months]

        # Determine active month selection
        requested_month = request.args.get('month')
        if requested_month and requested_month in available_keys:
            selected_month_str = requested_month
        elif current_month_str in available_keys:
            selected_month_str = current_month_str
        elif available_keys:
            selected_month_str = available_keys[0]
        elif requested_month:
            selected_month_str = requested_month
        else:
            selected_month_str = current_month_str

        try:
            selected_dt = datetime.strptime(selected_month_str, '%Y-%m')
            selected_month_label = selected_dt.strftime('%B %Y')
        except Exception:
            selected_month_label = selected_month_str

        # 2. Fetch budget for this month (fallback to latest budget)
        cursor.execute(
            "SELECT monthly_income, budget_limit FROM budgets WHERE user_id = %s AND month_year = %s ORDER BY id DESC LIMIT 1",
            (session['user_id'], selected_month_str)
        )
        budget_row = cursor.fetchone()
        if not budget_row:
            cursor.execute(
                "SELECT monthly_income, budget_limit FROM budgets WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (session['user_id'],)
            )
            budget_row = cursor.fetchone()

        if budget_row:
            monthly_income = float(budget_row['monthly_income'])
            budget_limit = float(budget_row['budget_limit'])
        else:
            monthly_income = 0.0
            budget_limit = 0.0

        # 3. Fetch Category breakdown for selected month
        cursor.execute(
            """
            SELECT category, SUM(amount) as cat_total, COUNT(id) as count
            FROM expenses 
            WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s 
            GROUP BY category
            ORDER BY cat_total DESC
            """,
            (session['user_id'], selected_month_str)
        )
        cat_rows = cursor.fetchall()
        if cat_rows:
            total_expenses = sum(float(r['cat_total']) for r in cat_rows)
            top_category = cat_rows[0]['category']
            top_category_amount = float(cat_rows[0]['cat_total'])
            for r in cat_rows:
                c_amt = float(r['cat_total'])
                c_pct = round((c_amt / total_expenses * 100), 1) if total_expenses > 0 else 0
                category_breakdown.append({
                    'category': r['category'],
                    'amount': c_amt,
                    'count': r['count'],
                    'percentage': c_pct
                })

        # 4. Determine budget status
        target_budget = budget_limit if budget_limit > 0 else monthly_income
        if target_budget > 0:
            is_within_budget = total_expenses <= target_budget
        else:
            is_within_budget = total_expenses == 0.0

        # 5. Fetch all expenses for the selected month (for raw table and CSV/PDF export)
        cursor.execute(
            """
            SELECT id, category, amount, description, expense_date 
            FROM expenses 
            WHERE user_id = %s AND DATE_FORMAT(expense_date, '%Y-%m') = %s 
            ORDER BY expense_date DESC, id DESC
            """,
            (session['user_id'], selected_month_str)
        )
        raw_expenses = cursor.fetchall()
        for exp in raw_expenses:
            e_date = exp['expense_date']
            date_str = e_date.strftime('%Y-%m-%d') if hasattr(e_date, 'strftime') else str(e_date)
            expenses_list.append({
                'id': exp['id'],
                'date': date_str,
                'category': exp['category'],
                'description': exp['description'] or '',
                'amount': float(exp['amount'])
            })

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Notice: Error loading reports data: {e}")

    return render_template(
        'reports.html',
        username=session.get('username', 'User'),
        available_months=available_months,
        selected_month_str=selected_month_str,
        selected_month_label=selected_month_label,
        monthly_income=monthly_income,
        budget_limit=budget_limit,
        total_expenses=total_expenses,
        top_category=top_category,
        top_category_amount=top_category_amount,
        is_within_budget=is_within_budget,
        category_breakdown=category_breakdown,
        expenses_list=expenses_list
    )

# Settings View (Profile and Security)
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    active_tab = request.args.get('tab', 'profile')
    profile_updated = False
    password_updated = False

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            action = request.form.get('action')

            # 1. Update Profile Information
            if action == 'update_profile':
                active_tab = 'profile'
                full_name = request.form.get('full_name', '').strip()
                email = request.form.get('email', '').strip()
                contact_number = request.form.get('contact_number', '').strip()

                if not email:
                    flash('Email address cannot be empty!', 'error')
                else:
                    # Check if email is already taken by another user
                    cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
                    existing = cursor.fetchone()
                    if existing:
                        flash('That email address is already in use by another account.', 'error')
                    else:
                        cursor.execute(
                            "UPDATE users SET full_name = %s, email = %s, contact_number = %s WHERE id = %s",
                            (full_name, email, contact_number, user_id)
                        )
                        connection.commit()
                        profile_updated = True
                        flash('Profile changes saved successfully!', 'success')

            # 2. Update Password (Security)
            elif action == 'change_password':
                active_tab = 'security'
                current_password = request.form.get('current_password', '')
                new_password = request.form.get('new_password', '')
                confirm_password = request.form.get('confirm_password', '')

                if not current_password or not new_password or not confirm_password:
                    flash('Please fill in all password fields.', 'error')
                elif new_password != confirm_password:
                    flash('New password and confirm password do not match!', 'error')
                elif len(new_password) < 6:
                    flash('New password must be at least 6 characters long.', 'error')
                else:
                    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
                    user_record = cursor.fetchone()
                    if not user_record or not check_password_hash(user_record['password'], current_password):
                        flash('Current password is incorrect!', 'error')
                    else:
                        new_hashed = generate_password_hash(new_password)
                        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed, user_id))
                        connection.commit()
                        password_updated = True
                        flash('Password updated successfully!', 'success')

        # Fetch latest user data to pre-populate fields
        cursor.execute("SELECT id, username, full_name, email, contact_number FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        flash(f'Database error: {error}', 'error')
        user_data = None
    except Exception as e:
        flash(f'Error: {e}', 'error')
        user_data = None

    if not user_data:
        user_data = {
            'username': session.get('username', 'User'),
            'full_name': '',
            'email': '',
            'contact_number': ''
        }

    return render_template(
        'settings.html',
        username=session.get('username', 'User'),
        user=user_data,
        active_tab=active_tab,
        profile_updated=profile_updated,
        password_updated=password_updated
    )



import pickle
import numpy as np
import os
import json

# Global ML model and training metadata
ml_model = None
model_last_trained = "Never"
model_accuracy = "N/A"

def load_ml_model_and_metadata():
    global ml_model, model_last_trained, model_accuracy
    try:
        if os.path.exists('budget_model.pkl'):
            with open('budget_model.pkl', 'rb') as file:
                ml_model = pickle.load(file)
            mtime = os.path.getmtime('budget_model.pkl')
            model_last_trained = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Check for saved metadata if available
            if os.path.exists('model_metadata.json'):
                try:
                    with open('model_metadata.json', 'r') as mf:
                        m_data = json.load(mf)
                        model_accuracy = m_data.get('accuracy', 'N/A')
                        if 'timestamp' in m_data:
                            model_last_trained = m_data['timestamp']
                except Exception:
                    pass
            print("[INFO] ML model loaded successfully!")
        else:
            ml_model = None
            print("[WARNING] budget_model.pkl not found - prediction feature disabled")
    except Exception as e:
        ml_model = None
        print(f"[WARNING] Error loading ML model: {e}")

load_ml_model_and_metadata()

# Prediction page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    prediction_result = None
    risk_level = None
    confidence = None
    
    if request.method == 'POST':
        try:
            # Get user input
            income = float(request.form['income'])
            budget_limit = float(request.form['budget_limit'])
            days_passed = int(request.form['days_passed'])
            food_spent = float(request.form['food_spent'])
            transport_spent = float(request.form['transport_spent'])
            utilities_spent = float(request.form['utilities_spent'])
            entertainment_spent = float(request.form['entertainment_spent'])
            other_spent = float(request.form['other_spent'])
            
            # Calculate totals
            total_spent = food_spent + transport_spent + utilities_spent + entertainment_spent + other_spent
            percent_spent = (total_spent / budget_limit * 100) if budget_limit > 0 else 0
            
            # Prepare features for prediction (same order as training!)
            features = np.array([[
                income,
                budget_limit,
                days_passed,
                food_spent,
                transport_spent,
                utilities_spent,
                entertainment_spent,
                other_spent,
                total_spent,
                percent_spent
            ]])
            
            # Make prediction
            if ml_model is not None:
                prediction = ml_model.predict(features)[0]
                probabilities = ml_model.predict_proba(features)[0]
                
                # Get confidence
                confidence = max(probabilities) * 100
                
                # Determine risk level
                if prediction == 1:
                    prediction_result = "WILL OVERSPEND"
                    risk_level = "HIGH"
                else:
                    if percent_spent >= 80:
                        prediction_result = "SAFE (but close!)"
                        risk_level = "MEDIUM"
                    elif percent_spent >= 70:
                        prediction_result = "SAFE"
                        risk_level = "MEDIUM"
                    else:
                        prediction_result = "SAFE"
                        risk_level = "LOW"
                
                flash('Prediction completed!', 'success')
            else:
                flash('ML model not available!', 'error')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('predict.html',
                         username=session.get('username', 'User'),
                         prediction=prediction_result,
                         risk_level=risk_level,
                         confidence=confidence)

# ==========================================
# ADMINISTRATIVE CONTROL & RBAC MODULES
# ==========================================

# Admin Login Portal
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If already authenticated as admin, go directly to log module
    if session.get('role') == 'admin' and 'admin_id' in session:
        return redirect(url_for('admin_logs'))

    if request.method == 'POST':
        identifier = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash('Please provide both admin username/email and password.', 'error')
            return redirect(url_for('admin_login'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM admins WHERE username = %s OR email = %s LIMIT 1",
                (identifier, identifier)
            )
            admin = cursor.fetchone()
            cursor.close()
            connection.close()

            if admin and check_password_hash(admin['password'], password):
                # Establish dedicated Admin Session
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                session['admin_name'] = admin['full_name'] or admin['username']
                session['role'] = 'admin'

                log_activity(
                    admin['username'],
                    'admin',
                    'ADMIN_LOGIN',
                    f"Administrator '{admin['username']}' authenticated successfully.",
                    admin['id']
                )

                flash(f"Welcome to Admin Portal, {admin['full_name'] or admin['username']}!", 'success')
                return redirect(url_for('admin_logs'))
            else:
                log_activity(
                    identifier,
                    'unknown',
                    'ADMIN_LOGIN_FAILED',
                    f"Failed authentication attempt for identifier '{identifier}'."
                )
                flash('Invalid administrator credentials.', 'error')
                return redirect(url_for('admin_login'))

        except Exception as e:
            flash(f'Authentication error: {e}', 'error')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')


# Admin Logout Handler
@app.route('/admin/logout')
def admin_logout():
    admin_uname = session.get('admin_username')
    if admin_uname:
        log_activity(
            admin_uname,
            'admin',
            'ADMIN_LOGOUT',
            f"Administrator '{admin_uname}' signed out.",
            session.get('admin_id')
        )

    session.pop('admin_id', None)
    session.pop('admin_username', None)
    session.pop('admin_name', None)
    if session.get('role') == 'admin':
        session.pop('role', None)

    flash('Administrator signed out successfully.', 'success')
    return redirect(url_for('admin_login'))


# Restricted Admin Log Module View (Strict RBAC: 'admin' only)
@app.route('/admin/logs')
@admin_required
def admin_logs():
    search_query = request.args.get('q', '').strip()
    role_filter = request.args.get('role', '').strip()

    logs = []
    total_logs = 0
    admin_action_count = 0
    user_action_count = 0
    today_logs_count = 0

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Refresh admin display name in session from database
        admin_id = session.get('admin_id')
        if admin_id:
            cursor.execute("SELECT username, full_name FROM admins WHERE id = %s", (admin_id,))
            current_admin = cursor.fetchone()
            if current_admin:
                session['admin_name'] = current_admin['full_name'] or current_admin['username']
                session['admin_username'] = current_admin['username']

        # 1. Compute summary stats
        cursor.execute("SELECT COUNT(*) as total FROM activity_logs")
        total_logs = cursor.fetchone()['total'] or 0

        cursor.execute("SELECT COUNT(*) as admin_count FROM activity_logs WHERE user_role = 'admin'")
        admin_action_count = cursor.fetchone()['admin_count'] or 0

        cursor.execute("SELECT COUNT(*) as user_count FROM activity_logs WHERE user_role = 'user'")
        user_action_count = cursor.fetchone()['user_count'] or 0

        cursor.execute("SELECT COUNT(*) as today_count FROM activity_logs WHERE DATE(created_at) = CURDATE()")
        today_logs_count = cursor.fetchone()['today_count'] or 0

        # 2. Build filtered log query
        query = "SELECT * FROM activity_logs WHERE 1=1"
        params = []

        if role_filter:
            query += " AND user_role = %s"
            params.append(role_filter)

        if search_query:
            query += " AND (username LIKE %s OR action LIKE %s OR details LIKE %s OR ip_address LIKE %s)"
            like_term = f"%{search_query}%"
            params.extend([like_term, like_term, like_term, like_term])

        query += " ORDER BY id DESC LIMIT 200"

        cursor.execute(query, tuple(params))
        raw_logs = cursor.fetchall()

        for r in raw_logs:
            c_date = r['created_at']
            date_str = c_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(c_date, 'strftime') else str(c_date)
            logs.append({
                'id': r['id'],
                'username': r['username'],
                'user_role': r['user_role'],
                'action': r['action'],
                'details': r['details'] or '',
                'ip_address': r['ip_address'] or '127.0.0.1',
                'created_at': date_str
            })

        cursor.close()
        connection.close()

    except Exception as e:
        flash(f'Error retrieving audit logs: {e}', 'error')

    return render_template(
        'admin_logs.html',
        logs=logs,
        total_logs=total_logs,
        admin_action_count=admin_action_count,
        user_action_count=user_action_count,
        today_logs_count=today_logs_count,
        search_query=search_query,
        role_filter=role_filter,
        admin_username=session.get('admin_username', 'admin'),
        admin_name=session.get('admin_name', 'Administrator'),
        model_last_trained=model_last_trained,
        model_accuracy=model_accuracy
    )


# Restricted Admin Log Module API (Strict RBAC: 'admin' only)
@app.route('/admin/logs/api')
@admin_required
def admin_logs_api():
    logs = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM activity_logs ORDER BY id DESC LIMIT 500")
        raw_logs = cursor.fetchall()
        for r in raw_logs:
            c_date = r['created_at']
            logs.append({
                'id': r['id'],
                'username': r['username'],
                'user_role': r['user_role'],
                'action': r['action'],
                'details': r['details'] or '',
                'ip_address': r['ip_address'] or '127.0.0.1',
                'created_at': c_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(c_date, 'strftime') else str(c_date)
            })
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'count': len(logs), 'logs': logs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Admin Self-Service Settings & Password Change (Strict RBAC: 'admin' only)
@app.route('/admin/settings', methods=['POST'])
@admin_required
def admin_settings():
    admin_id = session.get('admin_id')
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_password or not new_password or not confirm_password:
        flash('Please fill in all password fields.', 'error')
        return redirect(url_for('admin_logs'))

    if new_password != confirm_password:
        flash('New password and confirm password do not match!', 'error')
        return redirect(url_for('admin_logs'))

    if len(new_password) < 6:
        flash('New password must be at least 6 characters long.', 'error')
        return redirect(url_for('admin_logs'))

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()

        if not admin or not check_password_hash(admin['password'], current_password):
            cursor.close()
            connection.close()
            flash('Current admin password is incorrect!', 'error')
            return redirect(url_for('admin_logs'))

        new_hashed = generate_password_hash(new_password)
        cursor.execute("UPDATE admins SET password = %s WHERE id = %s", (new_hashed, admin_id))
        connection.commit()
        cursor.close()
        connection.close()

        log_activity(
            admin['username'],
            'admin',
            'ADMIN_PASSWORD_UPDATED',
            f"Administrator '{admin['username']}' updated their password.",
            admin['id']
        )

        flash('Admin password updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating password: {e}', 'error')

    return redirect(url_for('admin_logs'))


# Administrative ML Re-Training Route (Strict RBAC: 'admin' only)
@app.route('/admin/train', methods=['POST'])
@admin_required
def admin_train_model():
    global ml_model, model_last_trained, model_accuracy
    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score

        dataset_path = 'budget_training_data.csv'
        if not os.path.exists(dataset_path):
            return jsonify({
                'success': False,
                'error': f"Training dataset '{dataset_path}' not found."
            }), 404

        # 1. Load training data
        df = pd.read_csv(dataset_path)

        # 2. Features and target
        features = [
            'income', 'budget_limit', 'days_passed', 'food_spent',
            'transport_spent', 'utilities_spent', 'entertainment_spent',
            'other_spent', 'total_spent', 'percent_spent'
        ]
        X = df[features]
        y = df['overspent']

        # 3. Train/Test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 4. Train RandomForest model
        new_model = RandomForestClassifier(n_estimators=100, random_state=42)
        new_model.fit(X_train, y_train)

        # 5. Evaluate accuracy
        y_pred = new_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        acc_pct = round(acc * 100, 2)
        acc_str = f"{acc_pct}%"

        # 6. Save model to disk
        with open('budget_model.pkl', 'wb') as f:
            pickle.dump(new_model, f)

        # 7. Update in-memory state & metadata
        ml_model = new_model
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model_last_trained = now_str
        model_accuracy = acc_str

        # Persist metadata for server restarts
        try:
            with open('model_metadata.json', 'w') as mf:
                json.dump({
                    'timestamp': model_last_trained,
                    'accuracy': model_accuracy,
                    'sample_count': len(df)
                }, mf, indent=2)
        except Exception as me:
            print(f"Notice: Failed to persist model metadata: {me}")

        # 8. Record audit activity log
        admin_username = session.get('admin_username', 'admin')
        admin_id = session.get('admin_id')
        log_activity(
            admin_username,
            'admin',
            'ML_MODEL_RETRAINED',
            f"Machine Learning model re-trained successfully. Accuracy: {acc_str}, Samples: {len(df)}.",
            admin_id
        )

        return jsonify({
            'success': True,
            'message': 'ML model re-trained and reloaded successfully!',
            'timestamp': model_last_trained,
            'accuracy': model_accuracy,
            'sample_count': len(df)
        })

    except Exception as e:
        admin_username = session.get('admin_username', 'admin')
        admin_id = session.get('admin_id')
        log_activity(
            admin_username,
            'admin',
            'ML_MODEL_RETRAIN_FAILED',
            f"Error during ML re-training: {str(e)}",
            admin_id
        )
        return jsonify({
            'success': False,
            'error': f"Failed to train model: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

