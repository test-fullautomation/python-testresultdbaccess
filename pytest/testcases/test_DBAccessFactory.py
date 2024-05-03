#  Copyright 2020-2023 Robert Bosch GmbH
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
# --------------------------------------------------------------------------------------------------------------
#
# File: test_DBAccessFactory.py
#
# Initialy created by Tran Duy Ngoan / May 2024
#
# --------------------------------------------------------------------------------------------------------------

import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from TestResultDBAccess import DBAccessFactory

# --------------------------------------------------------------------------------------------------------------

class Test_DBAccessFactory:
   """DBAccessFactory tests"""

   @pytest.mark.parametrize(
      "Description", ["Test DB Access Factory: Direct Access",]
   )
   def test_direct_access(self, Description):
      """pytest 'DBAccessFactory' for Direct Access"""
      oDBAccess = DBAccessFactory().create('db')
      assert type(oDBAccess).__name__ == 'DirectDBAccess'

   @pytest.mark.parametrize(
      "Description", ["Test DB Access Factory: REST API Access",]
   )
   def test_rest_api_access(self, Description):
      """pytest 'DBAccessFactory' for REST API Access"""
      oDBAccess = DBAccessFactory().create('rest')
      assert type(oDBAccess).__name__ == 'RestApiDBAccess'

   @pytest.mark.parametrize(
      "Description", ["Test DB Access Factory: invalid interface",]
   )
   def test_invalid_access(self, Description):
      """pytest 'DBAccessFactory' for invalid value of interface"""
      with pytest.raises(Exception):
         DBAccessFactory().create('invalidInterface')