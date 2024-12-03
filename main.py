
import hashlib
import os

DATABASE_FILE_NAME = "passwd.txt"
COMMON_PASSWORDS_FILE_NAME = "common_passwords.txt"

# list of common passwords compiled from COMMON_PASSWORDS_FILE_NAME file
common_passwords = []

# dictionary mapping each function to its index
roles_perms_index = {
    1: "view_balance",
    2: "view_portfolio",
    3: "modify_portfolio",
    4: "view_advisor_contact",
    5: "view_planner_contact",
    6: "view_money_market",
    7: "view_private_info"
}

# dictionary mapping each role to its allowed function indexes
roles_perms = {
    "client": [1, 2, 4],
    "premium_client": [1, 2, 3, 4, 5],
    "financial_advisor": [1, 2, 3, 7],
    "financial_planner": [1, 2, 3, 6, 7],
    "teller": [1, 2, "limited_hours_access"]
}

# simulate a starting page
def _welcome_msg_() -> None:
    '''Displays the welcome message for the system.'''
    
    print("""
    justInvest System
    -----------------------------------

    Operations available on the system:

    1. View account balance
    2. View investment portfolio
    3. Modify investment portfolio
    4. View Financial Advisor contact info
    5. View Financial Planner contact info
    6. View money market instruments
    7. View private consumer instruments
    """)


def generate_salt() -> str:
    '''Generates a random salt for password hashing.'''
    return os.urandom(16).hex()


def hash_password(password: str, salt: str) -> str:
    '''Hashes a password using SHA-256 and the provided salt.'''

    if not password: raise ValueError("Password cannot be empty.")
    # hash the password using SHA256
    # add the password and salt and encode it before hashing to preserve all characters
    return hashlib.sha256((salt + password).encode()).hexdigest()


def verify_password(stored_password: str, stored_salt: str, input_password: str) -> bool:
    '''Verifies if the input password matches the stored password.'''

    if not stored_password or not stored_salt or not input_password: raise ValueError("All password inputs must be non-empty.")
    # the typed password in the client must be hashed with the salt value and check with the stored password in the server
    return stored_password == hash_password(input_password, stored_salt)


def authenticate_user(username: str, password: str) -> bool:
    '''Authenticates the user based on username and password.'''

    # check password validity
    if not is_valid_password(username, password):
        print("Password must be between 8 and 12 characters in length, contain one uppercase letter, one lowercase letter, one numerical digit, and one special character (!@#$%*&).")
        return False
    user = retrieve_user(username) # gets the user "object"

    if user is None:
        print("User does not exist.") 
        return False
        #raise LookupError("User does not exist.")
    # verify password with stored password, stored salt, and client typed password
    elif verify_password(user.get('password'), user.get('salt'), password): return True
    else: return False


def verify_access(username: str, func: int) -> bool:
    '''Checks if the user has access to the specified function.'''

    # get the user "object"
    user = retrieve_user(username)

    if user is None: raise LookupError("User not found.")

    role = user.get('role')

    if role is None: raise ValueError("Role not specified for the user.")
    # func is an int representation of an operation so look up in dictionary
    if func in roles_perms.get(role): return True
    else: raise PermissionError("Access denied for this operation.")


def is_username_taken(username: str) -> bool:
    '''Checks if the given username is already taken in the database file.'''

    # NOTE: data is stored as username:password:salt:role
    # loop through the text file to find the username
    with open(DATABASE_FILE_NAME, "r") as file:
        for line in file:
            # split all words by ":" to find username
            user_data = line.strip().split(":")
            if user_data[0] == username: return True
    return False

def is_valid_password(username: str, password: str) -> bool:
    '''Checks if the given password is valid and adheres to the following password policy:
    - Password must be between 8 and 12 characters in length
    - Password must include at least one uppercase letter
    - Password must include at least one lowercase letter
    - Password must include at least one numerical digit
    - Password must include at least one special character from the following: !, @, #, $, %, *, &
    - Password must NOT match the username
    - Password must NOT be a commonly used password
    '''

    within_bounds = False
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special = False
    not_matches_username = False
    not_common_password = False
    special_characters = "!@#$%*&"

    # check if password is between length 8 and 12
    if len(password) >= 8 and len(password) <= 12:
        within_bounds = True
    
    # loop through all characters in password to check each case
    for char in password:
        if char.isupper(): has_uppercase = True
        elif char.islower(): has_lowercase = True
        elif char.isdigit(): has_digit = True
        elif char in special_characters: has_special = True

    # true means it does NOT match the username
    if password != username: not_matches_username = True

    # is password in list of commonly used passwords
    if not (password in common_passwords): not_common_password = True

    return within_bounds and has_uppercase and has_lowercase and has_digit and has_special and not_matches_username and not_common_password

