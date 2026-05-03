from autoviron.core.deps import get_package_name

def test_get_package_name_exact_match():
    assert get_package_name("fastapi") == "fastapi"
    assert get_package_name("pytest") == "pytest"

def test_get_package_name_alias_mapping():
    assert get_package_name("bs4") == "beautifulsoup4"
    assert get_package_name("cv2") == "opencv-python"
    assert get_package_name("PIL") == "Pillow"
    assert get_package_name("dotenv") == "python-dotenv"
    assert get_package_name("yaml") == "pyyaml"
