from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Setup database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Users for Level 1
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, flag TEXT)''')
    c.execute('''INSERT OR IGNORE INTO users (id, username, flag) VALUES (1, 'admin', 'FLAG{Blind_SQLi_Success}')''')

    # Admins for Level 2
    c.execute('''CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, username TEXT, password TEXT, flag TEXT)''')
    c.execute('''INSERT OR IGNORE INTO admins (id, username, password, flag) VALUES (1, 'admin', 'password123', 'FLAG{Login_Bypass_Success}')''')

    # Hidden table for Level 3
    c.execute('''CREATE TABLE IF NOT EXISTS hidden_flags (id INTEGER PRIMARY KEY, secret_flag TEXT)''')
    c.execute('''INSERT OR IGNORE INTO hidden_flags (id, secret_flag) VALUES (1, 'FLAG{Union_Enumeration_Success}')''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/level1', methods=['GET', 'POST'])
def level1():
    hint = "💡 Hint: SQL Comments can help you... (like --)"
    flag = None
    if request.method == 'POST':
        username = request.form['username']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            query = f"SELECT flag FROM users WHERE username = '{username}'"
            c.execute(query)
            result = c.fetchone()
            if result:
                flag = result[0]
                session['level1'] = True
        except Exception as e:
            flag = None
        conn.close()
    return render_template('level1.html', hint=hint, flag=flag)

@app.route('/level2', methods=['GET', 'POST'])
def level2():
    if not session.get('level1'):
        return redirect(url_for('level1'))
    
    hint = "💡 Hint: ' OR '1'='1 works wonders..."
    flag = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            query = f"SELECT flag FROM admins WHERE username = '{username}' AND password = '{password}'"
            c.execute(query)
            result = c.fetchone()
            if result:
                flag = result[0]
                session['level2'] = True
        except Exception as e:
            flag = None
        conn.close()
    return render_template('level2.html', hint=hint, flag=flag)

@app.route('/level3', methods=['GET', 'POST'])
def level3():
    if not session.get('level2'):
        return redirect(url_for('level2'))
    
    hint = "💡 Hint: UNION SELECT... Find column count first!"
    flag = None
    records = []
    if request.method == 'POST':
        search = request.form['search']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
            c.execute(query)
            table_exists = c.fetchone()
            if not table_exists:
                c.execute('''CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
                c.execute('''INSERT INTO products (name, description) VALUES ('CyberDeck', 'A hacking laptop')''')
                conn.commit()
            
            query = f"SELECT name, description FROM products WHERE name LIKE '%{search}%'"
            c.execute(query)
            records = c.fetchall()

            # If successful union, also fetch hidden flags
            if 'UNION' in search.upper():
                c.execute("SELECT secret_flag FROM hidden_flags")
                hidden = c.fetchone()
                if hidden:
                    flag = hidden[0]
                    session['level3'] = True
        except Exception as e:
            pass
        conn.close()
    return render_template('level3.html', hint=hint, flag=flag, records=records)

@app.route('/flag')
def final_flag():
    if session.get('level3'):
        return render_template('flag.html')
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
