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
# File: db_accesss_interface.py
#
# Initialy created by Tran Duy Ngoan / March 2024
#
# This interface defines required methods to access TestResultWebapp' database.
#
# History:
#
# March 2024:
#  - initial version
#
# ******************************************************************************

from abc import ABCMeta, abstractmethod

class DBAccessInterface(object):
   """
Abstract base class defining the interface for database access.

This interface defines methods for connecting to and disconnecting from the database,
as well as methods for retrieving, creating, updating, and calling stored procedures
in the database.
   """

   __metaclass__ = ABCMeta
   @abstractmethod
   def connect(self):
      """
Connects to the database using the provided connection parameters.
      """
      pass

   @abstractmethod
   def disconnect(self):
      """
Disconnects from the database.
      """
      pass

   # Only used for DirectDBAccess which has a transaction 
   def commit(self):
      """
Commits a transaction (only applicable for DirectDBAccess with transaction support).
      """
      pass

   # Methods to retrieve (GET) information from database
   @abstractmethod
   def arGetCategories(self):
      """
Retrieves categories from the database.
      """
      pass

   @abstractmethod
   def bExistingResultID(self):
      """
Checks if the given result ID exists in the database.
      """
      pass

   @abstractmethod
   def sGetLatestFileID(self):
      """
Retrieves the latest file ID from the database.
      """
      pass

   # Methods to create new record(s) (POST) in database
   @abstractmethod
   def sCreateNewTestResult(self):
      """
Creates a new test result record in the database.
      """
      pass

   @abstractmethod
   def nCreateNewFile(self):
      """
Creates a new file record in the database.
      """
      pass

   @abstractmethod
   def vCreateNewHeader(self):
      """
Creates a new file header record in the database.
      """
      pass

   @abstractmethod
   def nCreateNewSingleTestCase(self):
      """
Creates a new single test case record in the database.
      """
      pass

   @abstractmethod
   def nCreateNewTestCase(self):
      """
Creates new test case(s) record in the database.
      """
      pass

   @abstractmethod
   def vCreateAbortReason(self):
      """
Creates a new abort reason record in the database.
      """
      pass

   @abstractmethod
   def vCreateCCRdata(self):
      """
Creates new CCR data in the database.
      """
      pass

   @abstractmethod
   def vCreateTags(self):
      """
Creates new tags in the database.
      """
      pass

   # Methods to update existing record (PUT) in database
   @abstractmethod
   def vCreateReanimation(self):
      """
Updates an existing test result with reanimation data in the database.
      """
      pass

   @abstractmethod
   def vSetCategory(self):
      """
Updates an existing test result with category information in the database.
      """
      pass

   @abstractmethod
   def vUpdateFileEndTime(self):
      """
Updates an existing file record with end time in the database.
      """
      pass

   @abstractmethod
   def vUpdateResultEndTime(self, *args, **kargv):
      """
Updates an existing test result record with end time in the database.
      """
      pass

   # Methods to call Stored Procedures of database
   @abstractmethod
   def vUpdateEvtbl(self):
      """
Calls a stored procedure to update event tables in the database.
      """
      pass

   @abstractmethod
   def vUpdateEvtbls(self):
      """
Calls a stored procedure to update event tables (plural) in the database.
      """
      pass

   @abstractmethod
   def vFinishTestResult(self):
      """
Calls a stored procedure to finish a test result in the database.
      """
      pass