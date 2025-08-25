"""
A simple python shopping list generator. Takes a series of items and prints them to a list.
"""

import os
import re

list_subfolder = "Shopping Lists"   #The subfolder shopping lists are created in

cur_str = lambda value, prefix = "$", suffix = "": f"{prefix}{value:.2f}{suffix}"
#Returns input to 2dp as string with currency prefix/suffix

first_numeric = lambda string: re.search(r"\d+(\.\d+)?", string).group()
#Returns the first valid numerical value from a string; used to filter unwanted noise like "$" etc.

class item:
    #The general class used for all shopping list items
    def __init__(self, data):
        self.name = data[0]        #name of item
        self.amount = data[1]    #amount of this item
        self.item_cost = data[2]  #cost per item
    def __str__(self):
        #For printing the items in a list
        return(f"{self.amount} {self.name}: {cur_str(self.total_cost())}")
    def total_cost(self):
        return(self.amount * self.item_cost)

def request_item(previous_items):
    #Get item name, amount, and cost from user
    end_alts = ["done", "finish", "finished", "end", "stop", "cease", "kill", "break", "halt"]   #The list of words that return False instead of a value
    confirm_words = [["n", "no", "0"], ["y", "yes", "1", "a"]]                       #strings for denial/confirmation; [0] for decline, [1] for accept
    confirm_alts = [["cancel","decline", "deny"], ["confirm", "accept", "good"]]   #keywords for denial/confirmation; [0] for decline, [1] for accept
    name_len_range = [1, 100]
    amount_range = [1, 100]
    cost_range = [0, 10000] #User may have free items they need/things they're not purchasing directly etc.

    name = None
    amount = None
    item_cost = None

    while name == None:
        name = input("Item name: ").strip()
        if name.lower() in end_alts:
            return("End")
        elif len(name) < name_len_range[0]:
            print("Name too short. Try again.")
            name = None
        elif len(name) > name_len_range[1]:
            print("Name too long. Try again.")
            name = None
        elif any((x for x in previous_items if x.name == name)):
            #Make user confirm if item already exists as later code will overwrite it
            while True:
                confirmation = input(f'"{name}" is already on list; delete/overwrite?\n').strip().lower()
                if confirmation in confirm_words[1] or any(word in confirmation for word in confirm_alts[1]):
                    print("\nContinue new entry - ")
                    break
                elif confirmation in confirm_words[0] or any(word in confirmation for word in confirm_alts[0]):
                    name = None
                    print("Overwrite canceled.\n")
                    break
                else:
                    print(f'Unable to interpret answer. Enter "{confirm_alts[1]}" or "{confirm_alts[0]}."')

    while amount == None:
        try:
            amount = input("Quantity: ")
            if amount in confirm_words[0] or any(word in amount for word in confirm_alts[0]):
                print("Entry cancelled, enter new/re-enter item.\n")
                return()
            amount = int(first_numeric(amount))
            if amount < amount_range[0]:
                print("Amount too small. Try again.")
                amount = None
            elif amount > amount_range[1]:
                print("Amount too large. Try again.")
                amount = None
        except:
            print("Use an integer value. Try again.")
            amount = None
    
    while item_cost == None:
        cent_alts = ["cent", "¢"]   #All the ways for the user to say cent and have the function divide the price by 100
        try:
            item_cost = input("Individual cost: ")
            if item_cost in confirm_words[0] or any(word in item_cost for word in confirm_alts[0]):
                print("Entry cancelled, enter new/re-enter item.\n")
                return()
            item_cost = (lambda x: float(first_numeric(x))/100 if any(cent_alt in x for cent_alt in cent_alts) else float(first_numeric(x)))(item_cost.replace(",", ""))
            if item_cost < cost_range[0]:
                print("Cost too low. Try again.")
                item_cost = None
            elif item_cost > cost_range[1]:
                print("Cost too high. Try again.")
                item_cost = None
        except:
            print("Use a numerical value. Try again.")
            item_cost = None
    final_item = item([name, amount, item_cost])
    while True:
        confirmation = input(f"Confirm: {str(final_item)}?\n").strip().lower()
        if confirmation in confirm_words[1] or any(word in confirmation for word in confirm_alts[1]):
            print("Item saved.\n")
            return(final_item)
        elif confirmation in confirm_words[0] or any(word in confirmation for word in confirm_alts[0]):
            print("Entry cancelled, enter new/re-enter item.\n")
            return()
        else:
            print(f'Unable to interpret answer. Enter "{confirm_alts[1][0]}" or "{confirm_alts[0][0]}."')

def save_items():
    #Use item class and request_item() repeatedly to return list of items user wants in shopping list
    items = []
    current_item = request_item(items)
    while current_item != "End" or not items:
        try:
            #Delete pre-existing matching name item if exists, else do nothing
            items.remove(next(x for x in items if x.name == current_item.name))
        except:
            pass
        
        if current_item == "End": print("Please enter an item.")    #Won't let users end program until something on list
        elif current_item: items.append(current_item)
        current_item = request_item(items)
    return(sorted(items, key = lambda x: x.name.lower()))

def safe_name(desired, suffix):
    #Takes desired file name as argument, returns desired if untaken, else returns in name form desired-n where n is lowest untaken int
    if not os.path.exists(desired + suffix):
        return(desired + suffix)
        #If name is already available use it, else calculate shortest untaken suffix and use that:
    n = 1
    while os.path.exists(f"{desired}-{n}{suffix}"):
        n += 1
    return(f"{desired}-{n}{suffix}")

def export_to_file(display_name, file_name, data):
    statistics = (f"Total cost is {cur_str(sum(i.total_cost() for i in data))}\nNumber of items is {sum(i.amount for i in data)}\nNumber of unique items is {len(data)}")
    with open(file_name, "w") as f:
        f.write(display_name + "\n\n")
        for i in data:
            f.write(str(i) + "\n")
        f.write("\n" + statistics)
    print(f"\nShopping list saved as {file_name}")
    print(statistics)
    return()

def request_file_name(prefix, suffix = ".txt"):
    min_name_length = 1
    file_name = None
    if not os.path.exists(prefix): os.makedirs(prefix)  #Creates shopping list subfolder if missing
    while file_name == None:
        desired_name = input("Shopping list name: ")
        file_name = safe_name(prefix + desired_name, suffix)
        try:
            if "/" in desired_name: raise ValueError('Filename cannot contain "/"')
            if len(desired_name) < min_name_length: raise ValueError(f'Filename must be at least {min_name_length} character')
            with open(file_name, "w") as f:
                pass  #Check if file is able to be created
            os.remove(file_name)
        except Exception as e:
            file_name = None
            print(f"Invalid name. Name must also be acceptable file name ({str(e).lower() if type(e) == ValueError else 'given filename unusable'}).")
    return(desired_name, file_name)


print('Enter the following data as instructed.\nYou will be asked to confirm after each item and can cancel at any time (by entering "cancel").\nTo change an item after confirming, simply re-enter it with the same name to delete/overwrite.\n')

export_to_file(*request_file_name(f"{__file__.split('/')[-2]}/{list_subfolder}/"), save_items())