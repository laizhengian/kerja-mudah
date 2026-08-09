import hashlib
import sys

def generate_key(hwid):
    key = hashlib.sha256(hwid.encode()).hexdigest()[:20].upper()
    return key

def main():
    print("=" * 50)
    print("  RepairShop License Key Generator")
    print("  (Keep this script secret!)")
    print("=" * 50)
    print()
    
    while True:
        hwid = input("Enter customer's HWID (or 'q' to quit): ").strip()
        if hwid.lower() == 'q':
            break
        if not hwid:
            print("HWID cannot be empty!")
            continue
        
        key = generate_key(hwid)
        print()
        print(f"  HWID: {hwid}")
        print(f"  KEY:  {key}")
        print()
        
        copy = input("Copy key to clipboard? (y/n): ").strip().lower()
        if copy == 'y':
            try:
                import pyperclip
                pyperclip.copy(key)
                print("Copied!")
            except ImportError:
                print("Install pyperclip for clipboard: pip install pyperclip")
                print(f"Key: {key}")
        print()

if __name__ == "__main__":
    main()
