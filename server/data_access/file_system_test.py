import unittest

from file_system import FileSystemRepo


class FileSystemRepoTestCases(unittest.TestCase):
    def test_FileSystemRepo_write_binary(self):
        file_path = 'test_write'
        test_data = b'test data'
        FileSystemRepo.write_binary(file_path, test_data)
        file = open('test_write', "rb")
        actual_data = file.read()

        file = open('golden_file/test_write', "rb")
        data = file.read()
        self.assertEqual(actual_data, data)

    def test_FileSystemRepo_read_binary(self):
        golden_file_path = 'golden_file/test_read'
        actual_data = FileSystemRepo.read_binary(golden_file_path)

        golden_file = open(golden_file_path, "rb")
        data = golden_file.read()

        self.assertEqual(actual_data, data)


if __name__ == '__main__':
    unittest.main()
