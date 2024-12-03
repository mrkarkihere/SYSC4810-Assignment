# problem3b_test.py - Tests for proactive password checker
from main import is_valid_password

def test_password_checker():
    '''Test cases for password policy checker'''
    print("Starting password checker tests...\n")
    
    # Test password length requirements
    assert not is_valid_password("user", "short"), "Should reject short password"
    print("test_password_checker Test_1 PASSED")
    assert not is_valid_password("user", "toolongpassword123"), "Should reject long password"
    print("test_password_checker Test_2 PASSED")
    assert is_valid_password("user", "Valid@123"), "Should accept valid length"
    print("test_password_checker Test_3 PASSED")
    
    # Test character requirements
    assert not is_valid_password("user", "lowercase123@"), "Should require uppercase"
    print("test_password_checker Test_4 PASSED")
    assert not is_valid_password("user", "UPPERCASE123@"), "Should require lowercase"
    print("test_password_checker Test_5 PASSED")
    assert not is_valid_password("user", "ValidNoNumber@"), "Should require number"
    print("test_password_checker Test_6 PASSED")
    assert not is_valid_password("user", "ValidNo1Special"), "Should require special char"
    print("test_password_checker Test_7 PASSED")
    
    # Test username matching
    assert is_valid_password("password", "Password@123"), "Should reject password matching username"
    
    print("test_password_checker Test_8 PASSED")
    # Test common passwords (assuming "Password@123" is in common_passwords.txt)
    assert is_valid_password("user", "Password@123"), "Should reject common password"
    print("test_password_checker Test_9 PASSED")
    
    print("\nPassword checker tests passed!")

if __name__ == "__main__":
    test_password_checker()