class Drink: 
    """A class representing a customizable drink with a base and optional flavors."""

    bases = ['water', 'sbrite', 'pokeacola', 'Mr. Salt', 'hill fog', 'leaf wine']
    flavors = ['lemon', 'cherry', 'strawberry', 'mint', 'blueberry', 'lime']
    sizes = ['small', 'medium', 'large']

    def __init__(self, base=None, size='medium'):
        """Initialize a Drink with a specified base and size.

        Args:
            base (str): The base type of the drink.
            size (str): The size of the drink (small, medium, or large).

        Raises:
            ValueError: If the base or size is not valid.
        """
        base = base.lower() if base else ''
        size = size.lower() if size else ''
        
        if base not in self.bases:
            raise ValueError('Invalid Base')
        if size not in self.sizes:
            raise ValueError('Invalid Size')

        self._base = base
        self._size = size
        self._flavors = []

    #Getter methods for flavors and bases
    def get_base(self): 
        """Get the base of the drink.

        Returns:
            str: The base of the drink.
        """
        return self._base
    
    def get_flavors(self):
        """Get the list of flavors added to the drink.

        Returns:
            list: Flavors added to the drink.
        """
        return self._flavors
    
    def get_size(self):
        """Get the size of the drink."""
        return self._size

    def set_size(self, size):
        """Set the size of the drink.

        Args:
            size (str): The new size of the drink.
        """
        size = size.lower()
        if size not in self.sizes:
            raise ValueError("Invalid Size")
        self._size = size

    
    def get_num_flavors(self):
        """Get the number of flavors added to the drink.

        Returns:
            int: Number of flavors.
        """
        return len(self._flavors)
    
    # Method to add a flavor, ensuring no duplicates
    def add_flavor(self, flavor):
        """Add a flavor to the drink if it hasn't been added already.

        Args:
            flavor (str): The flavor to add.

        Raises:
            ValueError: If the flavor is not valid.
        """
        if flavor not in self.flavors:
            raise ValueError("Invalid flavor")
        if flavor not in self._flavors:
            self._flavors.append(flavor)
        else:
            print(f"Flavor {flavor} already added.")

    #Settors for flavors
    def set_flavors(self, flavors):
        """Set multiple flavors for the drink, ensuring they are valid and unique.

        Args:
            flavors (list): A list of flavors to set.

        Raises:
            ValueError: If any flavor is not valid.
        """
        # Ensure no duplicates and only valid flavors are set
        unique_flavors = list(set(flavors))  # Remove duplicates
        for flavor in unique_flavors:
            if flavor not in self.valid_flavors:
                raise ValueError(f"{flavor} is not a valid flavor.")
        self._flavors = unique_flavors

    def get_total(self):
        """Calculate the total cost of the drink, including base cost and flavor cost.

        Returns:
            float: The total cost of the drink.
        """
        base_cost = 5  # Base cost for every drink
        flavor_cost = len(self._flavors) * 0.15  # Cost per flavor added
        size_multiplier = 1.0  # Default multiplier for 'medium'
        
        # Size cost adjustments
        if self._size == 'small':
            size_multiplier = 0.8
        elif self._size == 'large':
            size_multiplier = 1.2

        total_cost = base_cost + flavor_cost
        total_cost *= size_multiplier
        return total_cost

    
class Order:
    """A class representing an order of drinks."""

    TAX_RATE = 0.0725  # Tax rate for the order (7.25%)

    def __init__(self):
        """Initialize an empty order."""
        self._items = [] 

    #Getter methods for order
    def get_items (self): 
        """Get all drinks in the order.

        Returns:
            list: Drinks in the order.
        """
        return self._items
    
    def get_total(self):
        """Calculate the total cost of the order. / Assume each drink has a base cost of 5, and each flavor adds 1 to the cost

        Returns:
            int: Total cost in dollars.
        """
        total = 0
        for drink in self._items:
            total += 5  # Base price for every drink
            total += len(drink.get_flavors())  # Each flavor adds 1 to the cost
        return total
    
    def get_tax(self):
        """Calculate the tax for the total order.

        Returns:
            float: The tax amount for the order.
        """
        return self.get_total() * self.TAX_RATE
    
    def get_num_items(self):
        """Get the number of drinks in the order.

        Returns:
            int: Number of drinks.
        """
        return len(self._items)
    
    def get_receipt(self):
        """Generate a receipt for the order, including base costs, flavor costs, tax, and total.

        Returns:
            str: A formatted receipt string for the order.
        """
        receipt = "Receipt:\n"
        total_cost = 0
        for i, drink in enumerate(self._items):
            drink_total = drink.get_total()
            total_cost += drink_total
            receipt += f"Drink {i + 1}: Base - {drink.get_base()}, Size - {drink.get_size()}, Flavors - {', '.join(drink.get_flavors())}, Cost: ${drink_total:.2f}\n"
        
        tax = self.get_tax()
        receipt += f"Subtotal: ${total_cost:.2f}\n"
        receipt += f"Tax (7.25%): ${tax:.2f}\n"
        receipt += f"Total: ${total_cost + tax:.2f}"
        return receipt
    
    # Method to add a drink to the order
    def add_item(self, drink):
        """Add a drink to the order.

        Args:
            drink (Drink): The drink to add.

        Raises:
            ValueError: If the item is not a Drink object.
        """
        if not isinstance(drink, Drink):
            raise ValueError("Item must be a Drink object")
        self._items.append(drink)
    
        # Method to remove a drink from the order by index
    def remove_item(self, index):
        """Remove a drink from the order by its index.

        Args:
            index (int): The index of the drink to remove.

        Raises:
            IndexError: If the index is out of range.
        """
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
