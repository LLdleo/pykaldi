from .options_ext import SimpleOptions, ParseOptions
from .kaldi_table import ReadScriptFile, WriteScriptFile
from ..matrix import Vector, Matrix
from ..feat import WaveData
from .iostream import *
from .fstream import *
from .sstream import *

################################################################################
# Sequential Readers
################################################################################

class _SequentialReaderBase(object):
    """Base class defining the common API for sequential table readers."""

    def __init__(self, rspecifier=None):
        """Initializes a new sequential table reader.

        If rspecifier is not None, also opens the specified table.

        Args:
            rspecifier(str): Kaldi rspecifier for reading the data.
        """
        super(_SequentialReaderBase, self).__init__()
        if rspecifier is not None:
            self.Open(rspecifier)

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.Done():
            raise StopIteration
        else:
            key, value = self.Key(), self.Value()
            self.Next()
            return key, value


class SequentialVectorReader(_SequentialReaderBase,
                             kaldi_table.SequentialVectorReader):
    """Python wrapper for
    kaldi::SequentialTableReader<KaldiObjectHolder<Vector<float>>>.

    This is a wrapper around the C extension type SequentialVectorReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    def next(self):
        key, value = super(SequentialVectorReader, self).next()
        return key, Vector.new(value)


class SequentialMatrixReader(_SequentialReaderBase,
                             kaldi_table.SequentialMatrixReader):
    """Python wrapper for
    kaldi::SequentialTableReader<KaldiObjectHolder<Matrix<float>>>.

    This is a wrapper around the C extension type SequentialMatrixReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    def next(self):
        key, value = super(SequentialMatrixReader, self).next()
        return key, Matrix.new(value)


class SequentialWaveReader(_SequentialReaderBase,
                          kaldi_table.SequentialWaveReader):
    """Python wrapper for kaldi::SequentialTableReader<WaveHolder>.

    This is a wrapper around the C extension type SequentialWaveReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    def next(self):
        key, value = super(SequentialWaveReader, self).next()
        wave = WaveData()
        wave.Swap(value)
        return key, wave


class SequentialIntReader(_SequentialReaderBase,
                          kaldi_table.SequentialIntReader):
    """Python wrapper for kaldi::SequentialTableReader<BasicHolder<int32>>.

    This is a wrapper around the C extension type SequentialIntReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialFloatReader(_SequentialReaderBase,
                            kaldi_table.SequentialFloatReader):
    """Python wrapper for kaldi::SequentialTableReader<BasicHolder<float>>.

    This is a wrapper around the C extension type SequentialFloatReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialDoubleReader(_SequentialReaderBase,
                             kaldi_table.SequentialDoubleReader):
    """Python wrapper for kaldi::SequentialTableReader<BasicHolder<double>>.

    This is a wrapper around the C extension type SequentialDoubleReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialBoolReader(_SequentialReaderBase,
                          kaldi_table.SequentialBoolReader):
    """Python wrapper for kaldi::SequentialTableReader<BasicHolder<bool>>.

    This is a wrapper around the C extension type SequentialBoolReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialIntVectorReader(_SequentialReaderBase,
                                kaldi_table.SequentialIntVectorReader):
    """Python wrapper for
    kaldi::SequentialTableReader<BasicVectorHolder<int32>>.

    This is a wrapper around the C extension type SequentialIntVectorReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialIntVectorVectorReader(
        _SequentialReaderBase,
        kaldi_table.SequentialIntVectorVectorReader):
    """Python wrapper for
    kaldi::SequentialTableReader<BasicVectorVectorHolder<int32>>.

    This is a wrapper around the C extension type
    SequentialIntVectorVectorReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialIntPairVectorReader(
        _SequentialReaderBase,
        kaldi_table.SequentialIntPairVectorReader):
    """Python wrapper for
    kaldi::SequentialTableReader<BasicPairVectorHolder<int32>>.

    This is a wrapper around the C extension type SequentialIntPairVectorReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass


class SequentialFloatPairVectorReader(
        _SequentialReaderBase,
        kaldi_table.SequentialFloatPairVectorReader):
    """Python wrapper for
    kaldi::SequentialTableReader<BasicPairVectorHolder<float>>.

    This is a wrapper around the C extension type
    SequentialFloatPairVectorReader.
    It provides a more Pythonic API by implementing the iterator protocol.
    """
    pass

################################################################################
# Random Access Readers
################################################################################

