import json
import pytest
from pathlib import Path
from autoviron.core.failure_db import FailureDB

@pytest.fixture
def temp_db(tmp_path):
    # Mock the project root to be a temp dir
    return FailureDB(tmp_path)

def test_failure_db_init(temp_db):
    assert temp_db._cache == {}

def test_record_failure(temp_db):
    temp_db.record_failure("ModuleNotFoundError", "bs4", "Installed beautifulsoup4")
    
    resolutions = temp_db.get_resolutions("ModuleNotFoundError")
    assert len(resolutions) == 1
    assert resolutions[0]["message"] == "bs4"
    assert resolutions[0]["resolution"] == "Installed beautifulsoup4"

def test_record_failure_persistence(tmp_path):
    db1 = FailureDB(tmp_path)
    db1.record_failure("KeyError", "SECRET_KEY", "Injected secret")
    
    # Reload the DB to verify it reads from file
    db2 = FailureDB(tmp_path)
    resolutions = db2.get_resolutions("KeyError")
    assert len(resolutions) == 1
    assert resolutions[0]["message"] == "SECRET_KEY"
