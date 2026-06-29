from FileManager import FileManager
import Encryption
import re
import os


class AccountManager:
    def __init__(self):
        self.file_manager = FileManager()
        self.data = self.file_manager.read_files()
        self.accounts = self.get_info()
        self.salt = self.find_salt()
        self.cipher_suite = None
        self.test = self.find_test()

    def get_info(self):
        if self.data:
            return self.data["accounts"]
        
        return {}
    


    def is_there_password(self):
        return self.data
    

    def find_test(self):
        if self.data:
            return self.data["test"]
        
        return None

    def set_main_password(self, main_password):
        key = Encryption.convert_password_to_key(main_password, self.salt)
        self.cipher_suite = Encryption.Fernet(key)
        self.test = Encryption.encrypt_password("Test", self.cipher_suite)



    def check_password(self, password):
        try:
            key = Encryption.convert_password_to_key(password, self.salt)
            cipher_suite = Encryption.Fernet(key)
            Encryption.decrypt_password(self.test, cipher_suite)
            self.cipher_suite = cipher_suite
            self.dectypt_accounts()
            return True
        
        except Exception as e:
            return False




    def end_program(self):
        if self.cipher_suite:
            self.encrypt_accounts()
            self.file_manager.write_files(self.accounts, Encryption.base64.b64encode(self.salt).decode('utf-8'), self.test)


    def find_salt(self):
        if not self.data:
            return os.urandom(16)
        return Encryption.base64.b64decode(self.data["salt"].encode('utf-8')) 


    def show_info(self):
        return self.accounts
    

    def check_info(self, site_name, contact):

        condition = r"^[a-zA-Z0-9.-_%+]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$"

        if not (re.match(condition, contact) or contact.isdigit()):
            return 1
        
        elif site_name in self.accounts.keys() and contact in self.accounts[site_name].keys():
            return 2
        
        return 0
    

    def add_info(self, site_name, contact, password):


        if site_name not in self.accounts.keys():
            self.accounts[site_name] = {contact: password}


        else:
            self.accounts[site_name][contact] = password

        
        

    
    def edit_info(self, site_name, contact, new_password):

        """if this function returned 0: this operation was successful
           if this function returned 1: there is another one with the same name"""        
  

        if site_name in self.accounts.keys():

            self.accounts[site_name][contact] = new_password
            return 0
        
        
        return 1
    


    


    def remove_info(self, site_name, contact):


        """if this function returned 0: this operation was successful
           if this function returned 1: there is another one with the same name"""
        
        

        if site_name in self.accounts.keys():
            del self.accounts[site_name][contact]

            if not self.accounts[site_name]:
                del self.accounts[site_name]

            return 0
        
        return 1
        


    def encrypt_accounts(self):
        for contact_dict in self.accounts.values():
            for contact, password in contact_dict.items():
                contact_dict[contact] = Encryption.encrypt_password(password, self.cipher_suite)



    def dectypt_accounts(self):
        for contact_dict in self.accounts.values():
            for contact, crypted_password in contact_dict.items():
                contact_dict[contact] = Encryption.decrypt_password(crypted_password, self.cipher_suite)