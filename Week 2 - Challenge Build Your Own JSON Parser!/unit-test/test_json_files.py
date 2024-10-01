import os
import unittest
from json_parser_tester.json_parser_tester import test_valid_json

class TestJsonFiles(unittest.TestCase):

    def setUp(self):

        cwd = os.getcwd()
        folder_names = ['unit-test', 'test-files']
        self.folder_path = os.path.join(cwd, *folder_names)
    
    def test_print_json_files(self):

        # List all files in the directory
        files = os.listdir(self.folder_path)
        # print(files)
        
        # Filter out JSON files
        json_files = [f for f in files if f.endswith('.json')]

        print("\n")
        for json_file in json_files:
            file_path = os.path.join(self.folder_path, json_file)
            
            print("JSonFile: " + json_file )
            print(test_valid_json(file_path))
            print("\n")

if __name__ == '__main__':
    unittest.main()
    
