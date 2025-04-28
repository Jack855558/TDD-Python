import unittest
from refresh import Drink, Order


class TestDrink(unittest.TestCase):
    def test_and_create_valid_drink(self):
        drink = Drink('sbrite')
        self.assertEqual(drink.get_base(), 'sbrite')
        self.assertEqual(drink.get_flavors(), [])

    def test_invalid_base_raises_error(self):
        with self.assertRaises(ValueError):
            Drink('invalid_base')
    
    def test_add_valid_flavor(self):
        drink = Drink('water')
        drink.add_flavor('lemon')
        self.assertIn('lemon', drink.get_flavors())

    def test_add_invalid_flavor_raises_error(self):
        drink = Drink('water')
        with self.assertRaises(ValueError):
            drink.add_flavor('banana')
    
    def test_add_duplicate_flavor(self):
        drink = Drink('sbrite')
        drink.add_flavor('mint')
        drink.add_flavor('mint')  # Should not duplicate
        self.assertEqual(drink.get_flavors(), ['mint'])

    def test_num_flavors(self):
        drink = Drink('pokeacola')
        drink.add_flavor('lemon')
        drink.add_flavor('cherry')
        self.assertEqual(drink.get_num_flavors(), 2)


class TestOrder(unittest.TestCase): 
    def test_and_get_iteams(self): 
        order = Order()
        drink = Drink('pokeacola')
        order.add_item(drink)
        self.assertEqual(order.get_num_items(), 1)
        self.assertEqual(order.get_items()[0].get_base(), 'pokeacola')

    def test_total_cost(self):
        drink1 = Drink('sbrite')
        drink1.add_flavor('lemon')
        drink1.add_flavor('mint')

        drink2 = Drink('pokeacola')
        drink2.add_flavor('cherry')

        order = Order()
        order.add_item(drink1)
        order.add_item(drink2)

        # drink1: base 5 + 2 flavors = 7
        # drink2: base 5 + 1 flavor = 6
        # total = 13
        self.assertEqual(order.get_total(), 13)

    def test_remove_item(self):
        order = Order()
        drink = Drink('water')
        order.add_item(drink)
        order.remove_item(0)
        self.assertEqual(order.get_num_items(), 0)

    def test_remove_item_out_of_range(self):
        order = Order()
        with self.assertRaises(IndexError):
            order.remove_item(0)
    
    def test_add_non_drink_item_raises_error(self):
        order = Order()
        with self.assertRaises(ValueError):
            order.add_item("not a drink")

    def test_receipt(self):
        drink = Drink('hill fog')
        drink.add_flavor('lime')
        order = Order()
        order.add_item(drink)
        receipt = order.get_receipt()
        self.assertIn("hill fog", receipt)
        self.assertIn("lime", receipt)
        self.assertIn("Total Cost: $6", receipt)


if __name__ == '__main__':
    unittest.main()