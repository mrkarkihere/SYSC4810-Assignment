# problem4a_test.py - Tests for login interface
from main import authenticate_user, verify_password
from main import add_user, remove_user
from main import retrieve_user

def test_login():
    '''Test cases for login interface'''
    print("Starting login interface tests...")
    
    test_user = "test_login"
    test_pass = "Test@1234"
    
    try:
        # Add test user
        add_user(test_user, test_pass, "client")
        
        user_data = retrieve_user(test_user)
        print()
        # Test successful authentication
        assert authenticate_user(test_user, test_pass) == True, "Should authenticate valid credentials"
        print("test_login Test_1 PASSED")
        # Test password verification
        assert verify_password(user_data["password"], user_data["salt"], test_pass) == True, "Should verify correct password"
        print("test_login Test_2 PASSED")
        assert verify_password(user_data["password"], user_data["salt"], "WrongPass@1") == False, "Should reject wrong password"
        print("test_login Test_3 PASSED")
        
        # Test failed authentication
        assert not authenticate_user(test_user, "Wrong@1234"), "Should reject wrong password"
        print("test_login Test_4 PASSED")
        assert not authenticate_user("nonexistent", test_pass), "Should reject non-existent user"
        print("test_login Test_5 PASSED\n")
        
        print("Login interface tests passed!")
        
    finally:
        # Cleanup test user
        remove_user(test_user)

if __name__ == "__main__":
    test_login()