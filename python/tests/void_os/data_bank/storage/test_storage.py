import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestStorage(unittest.TestCase):

    def test_storage_1(self):
        """Storage MUST only insert into an input's relations."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_10(self):
        """The access program stored MUST give, as the sheet _stored, the records of _stored of the values whose positions lie between first and last, both included."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.10', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_11(self):
        """The access program inputs MUST give the relation _inputs, each input in the order it was first stored, its _values the number of its records of _stored, and its _file its file as storage.2 names it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.11', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_12(self):
        """A file system failure, or a file of the data bank the parser rejects, MUST end the access as keeping failed, its reason those words alone, naming no path."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.12', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_13(self):
        """The access program insert MUST, holding the lock, convert the values from the position equal to the number of values the input stores, and write the part."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.13', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_14(self):
        """The sheets the input's schema gives MUST be kept, at each insert, as the converter gives them, in the MTSV files _sheets.mtsv and _fields.mtsv in the data bank's folder, each replaced whole, the input's records replacing its earlier ones."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.14', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_15(self):
        """The access program names MUST give _sheets and _fields of every input stored, each input in the order it was first stored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.15', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_16(self):
        """An input the converter rejects MUST end the insert as non-conforming, nothing being stored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.16', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_17(self):
        """The access program folder MUST give the data bank's folder, as storage.23 decides it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.17', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_18(self):
        """A file storage replaces whole MUST be written beside it, at its name then the Value replace suffix, then renamed onto it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.18', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_19(self):
        """A file of the data bank that does not exist MUST be read as holding no record, and not as a file system failure."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.19', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_2(self):
        """Each input MUST be kept as one MTSV file at its name written as storage.25 writes it within the data bank's folder, then .mtsv."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_20(self):
        """A session or agent holding HT, LF, FF or CR MUST NOT be kept in _communicated, nothing being marked communicated to it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.20', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_21(self):
        """The access program relations MUST give the input's relations from its file, the records of the values at positions below the number of its records of _stored, each sheet name once, its records those of every part in the order appended."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.21', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_22(self):
        """The access program communicated MUST give the number of the input's values communicated to the session and agent, as _communicated keeps it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.22', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_23(self):
        """The data bank's folder MUST be the absolute path the environment variable the Value data bank variable names holds, where it holds one, and else the user's documents folder joined with the Value data bank folder."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.23', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_24(self):
        """The user's documents folder MUST be as PLATFORMDIRS gives it for the platform, from the user's home folder."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.24', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_25(self):
        """An input's name MUST be written within the data bank's folder as name within a folder writes it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.25', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_26(self):
        """A value's time and event MUST be kept only in _stored, beside it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.26', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_3(self):
        """A part MUST be written at the end of its input's file, the file opened for appending, its sheets in the file's order, a sheet's name repeating as MTSV permits."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_4(self):
        """Each value MUST be stored with all its records or with none: a value is stored whole once its record of _stored is written, after the part, and the records of a value at or after the number of the input's records of _stored are cut from the input's file before the next part is written."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_5(self):
        """The relation _communicated MUST be kept as the MTSV file _communicated.mtsv in the data bank's folder, replaced whole as storage.18 replaces a file."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_6(self):
        """One process at a time MUST write: before writing, a lock file named _lock is created in the data bank's folder only where it does not exist, and removed after; a process that finds it waits the Value lock wait and tries again, and takes a lock older than the Value lock timeout as released."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_7(self):
        """The number of an input's values communicated to a session and agent MUST be kept in _communicated, an input with no record for them having none communicated to them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.7', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_8(self):
        """Each value stored whole MUST have one record in _stored, its _time the time it was stored, in UTC, written as RFC 3339 writes a date and time with the offset Z, and its _event the event handed, the relation kept as the MTSV file _stored.mtsv in the data bank's folder, written at its end, as storage.3 writes a part."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.8', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_storage_9(self):
        """The value a source sends MUST be stored as it is sent."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('storage.9', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
