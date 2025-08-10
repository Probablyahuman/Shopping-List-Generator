import os

class item:
    #The general class used for all shopping list items
    def __init__(self, data):
        self.name = data[0]        #name of item
        self.amount = data[1]    #amount of this item
        self.item_cost = data[2]  #cost per item
    def __str__(self):
        #For printing the items in a list
        return(f"{self.amount} {self.name}: ${self.total_cost()}")
    def total_cost(self):
        return(self.amount * self.item_cost)
    
def request_item():
    #Get item name, amount, and cost from user
    end_keywords = ["done", "finish", "finished", "end", "stop", "cease", "kill", "break"]   #The list of words that return False instead of a value
    name_len_range = [1, 40]
    amount_range = [1, 20]
    cost_range = [0, 5000] #User may have free items they need/things they're not purchasing directly etc.

    name = False
    amount = False
    item_cost = False

    while not name:
        name = input("Item name: ")
        if name.lower() in end_keywords:
            return(False)
        elif len(name) < name_len_range[0]:
            print("Name too short. Try again.")
            name = False
        elif len(name) > name_len_range[1]:
            print("Name too long. Try again.")
            name = False

    while not amount:
        try:
            amount = int(input("Amount: "))
            if amount < amount_range[0]:
                print("Amount too small. Try again.")
                amount = False
            elif amount > amount_range[1]:
                print("Amount too large. Try again.")
                amount = False
        except:
            print("Use an integer value. Try again.")
    
    while not item_cost:
        try:
            item_cost = float(input("Cost: "))
            if item_cost < cost_range[0]:
                print("Cost too low. Try again.")
                item_cost = False
            elif item_cost > cost_range[1]:
                print("Cost too high. Try again.")
                item_cost = False
        except:
            print("Use a numerical value. Try again.")

    return([name, amount, item_cost])

def save_items():
    #Use item class and request_item() repeatedly to return list of items user wants in shopping list
    items = []
    current_item = request_item()
    while current_item:
        items.append(item(current_item))
        current_item = request_item()
    return(items)

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
    with open(file_name, "w") as f:
        f.write(display_name + "\n\n")
        for i in data:
            f.write("\n" + str(i) )
    print(f"Shopping list saved as {file_name}")
    print(f"Total cost was {sum(i.total_cost() for i in data)}")
    print(f"Total items was {sum(i.amount for i in data)}")
    print(f"Total unique items was {len(data)}")
    return()

list_name = input("Shopping list name: ")

export_to_file(list_name, safe_name("Shopping List Generator/Shopping Lists/" + list_name, ".txt"), save_items())

#print(sum(i.total_cost() for i in items))

#print total cost is:
#file saved as ...