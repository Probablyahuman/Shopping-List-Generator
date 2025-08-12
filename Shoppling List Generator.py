import os
import re

cur_str = lambda value, prefix = "$", suffix = "": f"{prefix}{value:.2f}{suffix}"
#Returns value to 2dp as string with currency prefix/suffix

first_numeric = lambda string: re.search(r"\d+(\.\d+)?", string).group()
#Returns the first valid numerical value from a string, used to filter unwanted noise like "$" etc.

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

def request_item():
    #Get item name, amount, and cost from user
    end_keywords = ["done", "finish", "finished", "end", "stop", "cease", "kill", "break", "halt"]   #The list of words that return False instead of a value
    name_len_range = [1, 40]
    amount_range = [1, 100]
    cost_range = [0, 10000] #User may have free items they need/things they're not purchasing directly etc.

    name = None
    amount = None
    item_cost = None

    while name == None:
        name = input("Item name: ")
        if name.lower() in end_keywords:
            return(False)
        elif len(name) < name_len_range[0]:
            print("Name too short. Try again.")
            name = None
        elif len(name) > name_len_range[1]:
            print("Name too long. Try again.")
            name = None

    while amount == None:
        try:
            amount = int(first_numeric(input("Amount: ")))
            if amount < amount_range[0]:
                print("Amount too small. Try again.")
                amount = None
            elif amount > amount_range[1]:
                print("Amount too large. Try again.")
                amount = None
        except:
            print("Use an integer value. Try again.")
    
    while item_cost == None:
        cent_alts = ["cent", "¢"]   #All the ways for the user to say cent and have the function divide the price by 100
        #try:
        if True:
            item_cost = (lambda x: float(first_numeric(x))/100 if any(cent_alt in x for cent_alt in cent_alts) else float(first_numeric(x)))(input("Cost: ").replace(",", ""))
            if item_cost < cost_range[0]:
                print("Cost too low. Try again.")
                item_cost = None
            elif item_cost > cost_range[1]:
                print("Cost too high. Try again.")
                item_cost = None
        '''except:
            print("Use a numerical value. Try again.")'''

    return([name, amount, item_cost])

def save_items():
    #Use item class and request_item() repeatedly to return list of items user wants in shopping list
    items = []
    current_item = request_item()
    while current_item or not items:
        if current_item: items.append(item(current_item))
        else: print("Please enter an item.")
        current_item = request_item()
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
    file_name = None
    while file_name == None:
        desired_name = input("Shopping list name: ")
        file_name = safe_name(prefix + desired_name, suffix)
        try:
            if "/" in desired_name: raise ValueError('Filename cannot contain "/"')
            if len(desired_name) < 1: raise ValueError('Filename must be at least 1 character')
            with open(file_name, "w") as f:
                pass  #Check if file is able to be created
            os.remove(file_name)
        except Exception as e:
            file_name = None
            print(f"Invalid name. Name must also be acceptable file name ({str(e).lower() if type(e) == ValueError else 'given filename unusable'}).")
    return(desired_name, file_name)

export_to_file(*request_file_name("Shopping List Generator/Shopping Lists/"), save_items())