class Drink:
    """A class representing a customizable drink with a base and optional flavors."""

    bases = ['water', 'sbrite', 'pokeacola', 'mr. salt', 'hill fog', 'leaf wine']
    flavors = ['lemon', 'cherry', 'strawberry', 'mint', 'blueberry', 'lime']
    sizes = ['small', 'medium', 'large']

    def __init__(self, base=None, size='medium'):
        base = base.lower() if base else ''
        size = size.lower() if size else ''
        if base not in self.bases:
            raise ValueError('Invalid Base')
        if size not in self.sizes:
            raise ValueError('Invalid Size')
        self._base = base
        self._size = size
        self._flavors = []

    def get_base(self):
        return self._base

    def get_flavors(self):
        return self._flavors

    def get_size(self):
        return self._size

    def set_size(self, size):
        size = size.lower()
        if size not in self.sizes:
            raise ValueError('Invalid Size')
        self._size = size

    def get_num_flavors(self):
        return len(self._flavors)

    def add_flavor(self, flavor):
        if flavor not in self.flavors:
            raise ValueError('Invalid flavor')
        if flavor not in self._flavors:
            self._flavors.append(flavor)
        else:
            print(f"Flavor {flavor} already added.")

    def set_flavors(self, flavors):
        unique_flavors = list(set(flavors))
        for flavor in unique_flavors:
            if flavor not in self.flavors:
                raise ValueError(f"{flavor} is not a valid flavor.")
        self._flavors = unique_flavors

    def get_total(self):
        base_cost = 5.0
        flavor_cost = len(self._flavors) * 0.15
        multiplier = {'small': 0.8, 'medium': 1.0, 'large': 1.2}[self._size]
        return (base_cost + flavor_cost) * multiplier


class Food:
    """A class representing a customizable food item with optional toppings."""

    base_prices = {
        'hotdog': 2.30,
        'corndog': 2.00,
        'ice cream': 3.00,
        'onion rings': 1.75,
        'french fries': 1.50,
        'tater tots': 1.70,
        'nacho chips': 1.90
    }

    topping_prices = {
        'cherry': 0.00,
        'whipped cream': 0.00,
        'caramel sauce': 0.50,
        'chocolate sauce': 0.50,
        'nacho cheese': 0.30,
        'chili': 0.60,
        'bacon bits': 0.30,
        'ketchup': 0.00,
        'mustard': 0.00
    }

    def __init__(self, food_type):
        f = food_type.lower()
        if f not in self.base_prices:
            raise ValueError('Invalid food item.')
        self._type = f
        self._toppings = []

    def get_type(self):
        return self._type

    def get_toppings(self):
        return self._toppings

    def set_toppings(self, toppings):
        unique = list(set(toppings))
        for t in unique:
            if t not in self.topping_prices:
                raise ValueError(f"{t} is not a valid topping.")
        self._toppings = unique

    def add_topping(self, topping):
        if topping not in self.topping_prices:
            raise ValueError('Invalid topping.')
        if topping not in self._toppings:
            self._toppings.append(topping)
        else:
            print(f"Topping {topping} already added.")

    def get_num_toppings(self):
        return len(self._toppings)

    def get_total(self):
        base = self.base_prices[self._type]
        extras = sum(self.topping_prices[t] for t in self._toppings)
        return base + extras


class Order:
    """A class representing an order of drinks and food items."""

    TAX_RATE = 0.0725

    def __init__(self):
        self._items = []

    def get_items(self):
        return self._items

    def add_item(self, item):
        from __main__ import Drink, Food
        if not isinstance(item, (Drink, Food)):
            raise ValueError('Item must be a Drink or Food object')
        self._items.append(item)

    def remove_item(self, index):
        if index < 0 or index >= len(self._items):
            raise IndexError('Item index out of range')
        del self._items[index]

    def get_total(self):
        return sum(item.get_total() for item in self._items)

    def get_tax(self):
        return self.get_total() * self.TAX_RATE

    def get_num_items(self):
        return len(self._items)

    def get_receipt(self):
        lines = ['Receipt:']
        subtotal = 0.0
        for i, item in enumerate(self._items, 1):
            cost = item.get_total()
            subtotal += cost
            if hasattr(item, 'get_base'):
                desc = (f"Drink {i}: Base - {item.get_base()}, Size - {item.get_size()},"
                        f" Flavors - {', '.join(item.get_flavors()) or 'none'}")
            else:
                desc = (f"Food {i}: Type - {item.get_type()},"
                        f" Toppings - {', '.join(item.get_toppings()) or 'none'}")
            lines.append(f"{desc}, Cost: ${cost:.2f}")
        tax = self.get_tax()
        total = subtotal + tax
        lines.append(f"Subtotal: ${subtotal:.2f}")
        lines.append(f"Tax ({self.TAX_RATE*100:.2f}%): ${tax:.2f}")
        lines.append(f"Total: ${total:.2f}")
        return "\n".join(lines)


# Example 
if __name__ == '__main__':
    # Drinks
    drink1 = Drink('sbrite', 'large')
    drink1.add_flavor('lemon')
    drink1.add_flavor('mint')

    drink2 = Drink('pokeacola', 'small')
    drink2.set_flavors(['cherry', 'blueberry', 'cherry'])

    # Foods
    food1 = Food('french fries')
    food1.add_topping('ketchup')
    food1.add_topping('nacho cheese')

    food2 = Food('ice cream')
    food2.set_toppings(['whipped cream', 'chocolate sauce'])

    # Create order
    order = Order()
    order.add_item(drink1)
    order.add_item(drink2)
    order.add_item(food1)
    order.add_item(food2)

    # Print receipt
    print(order.get_receipt())
