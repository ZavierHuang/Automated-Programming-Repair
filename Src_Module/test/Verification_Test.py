import unittest

from Src_Module.src.Verification import Verification
from Util_Module.src.FileIO import FileIO
from Config import ROOT


class Verification_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.fileIO = FileIO()


if __name__ == '__main__':
    unittest.main()