def add_user(username: str, password: str, role: str) -> None:
    '''Adds a new user to the database with the specified role.'''

    if is_username_taken(username): raise ValueError(f"Username '{username}' is already taken.")
    if not is_valid_password(username, password): raise ValueError("Password must be between 8 and 12 characters in length, contain one uppercase letter, one lowercase letter, one numerical digit, and one special character (!@#$%*&).")
    if role not in roles_perms: raise ValueError("Invalid role specified.")

    # since im making a new user, generate a new salt and hash the password using the salt
    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    # write the new data to the database (txt file)
    with open(DATABASE_FILE_NAME, "a") as file:
        # NOTE: data is stored as username:password:salt:role
        file.write(f"{username}:{hashed_password}:{salt}:{role}\n")
    # at this point a user has been succesfully written to the database

def remove_user(username: str) -> any:
    """Removes a user from the database by username.
    """
    
    # read the current file contents
    with open(DATABASE_FILE_NAME, "r") as file:
        lines = file.readlines()

    # find and remove the user entry
    user_found = False
    with open(DATABASE_FILE_NAME, "w") as file:
        for line in lines:
            if line.startswith(f"{username}:"):
                user_found = True
                continue  # skip writing this line back to file
            file.write(line)  # srite other lines back to the file

    # return a message if the user was not found
    if not user_found:
        return f"User '{username}' not found in database."

    return None

def retrieve_user(username: str) -> dict | None:
    '''Retrieves user details from the database by username.'''

    # loop through txt file to find username
    with open(DATABASE_FILE_NAME, "r") as file:
        for line in file:
            user_data = line.strip().split(":")
            # ill return the user data as a user "object" for ease of use
            if user_data[0] == username:
                return {
                    "username": user_data[0],
                    "password": user_data[1],
                    "salt": user_data[2],
                    "role": user_data[3]
                }
    # couldn't find the user; they dont exist
    return None


def main() -> None:
    '''Main function to run the system, allowing users to log in or sign up. Also permits operations.'''
    
    while True:
        # just prints the really big text with all the options and welcome msg
        _welcome_msg_()
        option = input("Please enter 0 to LOGIN or enter 1 to SIGN UP: ")
        print("\nLogin selected.\n" if option == "0" else "\nSign up selected.\n")

        # NOTE: client-sided username and password. must be transmitted to the server
        username = input("Enter username: ")
        password = input("Enter password: ")

        # option 0 means login, option 1 means signup
        if option == "0":
            if not authenticate_user(username, password):
                print(f"\nFailed to authenticate {username}.\n")
                break
        else:
            role = input("Please select a valid role (client, premium_client, financial_advisor, financial_planner, teller): ")

            if role not in roles_perms: raise ValueError("Invalid role selected.")
            # call the function to write the data to the txt file
            add_user(username, password, role)

        print(f"\nACCESS GRANTED!\nWelcome {username} [{retrieve_user(username).get('role')}.]")
        # this basically just retrieves all the permitted operations in a list such as [1, 2, 4] for client
        valid_operations = roles_perms.get(retrieve_user(username).get('role'))
        # apply a map to turn all the int operations to str and then join the list
        print("Your authorized operations are:", ", ".join(map(str, valid_operations)), "\n")

        try: selected_operation = int(input("Which operation would you like to perform? "))
        except ValueError: raise ValueError("Operation must be an integer.")

        # simulation of validating an operation
        if verify_access(username, selected_operation): print("\nOPERATION PERMITTED")
        else: print(f"\n{username} does not have permission to perform this operation.")

        # this ends the simulation
        print("\n$$$end$$$")
        break


if __name__ == "__main__":
    # add all the common passwords in this list to verify when needed
    with open(COMMON_PASSWORDS_FILE_NAME, "r") as file:
        for line in file:
            password = line.strip()
            common_passwords.append(password)
    main()