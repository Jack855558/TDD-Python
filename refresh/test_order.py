import unittest
from refresh import Drink, Order, Food


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

class TestFood(unittest.TestCase): 
    def test_and_create_food(self):
        food = Food('hotdog')
        self.assertEqual(food.get_type(), 'hotdog')
        self.assertEqual(food.get_toppings(), [])

    def test_invalid_food_type_raises_error(self):
        with self.assertRaises(ValueError):
            Food('sushi')
    
    def test_add_valid_topping (self):
        food = Food('french fries')
        food.add_topping('ketchup')
        self.assertIn('ketchup', food.get_toppings())

    def test_add_invalid_topping_raises_error(self):
        food = Food('hotdog')
        with self.assertRaises(ValueError):
            food.add_topping('sprinkles')

    def test_add_duplicate_topping(self):
        food = Food('nacho chips')
        food.add_topping('chili')
        food.add_topping('chili')  # Should not duplicate
        self.assertEqual(food.get_toppings(), ['chili'])

    def test_set_multiple_valid_toppings(self):
        food = Food('nacho chips')
        food.set_toppings(['chili', 'nacho cheese'])
        self.assertEqual(set(food.get_toppings()), {'chili', 'nacho cheese'})
    
    def test_num_toppings(self):
        food = Food('corndog')
        food.add_topping('ketchup')
        food.add_topping('mustard')
        self.assertEqual(food.get_num_toppings(), 2)

    def test_set_invalid_topping_raises_error(self):
        food = Food('french fries')
        with self.assertRaises(ValueError):
            food.set_toppings(['ketchup', 'mayo'])

class TestOrder(unittest.TestCase): 
    def test_and_get_iteams(self): 
        order = Order()
        drink = Drink('water')
        food = Food('hotdog')
        order.add_item(drink)
        order.add_item(food)

        self.assertEqual(order.get_num_items(), 2)
        self.assertEqual(order.get_items()[0].get_base(), 'water')
        self.assertEqual(order.get_items()[1].get_type(), 'hotdog')

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

    def test_receipt_contains_food_and_drink(self):
        drink = Drink('hill fog')
        drink.add_flavor('lime')

        food = Food('ice cream')
        food.add_topping('chocolate sauce')

        order = Order()
        order.add_item(drink)
        order.add_item(food)
        receipt = order.get_receipt()

        self.assertIn("hill fog", receipt)
        self.assertIn("lime", receipt)
        self.assertIn("ice cream", receipt)
        self.assertIn("chocolate sauce", receipt)
        self.assertIn("Total:", receipt)
        self.assertIn("Tax", receipt)


if __name__ == '__main__':
    unittest.main()