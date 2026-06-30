import json
from pathlib import Path


class FileManager:
    def __init__(self):
        self.file_path = Path(__file__).resolve().parent / "passwords.json"



    def write_files(self, informations, salt, crypted_test):

        data_base = {
            "accounts": informations,
            "salt": salt,
            "test": crypted_test,
        }

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data_base, file, ensure_ascii=False, indent=4)



    def read_files(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except(json.JSONDecodeError, FileNotFoundError):
            return {}