class _RandomAccessReaderBase(object):
    """Base class defining the common API for random access table readers."""
    def __init__(self, rspecifier=None):
        """Initializes a new random access table reader.

        If rspecifier is not None, also opens the specified table.

        Args:
            rspecifier(str): Kaldi rspecifier for reading the data.
        """
        super(_RandomAccessReaderBase, self).__init__()
        if rspecifier is not None:
            self.Open(rspecifier)

    def __enter__(self):
        return self

    def __contains__(self, key):
        return self.HasKey(key)

    def __getitem__(self, key):
        if self.HasKey(key):
            return self.Value(key)
        else:
            raise KeyError(key)


class RandomAccessVectorReader(_RandomAccessReaderBase,
                               kaldi_table.RandomAccessVectorReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<KaldiObjectHolder<Vector<float>>>.

    This is a wrapper around the C extension type RandomAccessVectorReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    def __getitem__(self, key):
        value = super(RandomAccessVectorReader, self).__getitem__(key)
        return Vector.new(value)


class RandomAccessMatrixReader(_RandomAccessReaderBase,
                               kaldi_table.RandomAccessMatrixReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<KaldiObjectHolder<Matrix<float>>>.

    This is a wrapper around the C extension type RandomAccessMatrixReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    def __getitem__(self, key):
        value = super(RandomAccessMatrixReader, self).__getitem__(key)
        return Matrix.new(value)


class RandomAccessWaveReader(_RandomAccessReaderBase,
                             kaldi_table.RandomAccessWaveReader):
    """Python wrapper for kaldi::RandomAccessTableReader<WaveHolder>.

    This is a wrapper around the C extension type RandomAccessWaveReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    def __getitem__(self, key):
        value = super(RandomAccessWaveReader, self).__getitem__(key)
        wave = WaveData()
        wave.Swap(value)
        return wave


class RandomAccessIntReader(_RandomAccessReaderBase,
                            kaldi_table.RandomAccessIntReader):
    """Python wrapper for kaldi::RandomAccessTableReader<BasicHolder<int32>>.

    This is a wrapper around the C extension type RandomAccessIntReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessFloatReader(_RandomAccessReaderBase,
                              kaldi_table.RandomAccessFloatReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<BasicHolder<float>>.

    This is a wrapper around the C extension type RandomAccessFloatReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessDoubleReader(_RandomAccessReaderBase,
                               kaldi_table.RandomAccessDoubleReader):
    """Python wrapper for kaldi::RandomAccessTableReader<BasicHolder<double>>.

    This is a wrapper around the C extension type RandomAccessDoubleReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessBoolReader(_RandomAccessReaderBase,
                             kaldi_table.RandomAccessBoolReader):
    """Python wrapper for kaldi::RandomAccessTableReader<BasicHolder<bool>>.

    This is a wrapper around the C extension type RandomAccessBoolReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessIntVectorReader(_RandomAccessReaderBase,
                                  kaldi_table.RandomAccessIntVectorReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<BasicVectorHolder<int32>>.

    This is a wrapper around the C extension type RandomAccessIntVectorReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessIntVectorVectorReader(
        _RandomAccessReaderBase,
        kaldi_table.RandomAccessIntVectorVectorReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<BasicVectorVectorHolder<int32>>.

    This is a wrapper around the C extension type
    RandomAccessIntVectorVectorReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessIntPairVectorReader(
        _RandomAccessReaderBase,
        kaldi_table.RandomAccessIntPairVectorReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<BasicPairVectorHolder<int32>>.

    This is a wrapper around the C extension type
    RandomAccessIntPairVectorReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass


class RandomAccessFloatPairVectorReader(
        _RandomAccessReaderBase,
        kaldi_table.RandomAccessFloatPairVectorReader):
    """Python wrapper for
    kaldi::RandomAccessTableReader<BasicPairVectorHolder<float>>.

    This is a wrapper around the C extension type
    RandomAccessFloatPairVectorReader.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass

################################################################################
# Random Access Mapped Readers
################################################################################

class _RandomAccessReaderMappedBase(object):
    """Base class defining the common API for random access mapped table
    readers."""
    def __init__(self, table_rspecifier=None, map_rspecifier=None):
        """Initializes a new random access mapped table reader.

        If rspecifier is not None, also opens the specified table.

        Args:
            rspecifier(str): Kaldi rspecifier for reading the data.
        """
        super(_RandomAccessReaderMappedBase, self).__init__()
        if table_rspecifier is not None and map_rspecifier is not None:
            self.Open(table_rspecifier, map_rspecifier)

    def __enter__(self):
        return self

    def __contains__(self, key):
        return self.HasKey(key)

    def __getitem__(self, key):
        if self.HasKey(key):
            return self.Value(key)
        else:
            raise KeyError(key)


class RandomAccessVectorReaderMapped(
        _RandomAccessReaderMappedBase,
        kaldi_table.RandomAccessVectorReaderMapped):
    """Python wrapper for
    kaldi::RandomAccessTableReaderMapped<KaldiObjectHolder<Vector<float>>>.

    This is a wrapper around the C extension type
    RandomAccessVectorReaderMapped.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    def __getitem__(self, key):
        value = super(RandomAccessVectorReaderMapped, self).__getitem__(key)
        return Vector.new(value)


class RandomAccessMatrixReaderMapped(
        _RandomAccessReaderMappedBase,
        kaldi_table.RandomAccessMatrixReaderMapped):
    """Python wrapper for
    kaldi::RandomAccessTableReaderMapped<KaldiObjectHolder<Matrix<float>>>.

    This is a wrapper around the C extension type
    RandomAccessMatrixReaderMapped.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    def __getitem__(self, key):
        value = super(RandomAccessMatrixReaderMapped, self).__getitem__(key)
        return Matrix.new(value)

class RandomAccessFloatReaderMapped(
        _RandomAccessReaderMappedBase,
        kaldi_table.RandomAccessFloatReaderMapped):
    """Python wrapper for
    kaldi::RandomAccessTableReaderMapped<BasicHolder<float>>.

    This is a wrapper around the C extension type RandomAccessFloatReaderMapped.
    It provides a more Pythonic API by implementing the __contains__ and
    __getitem__ methods.
    """
    pass

################################################################################
# Writers
################################################################################

class _WriterBase(object):
    """Base class defining the common API for table writers."""
    def __init__(self, wspecifier=None):
        """Initializes a new table writer.

        If wspecifier is not None, also opens the specified table.

        Args:
            wspecifier(str): Kaldi wspecifier for writing the data.
        """
        super(_WriterBase, self).__init__()
        if wspecifier is not None:
            self.Open(wspecifier)

    def __enter__(self):
        return self

    def __setitem__(self, key, value):
        self.Write(key, value)


class VectorWriter(_WriterBase, kaldi_table.VectorWriter):
    """Python wrapper for kaldi::TableWriter<KaldiObjectHolder<Vector<float>>>.

    This is a wrapper around the C extension type VectorWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class MatrixWriter(_WriterBase, kaldi_table.MatrixWriter):
    """Python wrapper for kaldi::TableWriter<KaldiObjectHolder<Matrix<float>>>.

    This is a wrapper around the C extension type MatrixWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class WaveWriter(_WriterBase, kaldi_table.WaveWriter):
    """Python wrapper for kaldi::TableWriter<WaveHolder>.

    This is a wrapper around the C extension type WaveWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class IntWriter(_WriterBase, kaldi_table.IntWriter):
    """Python wrapper for kaldi::TableWriter<BasicHolder<int32>>.

    This is a wrapper around the C extension type IntWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class FloatWriter(_WriterBase, kaldi_table.FloatWriter):
    """Python wrapper for kaldi::TableWriter<BasicHolder<float>>.

    This is a wrapper around the C extension type FloatWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class DoubleWriter(_WriterBase, kaldi_table.DoubleWriter):
    """Python wrapper for kaldi::TableWriter<BasicHolder<double>>.

    This is a wrapper around the C extension type DoubleWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class BoolWriter(_WriterBase, kaldi_table.BoolWriter):
    """Python wrapper for kaldi::TableWriter<BasicHolder<bool>>.

    This is a wrapper around the C extension type BoolWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class IntVectorWriter(_WriterBase, kaldi_table.IntVectorWriter):
    """Python wrapper for kaldi::TableWriter<BasicVectorHolder<int32>>.

    This is a wrapper around the C extension type IntVectorWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class IntVectorVectorWriter(_WriterBase, kaldi_table.IntVectorVectorWriter):
    """Python wrapper for kaldi::TableWriter<BasicVectorVectorHolder<int32>>.

    This is a wrapper around the C extension type IntVectorVectorWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class IntPairVectorWriter(_WriterBase, kaldi_table.IntPairVectorWriter):
    """Python wrapper for kaldi::TableWriter<BasicPairVectorHolder<int32>>.

    This is a wrapper around the C extension type IntPairVectorWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass


class FloatPairVectorWriter(_WriterBase, kaldi_table.FloatPairVectorWriter):
    """Python wrapper for kaldi::TableWriter<BasicPairVectorHolder<float>>.

    This is a wrapper around the C extension type FloatPairVectorWriter.
    It provides a more Pythonic API by implementing the __setitem__ method.
    """
    pass
