# Isabella Kemp
# Mailroom part 3 - incorporating exceptions and comprehensions
# 2/16/2020

import sys
import pathlib
import time

# List of donors and the amounts they have donated
donors = {"John": [150080.00, 41.28],
          "Irene": [1600.00, 24.47],
          "Rob": [19000.00, 200.47],
          "Kathy": [819.00, 34.5],
          "Laureen": [830.00, 47.00, 982.13],
          "Miles": [24.50, 87.00, 193.00]}

main_prompt = ("\n\nWelcome to the Mailroom! Please choose an option from the menu:"
               "\n1. Send a Thank you"
               "\n2. Create a Report"
               "\n3. Send letters to all donors"
               "\n4. Quit"
               "\n\n ----> ")


# Common function to get input from user, call with a prompt string
def get_user_input(prompt_string):
    response = input(prompt_string)
    return response


# User can enter 'list' to get list of existing donors
# User can enter 'listall' to get list of donors and their donations
# User can enter existing donor name, new donation, donation is added to list
# User can enter a new donor, new donation, user and donation is added to list
# We finish with a thank you
def thank_you():
    while True:
        name = get_user_input("Enter a donor name to send a thank you letter, "
                              "'list' or 'listall' for list of donors, '4' will exit: ")
        if name == "list":
            # comprehension
            print(list(donors))
        elif name == "listall":
            # entire record name with donations
            for key in donors:
                print("{0} {1}". format(key, donors[key]))
        elif name == '4':  # quit and return to main menu
            print("Finished processing thanks to donors...\n\n")
            return
        else:
            # User entered a name, so process that
            record = get_donor(name)
            donation = get_donation()
            # print(record) # for debug comment out
            if (record is not None):
                # donor is in our list,
                # get donation amount, add donation to list, send thank you
                print("Existing Donor")
                record.append(donation)
                donors[name] = record

            else:
                # new donor is not in our list, add the donor to our list
                # get donation amount, add donation to list, send thank you
                print("!!! NEW DONOR !!!")
                donors.update({name: [donation]})
        
            email(name, donation)

# end thank_you


# Checks to see if provided name is in our donor list
# returns donor record if found, else None
def get_donor(donor_name):
    return donors.get(donor_name)
    '''
    record = None
    try:
        record = donors[donor_name]
    except KeyError:
        record = None
    finally:
        return record'''


# Get donation amount
def get_donation():
    while True:
        money = get_user_input("Please enter a donation amount: $ ")
        try:
            amount = float(money)
            if amount <= 0:
                print("Invalid value")
            else:
                return amount
        except ValueError:
            print("Invalid value")


# Send thank you to donor
def email(name, amount):
    print("Thank you {}, for your generous donation of ${:.2f} !".format(name, amount))


# Sends a thank you letter for each donor and writes each letter to disk as a text file.
def letters():
    print("Sending a letter to all donors...")

    pth = pathlib.Path('./')
    folder = pth.absolute()
    # folder = tempfile.gettempdir()
    # print(folder)

    for donor in donors.keys():
        first_name = donor.split()[0]
        charity = sum(donors[donor])
        file_format = "{0}.txt".format(first_name)
        file_path = folder / file_format
        try:
            print(file_path)
            with open(file_path, 'w') as write_file:
                letters = ('Dear {0},\n'
                            'Thank you for your donations totaling '
                            '$ {1:,}. We very much appreciate it.\n'
                            'All the best,\n'
                            '- Izzy (Charity President)').format(first_name, charity)                

                write_file.write(letters)
        except IOError:
            print("Unable to write to file")


# Creates a report of donor name, total donated, number of donations, and avg donation.
def report():
    print("\n{:<19}| {:<13} | {:<13} | {:>13}".format('Donor Name', 'Total Donated',
                                                      'Number of Donations',
                                                      'Avg. Donation Amount'))
    print("-"*80)
    # Takes donors and sorts it representing each item in the list
    # Converts the dictionary to a list
    donors_list = list(donors.items())
    sort_donor = sorted(donors_list, key=sort_key, reverse=True)
    # For loop going through donors and calculating sum, number of donations, and average donations

    # not sure how to make a comprehension out of this for loop:
    for donor in sort_donor:
        total = sum(donor[1])
        num_donations = len(donor[1])
        average = total/num_donations
        print('{:<20} ${:>11,.2f}{:>13}            ${:>11,.2f}'.format(
            donor[0], total, num_donations, average))
           

# define sort key
def sort_key(donor):
    return sum(donor[1])


def exit_menu():
    print("Thank you, Goodbye...")
    sys.exit()  


def main():
    switch_func_dict = {
        "1": thank_you,
        "2": report,
        "3": letters,
        "4": exit_menu,
    }

    while True:
        try:
            num = get_user_input(main_prompt)
            switch_func_dict.get(num)()
        except TypeError:
            print("Main menu input is invalid, enter 1 2 3 4 only please")
        finally:
            time.sleep(1)


if __name__ == "__main__":
    main()
