import csv
import tkinter as tk
from operator import index
from tkinter import messagebox, ttk


class Basket:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        for product in self.products:
            if product.id == product_id:
                self.products.remove(product)
                return True
        return False

    def list_products(self):
        return "\n".join(str(product) for product in self.products) if self.products else "Basket is empty."

    def total_price(self):
        total = sum(float(product.price) for product in self.products if product.price)
        return total


class Product:
    def __init__(self, category, id, name, description, price, quantity):
        self.category = category
        self.id = id
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)




    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price} €"


# Hardcoded products (no file reading needed)
class App:
    def __init__(self, root):
        self.remove_entry = None
        self.root = root
        self.basket = Basket()

        # Hardcoded products list
        self.products = []

        with open('products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.products.append(Product(row['Category'], row['ID'], row['Name'], row['Description'], row['Price'], row['Quantity']))


        self.products_by_id = {product.id: product for product in self.products}

        self.root.title("Shopping Basket App")
        self.root.geometry("500x500")

        # Button to open the operations window
        self.open_operations_button = tk.Button(root, text="Basket", command=self.open_operations_window)
        self.open_operations_button.pack(pady=10)

        # Button to open the products view window
        self.view_products_button = tk.Button(root, text="View Products", command=self.open_products_window)
        self.view_products_button.pack(pady=10)

    def open_operations_window(self):
        """Creates and opens the operations window to handle basket actions."""
        operations_window = tk.Toplevel(self.root)
        operations_window.title("Basket Operations")
        operations_window.geometry("400x500")

        # Add product to basket
        tk.Label(operations_window, text="Enter Product ID to Add:").pack()
        self.add_entry = tk.Entry(operations_window)
        self.add_entry.pack()
        add_button = tk.Button(operations_window, text="Add to Basket", command=self.add_product_to_basket)
        add_button.pack()

        # Remove product from basket
        tk.Label(operations_window, text="Enter Product ID to Remove:").pack()
        self.remove_entry = tk.Entry(operations_window)
        self.remove_entry.pack()
        remove_button = tk.Button(operations_window, text="Remove from Basket", command=self.remove_product_from_basket,
                                  bg="red", fg="red")
        remove_button.pack()

        # List products in basket
        list_button = tk.Button(operations_window, text="List Basket Products", command=self.list_products_in_basket)
        list_button.pack()

        # Show total price
        total_button = tk.Button(operations_window, text="Show Total Price", command=self.show_total_price)
        total_button.pack()

        # Text area to display output
        self.output_text = tk.Text(operations_window, height=15, width=40)
        self.output_text.pack()

        # Checkout button to open the checkout page
        checkout_button = tk.Button(operations_window, text="CHECKOUT", command=self.open_checkout_page, bg="green",
                                    fg="green")
        checkout_button.pack(pady=10)

        # Return button to go back to main window
        return_button = tk.Button(operations_window, text="Return", command=operations_window.destroy, bg="gray",
                                  fg="black")
        return_button.pack(pady=10)

    def open_products_window(self):
        """Opens a new window to display all products."""
        products_window = tk.Toplevel(self.root)
        products_window.title("Available Products")
        products_window.geometry("500x400")

        # Scrollable frame for products
        frame = ttk.Frame(products_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Set up the canvas for scrolling
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display each product in the scrollable frame
        for product in self.products:
            product_label = tk.Label(scrollable_frame,
                                     text=f"ID: {product.id} | {product.name} | Price: {product.price}€ | Stock: {product.quantity}")
            product_label.pack(anchor="w", padx=10, pady=5)

        # Return button to close products window
        return_button = tk.Button(products_window, text="Return", command=products_window.destroy, bg="gray",
                                  fg="black")
        return_button.pack(pady=10)

    def open_checkout_page(self):
        """Opens a separate checkout page."""
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Checkout Page")
        checkout_window.geometry("400x500")

        # Display total price
        total = self.basket.total_price()
        self.original_total_label = tk.Label(checkout_window, text=f"Original Total: {total:.2f} €")
        self.original_total_label.pack(pady=5)

        # Label for discount total (initially hidden)
        self.discounted_total_label = tk.Label(checkout_window, text="")
        self.discounted_total_label.pack(pady=5)

        # Promo code section
        tk.Label(checkout_window, text="Enter Promo Code:").pack()
        self.promo_entry = tk.Entry(checkout_window)
        self.promo_entry.pack()

        # Apply promo code button
        apply_button = tk.Button(checkout_window, text="Apply Promo Code", command=self.apply_promo_code)
        apply_button.pack(pady=10)

        # Payment method selection
        tk.Label(checkout_window, text="Select Payment Method:").pack()
        self.payment_method = tk.StringVar(value="cash")  # Default selection
        tk.Radiobutton(checkout_window, text="Cash", variable=self.payment_method, value="cash").pack()
        # Payment method selection

        # Blue color for Visa button
        tk.Radiobutton(checkout_window, text="Visa", variable=self.payment_method, value="visa", fg="blue").pack()

        # Red and yellow mix for MasterCard button
        tk.Radiobutton(checkout_window, text="MasterCard", variable=self.payment_method, value="mastercard",
                       fg="#FF7F00").pack()

        # Confirm checkout button
        confirm_button = tk.Button(checkout_window, text="Confirm Purchase", command=self.confirm_purchase)
        confirm_button.pack(pady=20)

        # Return button to go back to the operations window
        return_button = tk.Button(checkout_window, text="Return", command=checkout_window.destroy, bg="gray",
                                  fg="black")
        return_button.pack(pady=10)

    def apply_promo_code(self):
        """Applies a discount if the promo code is 'student' and updates the display."""
        promo_code = self.promo_entry.get().strip().lower()
        total = self.basket.total_price()

        if promo_code == "student":
            discounted_total = total * 0.85  # Apply 15% discount
            self.discounted_total_label.config(text=f"Discounted Total: {discounted_total:.2f} €")
            messagebox.showinfo("Promo Code Applied",
                                f"15% discount applied! Original: {total:.2f} €, After Discount: {discounted_total:.2f} €")
        else:
            self.discounted_total_label.config(text="")
            if promo_code:  # If an incorrect code is entered
                messagebox.showwarning("Invalid Code", "The promo code entered is invalid.")

    def confirm_purchase(self):
        """Handles purchase confirmation and checks if payment method is selected."""
        if not self.payment_method.get():
            messagebox.showwarning("Payment Method", "Please select a payment method before confirming.")
        else:
            messagebox.showinfo("Purchase",
                                f"Purchase confirmed! Payment method: {self.payment_method.get().capitalize()}")

    def add_product_to_basket(self):
        """Add a product to the basket based on the entered product ID."""
        product_id = self.add_entry.get().strip()
        product = self.products_by_id.get(product_id)
        if product and product.quantity > 0:
            self.basket.add_product(product)
            product.quantity -= 1
            messagebox.showinfo("Added", f"Added {product.name} to the basket.")
            self.update_products_display()
        elif product and product.quantity == 0:
            messagebox.showwarning("Out of Stock", f"{product.name} is out of stock.")
        else:
            messagebox.showerror("Error", "Invalid product ID.")

    def remove_product_from_basket(self):
        """Remove a product from the basket based on the entered product ID."""
        product_id = self.remove_entry.get().strip()
        if self.basket.remove_product(product_id):
            messagebox.showinfo("Removed", f"Removed product with ID {product_id} from the basket.")
            self.update_products_display()
        else:
            messagebox.showerror("Error", "Product not found in the basket.")

    def list_products_in_basket(self):
        """Display the list of products in the basket."""
        products_list = self.basket.list_products()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Products in Basket:\n{products_list}")

    def show_total_price(self):
        """Display the total price of products in the basket."""
        total = self.basket.total_price()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Total: {total:.2f} €")

    def update_products_display(self):
        """Update the product list display, used after add/remove actions."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Basket updated.\n")


# Run the app
root = tk.Tk()
app = App(root)
root.mainloop()
