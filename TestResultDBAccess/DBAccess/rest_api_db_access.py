#  Copyright 2020-2024 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
#
# File: rest_api_db_access.py
#
# Initialy created by Tran Duy Ngoan / March 2024
#
# This class provides methods to interact with TestResultWebApp's REST APIs.
#
# History:
#
# March 2024:
#  - initial version
#
# ******************************************************************************

import requests
from .db_accesss_interface import DBAccessInterface
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
import ssl
import tempfile

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

class RestApiDBAccess(DBAccessInterface):
   """
RestApiDBAccess class provide methods to interact with TestResultWebApp's REST 
APIs.

This class implements the **DBAccessInterface** and extends it.
It includes methods for connecting to the database, handling API requests, 
creating, updating, and calling stored procedures in the database via RESTful 
API calls. 
   """

   def __init__(self):
      """
Initializes the RestApiDBAccess instance.
      """
      self.session  = requests.Session()
      self.base_url = ""
      self.session.headers = {
         "Content-Type": "application/json"
      }
      self.cookies = {}
      self.certs_file = self.get_certs_file()

      if self.certs_file:
         self.session.verify = self.certs_file
      else:
         self.session.verify = False
   
   def get_certs_file(self):
      """
Retrieves SSL certificates and saves them to a temporary file for request's 
verification.

**Returns:**

   / *Type*: str /

   The path to the temporary file containing SSL certificates.
      """
      context = ssl.create_default_context() 
      der_certs = context.get_ca_certs(binary_form=True) 
      pem_certs = [ssl.DER_cert_to_PEM_cert(der) for der in der_certs] 
      if len(pem_certs):
         with tempfile.NamedTemporaryFile(mode='w', delete=False) as outfile: 
            path2pem = outfile.name
            for pem in pem_certs:
               outfile.write("{}\n".format(pem))

         return path2pem
      else:
         return None

   @staticmethod
   def encrypt_password(password, pubkey):
      """
Encrypts a password using a public key.

**Arguments:**

*  ``password``

   / *Type*: str /
   
   The password to encrypt.

*  ``pubkey``

   / *Type*: str /
   
   The public key used for encryption.

**Returns:**

   / *Type*: str /

   The encrypted password.
      """
      from cryptography.hazmat.primitives import serialization, hashes
      from cryptography.hazmat.primitives.asymmetric import padding
      from cryptography.hazmat.backends import default_backend
      from base64 import b64encode

      try:
         keyPub = serialization.load_pem_public_key(pubkey.encode('utf-8'), 
                                                    backend=default_backend())
         encypted_Data = keyPub.encrypt(
            password.encode('utf-8'),
            padding.PKCS1v15()
         )
         return b64encode(encypted_Data).decode('utf-8', errors='ignore')
      except Exception as error:
         raise Exception("Cannot encrypt given password with public key. Reason: {}".format(error))

   # Methods to handle api request
   def __get_request(self, resource):
      """
Sends a GET request to the API endpoint specified by the resource.

**Arguments:**

*  ``resource``

   / *Condition*: required / *Type*: str /

   The resource endpoint to send the GET request to.

**Returns:**

   / *Type*: dict /

   The response data if the request is successful.
   Otherwise returns ``None``.
      """
      res = self.session.get("{}/{}".format(self.base_url, resource), 
                             allow_redirects=True)
      if res.status_code == 200 and res.json()['success']:
         return res.json()['data']
      else:
         # raise Exception(res.json()['message'])
         return None
   
   def __post_request(self, resource, payload=None):
      """
Sends a POST request to the API endpoint specified by the resource.

**Arguments:**

*  ``resource``

   / *Condition*: required / *Type*: str /

   The resource endpoint to send the POST request to.

*  ``payload``

   / *Condition*: optional / *Type*: bool / *Default*: None /

   The payload for POST request.

**Returns:**

   / *Type*: dict /

   The response data if the request is successful.
   Otherwise raise Exception with error message.
      """
      res = self.session.post("{}/{}".format(self.base_url, resource), 
                              json=payload, 
                              allow_redirects=True)
      if res.status_code == 201 and res.json()['success']:
         return res.json()['data']
      else:
         raise Exception(res.json()['message'])

   def __patch_request(self, resource, resource_id, payload=None):
      """
Sends a PATCH request to the API endpoint specified by the resource and its id.

**Arguments:**

*  ``resource``

   / *Condition*: required / *Type*: str /

   The resource endpoint to send the PATCH request to.

*  ``resource_id``

   / *Condition*: required / *Type*: str /

   The id of requesting resource.

*  ``payload``

   / *Condition*: optional / *Type*: bool / *Default*: None /

   The payload for PATCH request.

**Returns:**

   / *Type*: dict /

   The response data if the request is successful.
   Otherwise raise Exception with error message.
      """
      res = self.session.patch("{}/{}/{}".format(self.base_url, resource, resource_id), 
                               json=payload, allow_redirects=True)
      
      if res.status_code == 200 and res.json()['success']:
         return res.json()['data']
      else:
         raise Exception(res.json()['message'])

   def __get_wam_cookies(self):
      """
Try to obtain authentication to the REST API (behind an SSO system) via Kerberos.

This method sends a GET request to the '/loggedin' endpoint of the API using 
Kerberos authentication to obtain the necessary cookies for authentication. 

If the request is successful, the authorized session is reused for subsequent
 requests.

**Arguments:**

(*no arguments*)

**Returns:**

(*no returns*)
      """
      try:
         # Try with kerberos
         kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
         res = self.session.get("{}/loggedin".format(self.base_url), 
                                auth=kerberos_auth, allow_redirects=True)
         if res.status_code == 200:
            # Authorized session is reused for later requests
            return
      except Exception as err:
         raise Exception("Cannot access API server. Reason: {}".format(err))

   # Implementation of interface's methods
   #
   def connect(self, host, user, passwd, database, *args):
      """
Connects to the database via REST API using the provided credentials.

**Arguments:**

*  ``host``

   / *Condition*: required / *Type*: str /

   URL which is hosted the TestResultWebApp's REST APIs.

*  ``user``

   / *Condition*: required / *Type*: str /

   User name for database authentication.

*  ``passwd``

   / *Condition*: required / *Type*: str /

   User's password for database authentication.

*  ``database``

   / *Condition*: required / *Type*: str /

   Database name.

**Returns:**

(*no returns*)
      """
      self.base_url = "{}/{}".format(host, database)

      self.__get_wam_cookies()
      try:
         res = self.session.get("{}/getPubKey".format(self.base_url), 
                                allow_redirects=True)
         # print res.status_code
         pubkey = res.json()['pubKey']

      except Exception as err:
         raise Exception("Failed to get public key. Reason: {}".format(err))

      # Reponse payload with encrypted password
      req_body = {
         'usr': user,
         'pwd': self.encrypt_password(passwd, pubkey),
         'dom': '',
      }

      res = self.session.post("{}/login".format(self.base_url), allow_redirects=True, json=req_body)
      if res.json()['data'] == "login_success":
         print("  > Login successfully!")
      else:
         raise Exception('Login failed!')

   def disconnect(self):
      """
Disconnect from TestResultWebApp's database.

**Arguments:**

(*no arguments*)

**Returns:**

(*no returns*)
      """
      res = self.session.get(self.base_url+'/logout', allow_redirects=True)
      if res.status_code == 200:
         print("  > Logout successfully!")
      else:
         raise Exception('Logout failed!')

   # Methods to retrieve (GET) information from database
   def arGetCategories(self):
      """
Get existing categories.

**Arguments:**

(*no arguments*)

**Returns:**

*  ``arCategories``

   / *Type*: list /

   List of exsiting categories.
      """
      data = self.__get_request('categories')
      if data:
         return list(map(lambda item: item['category'],data))
      else:
         return []

   def bExistingResultID(self, result_id):
      """
Verify the given test result UUID is existing or not.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   Result UUID to be verified.

**Returns:**

   / *Type*: bool /

   True if given ``result_id`` is already existing.
      """
      data = self.__get_request('results/{}'.format(result_id))
      if data:
         return True
      return False

   def sGetLatestFileID(self, result_id=None):
      """
Get latest file ID of all result or given ``result_id``.

**Arguments:**

*  ``result_id``

   / *Condition*: optional / *Type*: str /

   Test result ID.
   If used, the latest file id of given ``result_id`` is returned.

**Returns:**

   / *Type*: int /

   Latest file ID.
      """
      request_url = 'files/last'
      if result_id:
         request_url = 'files/last?test_result_id={}'.format(result_id)
      data = self.__get_request(request_url)
      if data and ('id' in data) and data['id']:
         return data['id']
      else:
         raise Exception("Cannot get latest file_id")
   
   def arGetProjectVersionSWByID(self, result_id):
      """
Get the project and version_sw information of given ``result_id``

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   Result UUID to be get the information.

**Returns:**

*  / *Type*: tuple /

   None if test result UUID is not existing, else the tuple which contains 
   project and version_sw: (project, variant) is returned.
      """
      data = self.__get_request('results/{}'.format(result_id))
      if data:
         return (data['project'], data['version_sw_target'])
      return None

   # Methods to create new record(s) (POST) in database
   def sCreateNewTestResult(self, project, variant, branch, 
                                  result_id,
                                  result_interpretation,
                                  result_start_time,
                                  result_end_time,
                                  result_version_sw_target,
                                  result_version_sw_test,
                                  result_version_hw,
                                  result_build_url,
                                  result_report_qualitygate
                                  ):
      """
Creates a new test result.

**Arguments:**

*  ``project``

   / *Condition*: required / *Type*: str /

   Project information.

*  ``variant``

   / *Condition*: required / *Type*: str /

   Variant information.

*  ``branch``

   / *Condition*: required / *Type*: str /

   Branch information.

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

*  ``result_interpretation``

   / *Condition*: required / *Type*: str /

   Result interpretation.

*  ``result_start_time``

   / *Condition*: required / *Type*: str /

   Test result start time as format ``%Y-%m-%d %H:%M:%S``.

*  ``result_end_time``

   / *Condition*: required / *Type*: str /

   Test result end time as format ``%Y-%m-%d %H:%M:%S``.

*  ``result_version_sw_target``

   / *Condition*: required / *Type*: str /

   Software version information.

*  ``result_version_sw_test``

   / *Condition*: required / *Type*: str /

   Test version information.

*  ``result_version_hw``

   / *Condition*: required / *Type*: str /

   Hardware version information.

*  ``result_build_url``

   / *Condition*: required / *Type*: str /

   Link to the execution of test result (Jenkins, Gitlab CI/CD, ...).

*  ``result_report_qualitygate``

   / *Condition*: required / *Type*: str /

   Qualitygate information for reporting.

**Returns:**

*  ``result_id``

   / *Type*: str /

   ``test_result_id`` of new test result.
      """
      data_prj = self.__get_request('projects?project={}&variant={}&branch={}'.format(project, variant, branch))
      if not data_prj:
         req_prj = {
            "project": project,
            "variant": variant,
            "branch": branch
         }
         self.__post_request('projects', req_prj)
      
      req_result = {
         "test_result_id" : result_id,
         "project" : project,
         "variant" : variant,
         "branch" : branch,
         "time_start" : result_start_time,
         "time_end" : result_end_time,
         "version_sw_target" : result_version_sw_target,
         "version_sw_test" : result_version_sw_test,
         "version_hardware" : result_version_hw,
         "jenkinsurl" : result_build_url,
         "reporting_qualitygate" : result_report_qualitygate,
         "interpretation" : result_interpretation,
         "result_state" : "in progress"
      }
      self.__post_request('results', req_result)

      return result_id

   def nCreateNewFile(self, file_name,
                            file_tester_account,
                            file_tester_machine,
                            file_time_start,
                            file_time_end,
                            result_id,
                            file_origin="ROBFW"):
      """
Create new result file.

**Arguments:**

*  ``file_name``

   / *Condition*: required / *Type*: str /

   File name information.

*  ``file_tester_account``

   / *Condition*: required / *Type*: str /

   Tester account information.

*  ``file_tester_machine``

   / *Condition*: required / *Type*: str /

   Test machine information.

*  ``file_time_start``

   / *Condition*: required / *Type*: str /

   Test file start time as format ``%Y-%m-%d %H:%M:%S``.

*  ``file_time_end``

   / *Condition*: required / *Type*: str /

   Test file end time as format ``%Y-%m-%d %H:%M:%S``.

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result to which this result file belongs.

*  ``file_origin``

   / *Condition*: required / *Type*: str /

   Origin (test framework) of test file."

**Returns:**

   / *Type*: int /

   ID of new entry.
      """
      req_file = {
         "test_result_id" : result_id,
         "name" : file_name,
         "tester_account" : file_tester_account,
         "tester_machine" : file_tester_machine,
         "time_start" : file_time_start,
         "time_end" : file_time_end,
         "origin" : file_origin
      }
      data = self.__post_request('files', req_file)
      return data['id']

   def vCreateNewHeader(self, file_id,
                              testtoolconfiguration_testtoolname,
                              testtoolconfiguration_testtoolversionstring,
                              testtoolconfiguration_projectname,
                              testtoolconfiguration_logfileencoding,
                              testtoolconfiguration_pythonversion,
                              testtoolconfiguration_testfile,
                              testtoolconfiguration_logfilepath,
                              testtoolconfiguration_logfilemode,
                              testtoolconfiguration_ctrlfilepath,
                              testtoolconfiguration_configfile,
                              testtoolconfiguration_confname,
                           
                              testfileheader_author,
                              testfileheader_project,
                              testfileheader_testfiledate,
                              testfileheader_version_major,
                              testfileheader_version_minor,
                              testfileheader_version_patch,
                              testfileheader_keyword,
                              testfileheader_shortdescription,
                              testexecution_useraccount,
                              testexecution_computername,
                           
                              testrequirements_documentmanagement,
                              testrequirements_testenvironment,
                           
                              testbenchconfig_name,
                              testbenchconfig_data,
                              preprocessor_filter,
                              preprocessor_parameters ):
      """
Create a new result file header.

**Arguments:**

*  ``file_id``

   / *Condition*: required / *Type*: int /

   File ID information.

*  ``testtoolconfiguration_testtoolname``

   / *Condition*: required / *Type*: str /

   Test tool name.

*  ``testtoolconfiguration_testtoolversionstring``

   / *Condition*: required / *Type*: str /

   Test tool version.

*  ``testtoolconfiguration_projectname``

   / *Condition*: required / *Type*: str /

   Project name.

*  ``testtoolconfiguration_logfileencoding``

   / *Condition*: required / *Type*: str /

   Encoding of logfile.

*  ``testtoolconfiguration_pythonversion``

   / *Condition*: required / *Type*: str /

   Python version info.

*  ``testtoolconfiguration_testfile``

   / *Condition*: required / *Type*: str /

   Test file name.

*  ``testtoolconfiguration_logfilepath``

   / *Condition*: required / *Type*: str /

   Path to log file.

*  ``testtoolconfiguration_logfilemode``

   / *Condition*: required / *Type*: str /

   Mode of log file.

*  ``testtoolconfiguration_ctrlfilepath``

   / *Condition*: required / *Type*: str /

   Path to control file.

*  ``testtoolconfiguration_configfile``

   / *Condition*: required / *Type*: str /

   Path to configuration file.

*  ``testtoolconfiguration_confname``

   / *Condition*: required / *Type*: str /

   Configuration name.

*  ``testfileheader_author``

   / *Condition*: required / *Type*: str /

   File author.

*  ``testfileheader_project``

   / *Condition*: required / *Type*: str /

   Project information.

*  ``testfileheader_testfiledate``

   / *Condition*: required / *Type*: str /

   File creation date.

*  ``testfileheader_version_major``

   / *Condition*: required / *Type*: str /

   File major version.

*  ``testfileheader_version_minor``

   / *Condition*: required / *Type*: str /

   File minor version.

*  ``testfileheader_version_patch``

   / *Condition*: required / *Type*: str /

   File patch version.

*  ``testfileheader_keyword``

   / *Condition*: required / *Type*: str /

   File keyword.

*  ``testfileheader_shortdescription``

   / *Condition*: required / *Type*: str /

   File short description.

*  ``testexecution_useraccount``

   / *Condition*: required / *Type*: str /

   Tester account who run the execution.

*  ``testexecution_computername``

   / *Condition*: required / *Type*: str /

   Machine name which is executed on.

*  ``testrequirements_documentmanagement``

   / *Condition*: required / *Type*: str /

   Requirement management information.

*  ``testrequirements_testenvironment``

   / *Condition*: required / *Type*: str /

   Requirement environment information.

*  ``testbenchconfig_name``

   / *Condition*: required / *Type*: str /

   Testbench configuration name.

*  ``testbenchconfig_data``

   / *Condition*: required / *Type*: str /

   Testbench configuration data.

*  ``preprocessor_filter``

   / *Condition*: required / *Type*: str /

   Preprocessor filter information.

*  ``preprocessor_parameters``

   / *Condition*: required / *Type*: str /

   Preprocessor parameters definition.

**Returns:**

(*no returns*)
      """

      req_fileheader = {
         "file_id" : int(file_id),
         "testtoolconfiguration_testtoolname" : testtoolconfiguration_testtoolname,
         "testtoolconfiguration_testtoolversionstring" : testtoolconfiguration_testtoolversionstring,
         "testtoolconfiguration_projectname" : testtoolconfiguration_projectname,
         "testtoolconfiguration_logfileencoding" : testtoolconfiguration_logfileencoding,
         "testtoolconfiguration_pythonversion" : testtoolconfiguration_pythonversion,
         "testtoolconfiguration_testfile" : testtoolconfiguration_testfile,
         "testtoolconfiguration_logfilepath" : testtoolconfiguration_logfilepath,
         "testtoolconfiguration_logfilemode" : testtoolconfiguration_logfilemode,
         "testtoolconfiguration_ctrlfilepath" : testtoolconfiguration_ctrlfilepath,
         "testtoolconfiguration_configfile" : testtoolconfiguration_configfile,
         "testtoolconfiguration_confname" : testtoolconfiguration_confname,
         "testfileheader_author" : testfileheader_author,
         "testfileheader_project" : testfileheader_project,
         "testfileheader_testfiledate" : testfileheader_testfiledate,
         "testfileheader_version_major" : testfileheader_version_major,
         "testfileheader_version_minor" : testfileheader_version_minor,
         "testfileheader_version_patch" : testfileheader_version_patch,
         "testfileheader_keyword" : testfileheader_keyword,
         "testfileheader_shortdescription" : testfileheader_shortdescription,
         "testexecution_useraccount" : testexecution_useraccount,
         "testexecution_computername" : testexecution_computername,
         "testrequirements_documentmanagement" : testrequirements_documentmanagement,
         "testrequirements_testenvironment" : testrequirements_testenvironment,
         "testbenchconfig_name" : testbenchconfig_name,
         "testbenchconfig_data" : testbenchconfig_data,
         "preprocessor_parameters" : preprocessor_parameters,
         "preprocessor_filter" : preprocessor_filter
      }
      self.__post_request('fileheaders', req_fileheader)

   def nCreateNewSingleTestCase(self, case_name,
                                      case_issue,
                                      case_tcid,
                                      case_fid,
                                      case_testnumber,
                                      case_repeatcount,
                                      case_component,
                                      case_time_start,
                                      case_result_main,
                                      case_result_state,
                                      case_result_return,
                                      case_counter_resets,
                                      case_lastlog,
                                      result_id,
                                      file_id):
      """
Create single test case.

**Arguments:**

*  ``case_name``

   / *Condition*: required / *Type*: str /

   Test case name.

*  ``case_issue``

   / *Condition*: required / *Type*: str /

   Test case issue ID.

*  ``case_tcid``

   / *Condition*: required / *Type*: str /

   Test case ID (used for testmanagement tool).

*  ``case_fid``

   / *Condition*: required / *Type*: str /

   Test case requirement (function) ID.

*  ``case_testnumber``

   / *Condition*: required / *Type*: int /

   Order of test case in file.

*  ``case_repeatcount``

   / *Condition*: required / *Type*: int /

   Test case repeatition count.

*  ``case_component``

   / *Condition*: required / *Type*: str /

   Component which test case is belong to.

*  ``case_time_start``

   / *Condition*: required / *Type*: str /

   Test case start time as format ``%Y-%m-%d %H:%M:%S``.

*  ``case_result_main``

   / *Condition*: required / *Type*: str /

   Test case main result.

*  ``case_result_state``

   / *Condition*: required / *Type*: str /

   Test case completion state.

*  ``case_result_return``

   / *Condition*: required / *Type*: int /

   Test case result code (as integer).

*  ``case_counter_resets``

   / *Condition*: required / *Type*: int /

   Counter of target reset within test case execution.

*  ``case_lastlog``

   / *Condition*: required / *Type*: str /

   Traceback information when test case is failed.

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result to which this test case belongs.

*  ``file_id``

   / *Condition*: required / *Type*: int /

   ID of result file to which this test case belongs.

**Returns:**

   / *Type*: int /

   ID of new entry.
      """
      req_test = {
         "name"            : case_name,
         "issue"           : case_issue,
         "tcid"            : case_tcid,
         "fid"             : case_fid,
         "component"       : case_component,
         "time_start"      : case_time_start,
         "result_main"     : case_result_main,
         "result_state"    : case_result_state,
         "result_return"   : int(case_result_return),
         "counter_resets"  : int(case_counter_resets),
         "lastlog"         : case_lastlog,
         "testnumber"      : str(case_testnumber),
         "repeatcount"     : str(case_repeatcount),
         "test_result_id"  : result_id,
         "file_id"         : int(file_id)
      }
      data = self.__post_request('testcases', req_test)
      return data['id']

   def nCreateNewTestCase(self, *args):
      """
Alias for nCreateNewSingleTestCase, used in older import tools to import a bulk 
of test cases at once. 
      """
      return self.nCreateNewSingleTestCase(*args)

   def vCreateAbortReason(self, result_id,
                                abort_reason,
                                abort_message):
      """
Create abort reason entry.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

*  ``abort_reason``

   / *Condition*: required / *Type*: str /

   Abort reason.

*  ``abort_message``

   / *Condition*: required / *Type*: str /

   Detail message of abort.

**Returns:**

(*no returns*)
      """
      req_abort = {
         "test_result_id"  : result_id,
         "abort_reason"    : abort_reason,
         "msg_detail"      : abort_message
      }
      self.__post_request('aborts', req_abort)

   def vCreateCCRdata(self, test_case_id, lCCRdata):
      """
Create CCR data per test case.

**Arguments:**

*  ``_tbl_test_case_id``

   / *Condition*: required / *Type*: int /

   test case ID.

*  ``lCCRdata``

   / *Condition*: required / *Type*: list /

   list of CCR data.

**Returns:**

(*no returns*)
      """
      for row in lCCRdata:
         req_ccr = {
            "test_case_id" : test_case_id,
            "timestamp"    : row[0],
            "MEM_RSS"      : row[1],
            "CPU"          : row[2]
         }
         self.__post_request('ccrs', req_ccr)

   def vCreateTags(self, result_id, tags):
      """
Create tag entries.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

*  ``tags``

   / *Condition*: required / *Type*: str /

   User tags information.

**Returns:**

(*no returns*)
      """
      req_tag = {
         "test_result_id"  : result_id,
         "tags"            : tags
      }
      self.__post_request('userresults', req_tag)

   # Methods to update existing record (PATCH) in database
   def vCreateReanimation(self, result_id, num_of_reanimation):
      """
Create reanimation entry.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

*  ``num_of_reanimation``

   / *Condition*: required / *Type*: int /

   Counter of target reanimation during execution.

**Returns:**

(*no returns*)
      """
      req_reanimation = {
         "num_of_reanimation"  : num_of_reanimation
      }
      self.__patch_request('results', result_id, req_reanimation)

   def vSetCategory(self, result_id, category_main):
      """
Create category entry.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

*  ``category_main``

   / *Condition*: required / *Type*: str /

   Category information.

**Returns:**

(*no returns*)
      """
      req_category = {
         "category_main"  : category_main
      }
      self.__patch_request('results', result_id, req_category)

   def vUpdateFileEndTime(self, file_id, time_end):
      """
Update test file end time.

**Arguments:**

*  ``file_id``

   / *Condition*: required / *Type*: int /

   File ID to be updated.

*  ``time_end``

   / *Condition*: required / *Type*: str /

   File end time as format ``%Y-%m-%d %H:%M:%S``.

**Returns:**

(*no returns*)
      """
      req_endtime = {
         "time_end"  : time_end
      }
      self.__patch_request('files', file_id, req_endtime)

   def vUpdateResultEndTime(self, result_id, time_end):
      """
Update test result end time.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   Result UUID to be updated.

*  ``time_end``

   / *Condition*: required / *Type*: str /

   Result end time as format ``%Y-%m-%d %H:%M:%S``.

**Returns:**

(*no returns*)
      """
      req_endtime = {
         "time_end"  : time_end
      }
      self.__patch_request('results', result_id, req_endtime)

   def vFinishTestResult(self, result_id):
      """
Update state of given test result to "new report".

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

**Returns:**

(*no returns*)
      """
      req_finish_result = {
         "result_state"  : "new report"
      }
      self.__patch_request('results', result_id, req_finish_result)

   # Methods to call Stored Procedures of database
   def vUpdateEvtbl(self, result_id):
      """
Call ``update_evtbl`` stored procedure to update given ``result_id``.

**Arguments:**

*  ``result_id``

   / *Condition*: required / *Type*: str /

   UUID of test result.

**Returns:**

(*no returns*)
      """
      self.__patch_request('evtblresults', result_id)

   def vUpdateEvtbls(self):
      """
Call ``update_evtbls`` stored procedure.

**Arguments:**

(*no arguments*)

**Returns:**

(*no returns*)
      """
      self.__post_request('evtblresults')