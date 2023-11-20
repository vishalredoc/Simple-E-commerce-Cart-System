# -*- coding: utf-8 -*-
"""Simple E-commerce Cart System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YEw-Pj7zX63uWbuxtzAmERYX6pbzYXSO
"""

import copy

# Product base class
class Product:
    def __init__(self, name, price, available=True):
        self.name = name
        self.price = price
        self.available = available

    def clone(self):
        return copy.deepcopy(self)

# Concrete product subclasses
class Laptop(Product):
    pass

class Headphones(Product):
    pass

# Strategy Pattern for discount strategies
class DiscountStrategy:
    def apply_discount(self, total):
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage / 100.0

    def apply_discount(self, total):
        return total - (total * self.percentage)

class Cart:
    def __init__(self, discount_strategy=None):
        self.items = {}
        self.discount_strategy = discount_strategy

    def add_item(self, product, quantity=1):
        if product.name not in self.items:
            self.items[product.name] = {'product': product.clone(), 'quantity': 0}

        self.items[product.name]['quantity'] += quantity

    def update_quantity(self, product_name, quantity):
        if product_name in self.items:
            self.items[product_name]['quantity'] = quantity

    def remove_item(self, product_name):
        if product_name in self.items:
            del self.items[product_name]

    def calculate_total(self):
        total = sum(item['product'].price * item['quantity'] for item in self.items.values())
        if self.discount_strategy:
            total = self.discount_strategy.apply_discount(total)
        return total

    def display_cart(self):
        cart_items = [f"{item['quantity']} {item['product'].name}" for item in self.items.values()]
        print(f"Cart Items: You have {', '.join(cart_items)} in your cart.")
        print(f"Total Bill: Your total bill is ${self.calculate_total()}.")

# Example usage with user input
def main():
    laptop = Laptop("Laptop", 1000)
    headphones = Headphones("Headphones", 50)

    discount_choice = input("Do you want to apply a discount? (yes/no): ")
    discount_strategy = PercentageDiscount(10) if discount_choice.lower() == 'yes' else None

    cart = Cart(discount_strategy)

    while True:
        print("\nAvailable products:")
        print(f"1. {laptop.name} - ${laptop.price}")
        print(f"2. {headphones.name} - ${headphones.price}")

        user_input = input("Enter command (add <product_name> <quantity>, update <product_name> <quantity>, remove <product_name>, exit): ").split()

        try:
            command = user_input[0]

            if command == "add":
                product_name = user_input[1]
                quantity = int(user_input[2])
                if product_name.lower() == "laptop":
                    cart.add_item(laptop, quantity)
                elif product_name.lower() == "headphones":
                    cart.add_item(headphones, quantity)
                else:
                    print("Invalid product name.")

            elif command == "update":
                product_name = user_input[1]
                quantity = int(user_input[2])
                cart.update_quantity(product_name, quantity)

            elif command == "remove":
                product_name = user_input[1]
                cart.remove_item(product_name)

            elif command == "exit":
                break

            else:
                print("Invalid command.")

            cart.display_cart()

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()