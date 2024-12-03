# problem1c_test.py - Tests for access control mechanism
from main import verify_access
from main import add_user, remove_user

def test_access_control():
    '''Test cases for the access control mechanism'''
    print("Starting access control tests...")
    
    # Test setup - create test users with different roles
    add_user("test_client", "Test@1234", "client")
    add_user("test_advisor", "Test@5678", "financial_advisor")
    add_user("test_planner", "Test@9012", "financial_planner")
    try:
        # Test client permissions
        print()
        assert verify_access("test_client", 1) == True, "Client should have access to view balance"
        print("test_client Test_1 PASSED")
        assert verify_access("test_client", 2) == True, "Client should have access to view portfolio"
        print("test_client Test_2 PASSED")
        assert verify_access("test_client", 4) == True, "Client should have access to view advisor contact"
        print("test_client Test_3 PASSED")
        try:
            verify_access("test_client", 3)
            assert False, "Client should not have access to modify portfolio"
        except PermissionError:
            print("test_client Test_4 PASSED")
         
        # Test financial advisor permissions
        print()
        assert verify_access("test_advisor", 1) == True, "Advisor should have access to view balance"
        print("test_advisor Test_1 PASSED")
        assert verify_access("test_advisor", 3) == True, "Advisor should have access to modify portfolio"
        print("test_advisor Test_2 PASSED")
        assert verify_access("test_advisor", 7) == True, "Advisor should have access to private info"
        print("test_advisor Test_3 PASSED")
        try:
            verify_access("test_advisor", 6)
            assert False, "Advisor should not have access to money market"
        except PermissionError:
            print("test_advisor Test_4 PASSED")
        
        # Test financial planner permissions
        print()
        assert verify_access("test_planner", 6) == True, "Planner should have access to money market"
        print("test_planner Test_1 PASSED")
        assert verify_access("test_planner", 7) == True, "Planner should have access to private info"
        print("test_planner Test_2 PASSED")
        assert verify_access("test_planner", 3) == True, "Planner should have access to modify portfolio"
        print("test_planner Test_3 PASSED")
        
        print("\nAccess control tests passed!")
        
    finally:
        # Cleanup test users
        remove_user("test_client")
        remove_user("test_advisor")
        remove_user("test_planner")

if __name__ == "__main__":
    test_access_control()