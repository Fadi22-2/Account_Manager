from AccountManager import AccountManager
import os, sys

class Interface:

    def __init__(self):
        self.account_manager = AccountManager()
        self.accounts = self.account_manager.show_info()
        self.there_password = self.account_manager.is_there_password()

    @staticmethod
    def clear_console() -> None:
        #clear the console/terminal
        os.system("cls" if os.name == "nt" else "clear")

    def get_contact(self, name: str, number: int) -> str:

        contacts = iter(self.accounts[name].keys())

        for _ in range(number - 1):
            next(contacts)

        return next(contacts)
    



    def exit_program(self):
        self.account_manager.end_program()
        sys.exit(0)

    def set_new_password(self) -> None:
        while True:
                self.clear_console()
                new_password = input("Enter The New Password: ")
                confirm_password = input("Confirm The Password: ")

                if new_password == confirm_password:
                    self.account_manager.set_main_password(new_password)
                    print("Password Added Successful")
                    input()
                    break

                else:
                    print("Try Again")
                    input()
    


    def enter_main_password(self) -> None:
        if self.there_password:

            while True:
                self.clear_console()

                password = input("Enter The Main Password(q to quit): ")

                if password == "q":
                    self.exit_program()

                elif self.account_manager.check_password(password):
                    break

                else:
                    print("Incorrect Password, Try Again")
                    input()


        else:
            self.set_new_password()

    

    def update_accounts(self):
        self.accounts = self.account_manager.show_info()


    def show_accounts(self):

        if not self.accounts:
            print("There is No Password")
            return
        
        
        for site in self.accounts.keys():
            accounts_num = 0
            print("-"*30 + f'\n{site}:\n')
            for contact, password in self.accounts[site].items():
                accounts_num += 1
                print(f"{accounts_num}. {contact} : {password}")


        print("-"*30)

    def run(self):

        self.enter_main_password()

        main_menu = """choose:
        1. Add Account
        2. Edit Account
        3. Remove Account
        4. Set New Password
        """


        print("Welcome To AccountManager \n")

        while True:
            self.clear_console()
            self.show_accounts()
            print("\n" + main_menu)
            choice = input("Enter your Choice from 1 to 4 (0 to exit): ")

            match choice:

                case "1":
                    while True:

                        name = (input("Enter the Name of site(q to quit): ")).title()
                        if name.lower() == "q" or name == "": break

                        contact = (input("Enter The email or phone number(q to quit): ")).lower()
                        if contact.lower() == "q" or contact == "": break

                        checked_info = self.account_manager.check_info(name, contact)

                        if checked_info:

                            if checked_info == 1:
                                print("Enter a Valid contact")

                            elif checked_info == 2:
                                print(f"This contact is already in {name} site")

                            input()
                            continue


                        password = input("Enter The Password(q to quit): ")
                        if password.lower() == "q" or password == "": break


                        error = self.account_manager.add_info(name, contact, password)
                        if not error:
                            print("Adding Password was Successful")
                            input()
                            break

                        
                        input()


                case "2":
                    if self.accounts:
                        while True:

                            name = (input("Enter the Name of site(q to quit): ")).title()
                            if name.lower() == "q" or name == "": return

                            if name not in self.accounts.keys():
                                print("Invalid Site")
                                input()
                                continue

                            try:
                                number = int(input("Enter The Number of Account(0 to quit): "))
                                if number == 0: break
                            except ValueError:
                                print("Enter 0 not letter, poor guy")
                                input()
                                continue

                            contact = self.get_contact(name, number)

                            if not contact:
                                print("Invalid Index")
                                input()
                                continue


                            new_password = input("Enter The New Password(q to quit): ")
                            if new_password == "q": break


                            error = self.account_manager.edit_info(name, contact, new_password)

                            if not error:
                                print("Editing Password was Successful")
                                input()
                                break
                                
                            elif error == 1:
                                print("Error, Editing Password wasn't Successful")

                            elif error == 2:
                                print("Error, contact is Not in Database")

                            input()



                    else:
                        print("There's No Account to Edit")
                        input()
                    

                case "3":
                    if self.accounts:
                        while True:
                            name = (input("Enter The Site Name(q to quit): ")).title()

                            if name not in self.accounts.keys():
                                print("Invalid Site")
                                input()
                                continue

                            elif name.lower() == "q" or name == "": break

                            try:
                                number = int(input("Enter The Number of Account(0 to quit): "))
                                if number == 0: break

                            except ValueError:
                                print("Enter 0 not letter, poor guy")
                                input()
                                continue

                            if number == 0: break

                            contact = self.get_contact(name, number)

                            if not contact:
                                print("Invalid Index")
                                input()
                                continue

                            error = self.account_manager.remove_info(name, contact)

                            if not error:
                                print("Deleting Password was Successful")
                                input()
                                break
                                
                            elif error == 1:
                                print("Deleting Password Wasn't Successful")


                            elif error == 2:
                                print("Error, contact is not in Database")

                            input()

                    else:
                        print("There's No Account to remove")
                        input()


                case "4":
                    self.set_new_password()


                case "0":
                    self.exit_program()
                    break
                
                case _:
                    print("Enter the number between 0 and 4")
                    input()
                    continue

            
            self.update_accounts()

            
