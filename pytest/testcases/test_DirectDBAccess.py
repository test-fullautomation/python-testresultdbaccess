import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
# from TestResultDBAccess.DBAccess import DirectDBAccess
import TestResultDBAccess.DBAccess.direct_db_accesss

class Cursor:
   def __init__(self):
      pass
   
   def execute(self, command, values):
      return "cur:execute"

   def executemany(self, command, values):
      return "cur:executemany"

   def fetchall(self):
      return "cur:fetchall"

   @property
   def lastrowid(self):
      return "cur:lastrowid"

   def close(self):
      return "cur:close"

class Connection:
   def __init__(self, *args, **kwagv):
      pass

   def autocommit(self, bool):
      return "con:autocommit"

   def commit(self):
      return "con::commit"

   def close(self):
      return "con:close"

   def cursor(self):
      return Cursor()

class MockDB:
   def __init__(self):
      pass

   def connect(self, *args, **kwagv):
      return Connection(*args, **kwagv)

class Test_DirectDBAccess:

   @pytest.fixture
   def db_access(self):
      TestResultDBAccess.DBAccess.direct_db_accesss.db = MockDB
      db_access = TestResultDBAccess.DBAccess.direct_db_accesss.DirectDBAccess()
      return db_access

   def test_connect(self, db_access):
      db_access.connect("host", "user", "password", "db")

   def test_commit(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.commit()

   def test_disconnect(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.disconnect()

   def test_cleanAllTables(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.cleanAllTables()

   def test_sCreateNewTestResult(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.sCreateNewTestResult("project", "variant", "branch", "result_id",
            "interpretation", "time_start", "end_time", "version_sw",
            "version_test", "version_hw", "jenkins_url", "qualitygate"
         )

   def test_nCreateNewFile(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.nCreateNewFile("name", "tester", "machine",  "time_start", 
            "end_time", "result_id", "origin"
         )

   def test_vCreateNewHeader(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vCreateNewHeader("file_id", "testtoolname", "testtoolver",  
            "projectname", "encoding", "pythonver", "testfile", "logfilepath", 
            "logfilemode", "ctrfilepath", "configfile", "confname", "author",
            "project", "filedate", "vermajor", "vermonir", "verpatch", "keyword",
            "shortdesc", "user", "computer", "document", "environment", "configname",
            "configdata", "filter", "parameters"
         )

   def test_nCreateNewSingleTestCase(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.nCreateNewSingleTestCase("name", "issue", "tcid",  "fid", "testnumber",
            "repeatcount", "component", "start_time", "result_main",
            "result_state", "result_return", "reset_counter", "lastlog",
            "result_id", "file_id"
         )

   def test_nCreateNewTestCase(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.nCreateNewTestCase("name", "issue", "tcid",  "fid", "testnumber",
            "repeatcount", "component", "start_time", "result_main",
            "result_state", "result_return", "reset_counter", "lastlog",
            "result_id", "file_id"
         )

   def test_vCreateTags(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vCreateTags("result_id", "result_tag")

   def test_vSetCategory(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vSetCategory("result_id", "result_category")

   def test_vUpdateStartEndTime(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vUpdateStartEndTime("result_id", "start_time", "end_time")

   def test_arGetCategories(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.arGetCategories()

   def test_vCreateAbortReason(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vCreateAbortReason("result_id", "reason", "message")

   def test_vCreateReanimation(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vCreateReanimation("result_id", "reanimation")

   def test_vCreateCCRdata(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vCreateCCRdata("testcase_id", [[1,2,3], [4,5,6]])

   def test_vFinishTestResult(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vFinishTestResult("result_id")

   def test_vUpdateEvtbls(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vUpdateEvtbls()

   def test_vUpdateEvtbl(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vUpdateEvtbl("result_id")

   def test_vEnableForeignKeyCheck(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vEnableForeignKeyCheck()

   def test_sGetLatestFileID(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.sGetLatestFileID("result_id")

   def test_vUpdateFileEndTime(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vUpdateFileEndTime("file_id", "end_time")

   def test_vUpdateResultEndTime(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.vUpdateResultEndTime("result_id", "end_time")

   def test_bExistingResultID(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.bExistingResultID("result_id")

   def test_arGetProjectVersionSWByID(self, db_access):
      db_access.connect("host", "user", "password", "db")
      db_access.arGetProjectVersionSWByID("result_id")

if __name__=="__main__":
   pytest.main([__file__])