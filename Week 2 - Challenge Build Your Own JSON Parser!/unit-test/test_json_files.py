import os
import unittest
from json_parser_tester.json_parser_tester import test_valid_json

class TestJsonFiles(unittest.TestCase):

    def setUp(self):
        # Define the folder containing your JSON files
        cwd = os.getcwd()
        # folder_name = 'test-files'
        folder_names = ['unit-test', 'test-files']
        self.folder_path = os.path.join(cwd, *folder_names)
    
    def test_print_json_files(self):

        # List all files in the directory
        files = os.listdir(self.folder_path)
        # print(files)
        
        # Filter out JSON files
        json_files = [f for f in files if f.endswith('.json')]
        # print(json_files)

        # TODO: Replace the reading of the Json file, with the actual
        # calling of the function here
        print("\n")

        for json_file in json_files:
            file_path = os.path.join(self.folder_path, json_file)
            
            # print("PATH: " + file_path)

            # send the file path
            # print("\n")

            print("JSonFile: " + json_file )
            print(test_valid_json(file_path))
            print("\n")

            # if json_file == "fail22.json" or json_file == "pass1.json":
            #     print(test_valid_json(file_path))
            #     print("\n")


            # with open(file_path, 'r') as f:
            #     print("FILE: " + json_file)
            #     print("====================================================")
            #     print(f.read())
            #     print("====================================================")
            #     print('\n\n')



if __name__ == '__main__':
    unittest.main()
    
