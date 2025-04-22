class Drink: 
    bases = ['water', 'sbrite', 'pokeacola', 'Mr. Salt', 'hill fog', 'leaf wine']
    flavors = ['lemon', 'cherry', 'strawberry', 'mint', 'blueberry', 'lime']

    def __init__(self, base=None):
        if base not in self.bases: 
            raise ValueError('Invalid Base')
        self._base = base
        self._flavors = []

    #Getter methods for flavors and bases
    def get_base(self): 
        return self._base
    
    def get_flavors(self):
        return self._flavors
    
    def get_num_flavors(self):
        return len(self._flavors)
    
    # Method to add a flavor, ensuring no duplicates
    def add_flavor(self, flavor):
        if flavor not in self.flavors:
            raise ValueError("Invalid flavor")
        if flavor not in self._flavors:
            self._flavors.append(flavor)
        else:
            print(f"Flavor {flavor} already added.")

    #Settors for flavors
    def set_flavors(self, flavors):
        # Ensure no duplicates and only valid flavors are set
        unique_flavors = list(set(flavors))  # Remove duplicates
        for flavor in unique_flavors:
            if flavor not in self.valid_flavors:
                raise ValueError(f"{flavor} is not a valid flavor.")
        self._flavors = unique_flavors

    
class Order:
    def __init__(self):
        # Initialize a list of all drink
        self._items = [] 

    #Getter methods for order
    def get_items (self): 
        return self._items
    
    def get_total(self):
        # Assume each drink has a base cost of 5, and each flavor adds 1 to the cost
        total = 0
        for drink in self._items:
            total += 5  # Base price for every drink
            total += len(drink.get_flavors())  # Each flavor adds 1 to the cost
        return total
    
    def get_num_items(self):
        return len(self._items)
    
    def get_receipt(self):
        # Return a simple string receipt for the order
        receipt = "Receipt:\n"
        for i, drink in enumerate(self._items):
            receipt += f"Drink {i+1}: Base - {drink.get_base()}, Flavors - {', '.join(drink.get_flavors())}\n"
        receipt += f"Total Items: {self.get_num_items()}, Total Cost: ${self.get_total()}"
        return receipt
    
    # Method to add a drink to the order
    def add_item(self, drink):
        if not isinstance(drink, Drink):
            raise ValueError("Item must be a Drink object")
        self._items.append(drink)
    
        # Method to remove a drink from the order by index
    def remove_item(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError("Item index out of range")
        del self._items[index]

    
# Create a new drink with a base and flavors
drink1 = Drink("sbrite")
drink1.add_flavor("lemon")
drink1.add_flavor("mint")

# Create another drink with a different base
drink2 = Drink("pokeacola")
drink2.add_flavor("cherry")
drink2.add_flavor("blueberry")

# Create a new order and add drinks
order = Order()
order.add_item(drink1)
order.add_item(drink2)

# Print the order receipt
print(order.get_receipt())
