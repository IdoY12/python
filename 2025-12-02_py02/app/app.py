from enum import Enum
import json


class Actions(Enum):
    ADD = 1
    KILL = 2
    UPDATE = 3
    DISPLAY = 4
    FIND=5
    EXIT = 6



def display_menu():
    for item in Actions: print(f"{item.value}  -  {item.name}")
    return Actions(int(input("Select from the menu...")))


def add_contact():
    with open('contacts.json', 'r') as f:
        contacts=json.load(f)
    contact_name=input('Contact Name: ')
    age=input('age: ')
    contacts.append({'name': contact_name, "age": age})
    with open('contacts.json', 'w') as f:
        json.dump(contacts, f, indent=4)


def kill_user():
    with open('contacts.json', 'r') as f:
        contacts=json.load(f)

    for i, name_to_kill in enumerate(contacts):
        print(i, ' | ', name_to_kill['name'])
    idx=int(input('Select index to delete contact'))
    contacts.pop(idx)
    
    with open('contacts.json', 'w') as f:
        json.dump(contacts, f, indent=4)




def update_user():
    with open('contacts.json', 'r') as f:
        contacts=json.load(f)
    for i, item in enumerate(contacts):
        print(i, item['name'])
    user_index=int(input("Select contact to update: "))
    contact=contacts[user_index]
    field=input('select field to update name/age: ')
    new_value=input('New Value: ')
    contact[field]=new_value
    with open('contacts.json', 'w') as f:
        json.dump(contacts, f, indent=4)



def display_contacts():
    with open('contacts.json', 'r') as f:
        contacts=json.load(f)
        for i in contacts:
            print(i['name'], ' | ', i['age'])


def exit_plan():
    print("Goodbye!")
    exit()


def find_contact():
    contactToSearch=input('Enter Contact Name: ')
    with open('contacts.json', 'r') as f:
        contacts=json.load(f)
        for i in contacts:
            if i['name'] == contactToSearch:
                return print('Name: ', i['name'], '| ', 'Age: ', i['age'])
        else: return 'contact is missing'


if __name__ == "__main__":
    # print(f"{Actions(1)} this is the name of value --> Actions(1)")
    # print(f"{Actions(2)} this is --> Actions(2)")
    # print(f"{Actions(3)} this is --> Actions(3)")
    while(True):
        userSelection =display_menu()
        if userSelection == Actions.ADD: 
            add_contact()
        if userSelection == Actions.KILL: 
            kill_user()
        if userSelection == Actions.UPDATE: 
            update_user()
        if userSelection == Actions.DISPLAY: 
            display_contacts()
        if userSelection == Actions.FIND:
            find_contact()
        if userSelection == Actions.EXIT: 
            exit_plan()