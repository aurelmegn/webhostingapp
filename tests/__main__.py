import sys

import trace
import unittest
from unittest import TestSuite

sys.path.append(".")
sys.path.append("../")

from ftpserver.TestAppAuthorizer import TestAppAuthorizer
from src.controllers import TestIndex


#
# def suite():
#     s = TestSuite()
#     s.addTest(TestAppAuthorizer)
#     return s

# TestIndex
if __name__ == "__main__":
    unittest.main()
