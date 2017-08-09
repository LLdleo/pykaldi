from __future__ import division
import os 
import unittest

from kaldi.matrix import *
from kaldi.util import *

from mixins import *

# TODO (VM):
# This tests make use of the filesystem
# However at the moment I am assuming a 
# Unix architecture (e.g., writing to /tmp).
# How to do a multi-platform setup?
class _TestWriters(AuxMixin):

    def test__init__(self):
        writer = self.getImpl() # call factory method
        self.assertIsNotNone(writer)
        self.assertFalse(writer.IsOpen())

        with self.assertRaises(Exception): 
            writer.Close()

        writer = self.getImpl(self.rspecifier)
        self.assertIsNotNone(writer)
        self.assertTrue(writer.IsOpen())
        self.assertTrue(writer.Close())

        with self.assertRaises(RuntimeError): 
            writer.Close()
        
        # Check that the file exists after closing the writer
        self.assertTrue(os.path.exists(self.filename))
        
    def testContextManager(self):
        obj = self.getExampleObj()

        with self.getImpl(self.rspecifier) as writer:
            writer.Write("myobj", obj)

        # Check writer is closed
        self.assertFalse(writer.IsOpen())

        # Check that the file exists after closing the writer
        self.assertTrue(os.path.exists(self.filename))

    def test__setitem__(self):
        obj = self.getExampleObj()
        with self.getImpl(self.rspecifier) as writer:
            writer["myobj"] = obj

        # Check writer is closed
        self.assertFalse(writer.IsOpen())

        # Check that the file exists after closing the writer
        self.assertTrue(os.path.exists(self.filename))

class TestVectorWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return Vector.new([1, 2, 3, 4, 5])

class TestMatrixWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return Matrix.new([[3, 5], [7, 11]])

class TestIntWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return 3

class TestFloatWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return 5.0

class TestBoolWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return True

class TestIntVectorWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return [5, 6, 7, 8]

class TestIntVectorVectorWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return [[5, 6, 7, 8], [9, 10, 11]]

class TestIntPairVectorWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return [(1, 2), (3, 4), (5, 6)]

class TestFloatPairVectorWriter(_TestWriters, unittest.TestCase):
    def getExampleObj(self):
        return [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]


if __name__ == '__main__':
    unittest.main()
