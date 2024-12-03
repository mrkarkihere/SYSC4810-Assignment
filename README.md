# **justInvest System Assignment**  
This project is a user authentication and access control system for the justInvest company, implementing secure login, role-based access control, and a proactive password policy.

---

## **Table of Contents**
1. [Main Program](#main-program)
2. [Test Cases](#test-cases)
3. [Password Database File](#password-database-file)
4. [Common Passwords File](#common-passwords-file)

---

## **Main Program**  
To run the main program, navigate to the directory containing the `main.py` file and execute the following command:

```bash
python -m main
```

### **Alternative Commands**  
Depending on your operating system or Python version, you may need to use one of the following commands:

```bash
python3 -m main
```

or  

```bash
python -m main.py
```

Ensure you are in the correct directory before running the command.

---

## **Test Cases**  
All unit tests for verifying the functionality of each component are located in the `unit_tests` directory. To run the tests, use the following command:

```bash
python3 -m unit_tests.problem1c_test
```

If your system requires it, you can use `python` instead of `python3`:

```bash
python -m unit_tests.problem1c_test
```

Make sure to replace `problem1c_test.py` with the specific test file name if testing different components.

---

## **Password Database File**  
The `passwd.txt` file serves as the **database** for the system. It stores user information in the following format:

```plaintext
username:hashed_password:salt:role
```

### **Features:**  
- **Add User:** Automatically stores user credentials when a new user is created.  
- **Retrieve User:** Provides user details during login or other operations.  
- **Remove User:** Deletes user records when necessary.

For more details on the structure and usage, refer to the accompanying PDF report.

---

## **Common Passwords File**  
The `common_passwords.txt` file contains a list of commonly used passwords that are prohibited based on the following policy constraints:  

- Password length must be **between 8 and 12 characters**.  
- Passwords must include at least:  
  - **One uppercase letter**  
  - **One lowercase letter**  
  - **One numerical digit**  
  - **One special character** from the following: `! @ # $ % * &`

### **How to Update:**  
To add a new commonly used password:  
1. Open the `common_passwords.txt` file.  
2. Add the new password on a **new line**.  
3. Save the file.

**Note:** The system will automatically reject any password that matches an entry in this file during user sign-up.