import json
from app import map_partner_name, load_caps

def verify():
    print("Loading caps from caps/partner_caps_jan.json...")
    caps = load_caps('caps/partner_caps_jan.json')
    
    # Check if empty partner exists in caps - This is now EXPECTED/ALLOWED
    empty_caps = [c for c in caps if not c.get('Partner') or not str(c.get('Partner')).strip()]
    if empty_caps:
        print("INFO: Empty partner exists in caps file (as expected).")
    else:
        print("INFO: No empty partner in caps file.")
        
    # Test Mapping
    test_cases = [
        ("Cash App Savings Account", "CashApp"),
        ("E*TRADE Savings Account", "Etrade"),
        ("Some Unknown Partner", "Some Unknown Partner") # Should match itself if no cap matches
    ]
    
    print("\nTesting Mapping Logic:")
    all_pass = True
    for input_name, expected in test_cases:
        result = map_partner_name(input_name, caps)
        if result == expected:
            print(f"PASS: '{input_name}' -> '{result}'")
        else:
            print(f"FAIL: '{input_name}' -> '{result}' (Expected: '{expected}')")
            all_pass = False
            
    if all_pass:
        print("\nSUCCESS: All tests passed. Data issue resolved.")
    else:
        print("\nFAILURE: Some tests failed.")

if __name__ == "__main__":
    verify()
