def view():
    while True:
        pltfrm = input("Enter the platform name to view passwords: ").capitalize()
        with open("passwords.txt", 'r') as f:
            found = False
            content = f.readlines()
            for line in content:
                if line.strip() == f"Platform:{pltfrm}":
                    found = True
                    break
        if not found:
            print(f"No records found for '{pltfrm}'. Please try again.")
            log_access(name,f"Unsucessfull atempt to view records of {pltfrm}")
            continue

        print(f"Here are the saved credentials for {pltfrm}:")
        log_access(name,f"VIWED records of {pltfrm}")
        found = False
        for line in content:
            line = line.strip()
            if found:
                print(line)
                break
            if line == f"Platform:{pltfrm}":
                found = True
        break


def add():
    pltfrm = input("Enter the platform name you want to save: ").capitalize()
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    with open("passwords.txt", "a") as f:
        f.write(f"Platform:{pltfrm}\nUsername:{username} | Password:{password}\n\n")
    print(f"Credentials for {pltfrm} saved successfully!")
    log_access(name,f"ADDED credentials to {pltfrm}")


def edit():
    b = input("Would you like to update your 'username' or 'password'? ").lower()
    if b=="username" or b=="password":
        pltfrm = input("Enter the platform name: ").capitalize()
        while True:
            with open("passwords.txt", 'r') as f:
                found = False
                content = f.readlines()
                for line in content:
                    if line.strip() == f"Platform:{pltfrm}":
                        found = True
                        break
                if not found:
                    print(f"No records found for '{pltfrm}'.")
                    break

            if b == "username":
                new_username = input(f"Enter the new username for {pltfrm}: ")
                old_username = input(f"Enter the current username for {pltfrm}: ")
                with open("passwords.txt", 'r') as f:
                    data = f.readlines()

                check = False
                with open("passwords.txt", 'w') as f:
                    i = 0
                    while i < len(data):
                        if data[i] == f"Platform:{pltfrm}\n":
                            f.write(data[i])
                            if f"Username:{old_username}" in data[i + 1]:
                                updated_data = data[i + 1].replace(f"Username:{old_username}", f"Username:{new_username}")
                                check = True
                                f.write(updated_data)
                                i += 2
                                print("Username updated successfully!")
                                log_access(name,f"EDITED username for {pltfrm}")
                                continue
                            elif i + 1 < len(data):
                                f.write(data[i + 1])
                                i += 2
                                print("The username did not match. Try again.")
                                log_access(name,f"Unsucessfull atempt to edit username for {pltfrm}")
                                continue
                        f.write(data[i])
                        i += 1
                    if check:
                        break
            elif b=="password":
                new_password = input(f"Enter the new password for {pltfrm}: ")
                old_password = input(f"Enter the current password for {pltfrm}: ")
                with open("passwords.txt", "r") as f:
                    pwsd = f.readlines()

                check = False
                with open("passwords.txt", 'w') as f:
                    i = 0
                    while i < len(pwsd):
                        if pwsd[i] == f"Platform:{pltfrm}\n":
                            f.write(pwsd[i])
                            if i + 1 < len(pwsd) and f"Password:{old_password}" in pwsd[i + 1]:
                                updated_pwsd = pwsd[i + 1].replace(f"Password:{old_password}", f"Password:{new_password}")
                                check = True
                                f.write(updated_pwsd)
                                i += 2
                                print("Password updated successfully!")
                                log_access(name,f"EDITED Password for {pltfrm}")
                                continue
                            elif i + 1 < len(pwsd):
                                f.write(pwsd[i + 1])
                                i += 2
                                print("The password did not match. Try again.")
                                log_access(name,f"Unsucessfull atempt to edit Password for {pltfrm}")
                                continue
                        f.write(pwsd[i])
                        i += 1
                    if check:
                        break
    else:
        print("invalid request")
def remove():
    while True:
        d = input("Do you want to delete a set of credentials? (yes/no): ").lower()
        if d == "yes":
            pltfrm = input("Enter the platform name: ").capitalize()
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            with open("passwords.txt", 'r') as f:
                content = f.readlines()
            check = False
            with open("passwords.txt", 'w') as f:
                i = 0
                while i < len(content):
                    if i + 1 < len(content) and content[i].strip() == f"Platform:{pltfrm}" and \
                            content[i + 1].strip() == f"Username:{username} | Password:{password}":
                        print("Credentials deleted successfully!")
                        log_access(name,f"REMOVED credentials from {pltfrm}")
                        check = True
                        i += 2
                        continue
                    f.write(content[i])
                    i += 1
            if not check:
                print("Credentials did not match. Please check and try again.")
                log_access(name,f"Unsucessfull atempt to remove credentials from {pltfrm}")
            break
        elif d == "no":
            print("No changes made.")
            break

import datetime
def log_access(user, status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("access_log.txt", "a") as f:
        f.write(f"[{now}] User: {user} | Status: {status}\n")


name = input("Welcome! Please enter your name: ")
print(f"Hello, {name}!")
count = 0
while True:
    master_psw = input("Enter your master password to continue: ")
    if master_psw == "rabinsayshi":
        print("Access granted! Welcome to your password manager.")
        log_access(name,"LOGIN")
        while True:
            mode = input("What would you like to do? (add/view/edit/remove/exit): ").lower()
            if mode == "add":
                add()
            elif mode == "view":
                view()
            elif mode == "edit":
                edit()
            elif mode == "remove":
                remove()
            elif mode == "exit":
                print("Goodbye! Stay safe with your passwords.")
                log_access(name,"LOGOUT")
                exit()
            else:
                print(f"'{mode}' is not a valid option. Please try again.")
    else:
        print("Incorrect master password. Try again.")
        log_access(name,"FAILED LOGIN ATEMPT")
        count += 1
        if count == 3:
            print("Too many failed attempts. Access denied.")
            log_access(name,"LOCKED OUT")
            break