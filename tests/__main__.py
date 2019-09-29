import sys

import trace
import unittest
from unittest import TestSuite

sys.path.append(".")
sys.path.append("../")

from tests.TestAppAuthorizer import TestAppAuthorizer

#
# def suite():
#     s = TestSuite()
#     s.addTest(TestAppAuthorizer)
#     return s


if __name__ == "__main__":
    unittest.main()
