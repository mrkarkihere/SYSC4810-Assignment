# problem2c_test.py - Tests for password file management
from main import generate_salt, hash_password, retrieve_user
from main import add_user, remove_user

def test_password_file():
    '''Test cases for password file management'''
    print("Starting password file tests...\n")
    
    try:
        # Test salt generation
        salt1 = generate_salt()
        salt2 = generate_salt()
        assert len(salt1) == 32, "Salt should be 32 characters (16 bytes hex)"
        print("test_password_file Test_1 PASSED")
        assert salt1 != salt2, "Generated salts should be unique"
        print("test_password_file Test_2 PASSED")
        
        # Test password hashing
        password = "Test@1234"
        salt = generate_salt()
        hash1 = hash_password(password, salt)
        hash2 = hash_password(password, salt)
        assert hash1 == hash2, "Same password and salt should produce same hash"
        print("test_password_file Test_3 PASSED")
        assert len(hash1) == 64, "SHA-256 hash should be 64 characters"
        print("test_password_file Test_4 PASSED")
        
        # Test user retrieval
        test_user = "test_retrieve"
        add_user(test_user, "Test@1234", "client")
        print("test_password_file Test_5 PASSED")
        user_data = retrieve_user(test_user)
        assert user_data is not None, "Should retrieve existing user"
        print("test_password_file Test_6 PASSED")
        assert user_data["username"] == test_user, "Retrieved username should match"
        print("test_password_file Test_7 PASSED")
        assert user_data["role"] == "client", "Retrieved role should match"
        print("test_password_file Test_8 PASSED")
        
        # Test non-existent user
        assert retrieve_user("nonexistent") is None, "Should return None for non-existent user"
        print("test_password_file Test_9 PASSED")
        
        print("\nPassword file tests passed!")
        
    finally:
        # Cleanup test user
        remove_user(test_user)

if __name__ == "__main__":
    test_password_file()