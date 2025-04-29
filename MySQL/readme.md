# MySQL SQL Injection CTF Challenge

Welcome to the **MySQL SQL Injection Capture The Flag (CTF)** challenge. In this challenge, you'll test and sharpen your skills in identifying and exploiting SQL injection vulnerabilities across 3 levels of increasing difficulty. The objective is to find the flag hidden within the application at each level.

## Setup Instructions

1. **Clone this repository:**
    ```
    git clone <repository-url>
    ```

2. **Install dependencies:**
    - You need Python 3.6 or higher.
    - Install the necessary libraries using:
      ```
      pip install -r requirements.txt
      ```

3. **Database Setup:**
    - Each level has its own SQL schema stored in the `schema/` directory.
    - Run the respective `levelX.sql` file to set up the database.

4. **Running the Application:**
    - Run the Flask app:
      ```
      python app.py
      ```

5. **Access the application:**
    - Open your browser and go to `http://127.0.0.1:5000`.

## Levels Overview

### 🔎 **Level 1: Blind SQL Injection**
- In this level, the goal is to perform a blind SQL injection. You'll need to deduce the existence of users based on subtle changes in the application’s responses. 
- **Hint:** Use boolean conditions to infer whether data exists.

### 🔐 **Level 2: Login Bypass via SQL Injection**
- This level presents a login form vulnerable to SQL injection. The goal is to bypass the login form by manipulating the query to authenticate as an admin user.
- **Hint:** Try using `' OR '1'='1` style SQL injections to bypass authentication.

### 🕵️ **Level 3: Union-based SQL Injection + Enumeration**
- In this level, you'll use a search form that is vulnerable to union-based SQL injection. The goal is to retrieve data from a hidden table containing the flag by exploiting the `UNION SELECT` technique.
- **Hint:** You'll need to determine the correct number of columns and enumerate tables to find the flag.

## Flags

- Level 1 Flag: Hidden within the database, can be inferred after successful exploitation.
- Level 2 Flag: Revealed after logging in as admin using SQL injection.
- Level 3 Flag: Hidden in the `hidden_data` table, retrievable via Union-based SQL injection.

## License

This project is created for educational purposes only. Do not use it for malicious activities.

Happy hacking! 🎯