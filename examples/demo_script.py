import os
import time

# This script is designed to crash to demonstrate AutoViron's self-healing loop.
# It attempts to import a package that isn't installed by default.
try:
    import bs4
    print("✅ bs4 (BeautifulSoup) imported successfully!")
except ImportError:
    # AutoViron will intercept this, auto-install 'beautifulsoup4', and retry.
    raise

# It also relies on a missing environment variable.
print("Checking for SUPER_SECRET_KEY...")
time.sleep(1)

# This will trigger a KeyError if not set. AutoViron will catch this,
# ask you to input a value in the terminal, inject it, and retry!
secret = os.environ["SUPER_SECRET_KEY"]

print(f"✅ Success! Your secret key is: {secret}")
print("\n🎉 AutoViron has successfully self-healed this script!")
