import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import json

# Food menu with items, their prices, and corresponding images
food_menu = {
    'Green Canteen': {
        'Chole Bhature': {'price': 100.00, 'image': 'images/chole_bhature.png', 'description': 'Delicious chole served with bhature.'},
        'Chole Chawal': {'price': 50.00, 'image': 'images/chole_chawal.png', 'description': 'Chole served with steamed rice.'},
        'Rajma Chawal': {'price': 50.00, 'image': 'images/rajma_chawal.png', 'description': 'Red kidney beans served with rice.'},
        'Puri Sabji': {'price': 50.00, 'image': 'images/puri_sabji.png', 'description': 'Puri served with mixed vegetable curry.'},
        'Chilli Potato': {'price': 80.00, 'image': 'images/chilli_potato.png', 'description': 'Spicy fried potatoes.'},
        'Spring Roll': {'price': 60.00, 'image': 'images/spring_roll.png', 'description': 'Crispy spring rolls filled with vegetables.'},
        'Chowmein': {'price': 60.00, 'image': 'images/chowmein.png', 'description': 'Stir-fried noodles with vegetables.'},
        'Stuff Paratha': {'price': 50.00, 'image': 'images/stuff_paratha.png', 'description': 'Stuffed paratha served with yogurt.'},
    },
    'Red Canteen': {
        'Samosa': {'price': 15.00, 'image': 'images/samosa.png', 'description': 'Crispy potato-filled pastry.'},
        'Paneer Roll': {'price': 80.00, 'image': 'images/paneer_roll.png', 'description': 'Roll filled with spiced paneer.'},
        'Chowmein Roll': {'price': 40.00, 'image': 'images/chowmein_roll.png', 'description': 'Chowmein wrapped in a roll.'},
        'Egg Roll': {'price': 70.00, 'image': 'images/egg_roll.png', 'description': 'Egg-filled roll with spices.'},
        'Veg Roll': {'price': 50.00, 'image': 'images/veg_roll.png', 'description': 'Vegetable-filled roll.'},
        'Masala Maggi': {'price': 50.00, 'image': 'images/masala_maggi.png', 'description': 'Instant noodles with spices.'},
        'Vegetable Maggi': {'price': 40.00, 'image': 'images/vegetable_maggi.png', 'description': 'Vegetable noodles.'},
        'Chai': {'price': 10.00, 'image': 'images/chai.png', 'description': 'Traditional Indian tea.'},
        'Cold Coffee': {'price': 50.00, 'image': 'images/cold_coffee.png', 'description': 'Chilled coffee drink.'},
        'Oreo Shake': {'price': 50.00, 'image': 'images/oreo_shake.png', 'description': 'Oreo flavored shake.'},
        'Chocolate Shake': {'price': 50.00, 'image': 'images/chocolate_shake.png', 'description': 'Rich chocolate shake.'},
    },
    'Yellow Canteen': {
        'Cheese Sandwich': {'price': 45.00, 'image': 'images/cheese_sandwich.png', 'description': 'Sandwich with cheese and veggies.'},
        'Sandwich': {'price': 30.00, 'image': 'images/sandwich.png', 'description': 'Classic vegetable sandwich.'},
        'Burger': {'price': 40.00, 'image': 'images/burger.png', 'description': 'Juicy burger with toppings.'},
        'Frooti': {'price': 20.00, 'image': 'images/frooti.png', 'description': 'Mango flavored drink.'},
        'Cold Drink': {'price': 40.00, 'image': 'images/cold_drink.png', 'description': 'Chilled soft drink.'},
        'Lassi': {'price': 25.00, 'image': 'images/lassi.png', 'description': 'Yogurt-based drink.'},
        'Smoothie': {'price': 10.00, 'image': 'images/smoothie.png', 'description': 'Fruit blended smoothie.'},
        'Chips': {'price': 20.00, 'image': 'images/chips.png', 'description': 'Crispy potato chips.'},
        'Oreo': {'price': 10.00, 'image': 'images/oreo.png', 'description': 'Delicious Oreo cookies.'},
    },
    'Cafe de latte': {
        'Ice Cream': {'price': 30.00, 'image': 'images/ice_cream.png', 'description': 'Creamy ice cream.'},
        'Brownie': {'price': 50.00, 'image': 'images/brownie.png', 'description': 'Chocolate brownie.'},
        'Cold Coffee': {'price': 50.00, 'image': 'images/cold_coffee.png', 'description': 'Chilled coffee drink.'},
        'Red Bull': {'price': 125.00, 'image': 'images/red_bull.png', 'description': 'Energy drink.'},
        'Coolberg': {'price': 90.00, 'image': 'images/coolberg.png', 'description': 'Non-alcoholic beer.'},
        'Burger': {'price': 40.00, 'image': 'images/burger.png', 'description': 'Juicy burger with toppings.'},
        'Pizza Slice': {'price': 40.00, 'image': 'images/pizza_slice.png', 'description': 'Slice of pizza with cheese.'},
    }
}

# Order cart and history
order_cart = []
order_history = []

# Load order history safely
def load_order_history():
    global order_history
    try:
        if os.path.exists("order_history.json"):
            with open("order_history.json", "r") as file:
                order_history = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        order_history = []

# Save order history
def save_order_history():
    with open("order_history.json", "w") as file:
        json.dump(order_history, file)

# Add item to cart
def add_to_cart(item, price, quantity):
    if quantity <= 0:
        messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero.")
        return
    order_cart.append((item, price, quantity))
    update_total()
    messagebox.showinfo("Item Added", f"{quantity} x {item} added to your cart.")

# View cart
def view_cart():
    def remove_and_refresh(idx, window):
        order_cart.pop(idx)
        update_total()
        window.destroy()
        view_cart()

    cart_window = tk.Toplevel()
    cart_window.title("View Cart")
    cart_window.geometry("400x400")
    cart_window.configure(bg="#f9f9f9")

    header_frame = tk.Frame(cart_window, bg="#4CAF50")
    header_frame.pack(fill=tk.X)

    label = tk.Label(header_frame, text="Your Cart", font=("Arial", 24), bg="#4CAF50", fg="white")
    label.pack(pady=10)

    item_frame = tk.Frame(cart_window, bg="#f9f9f9")
    item_frame.pack(pady=10)

    if not order_cart:
        tk.Label(item_frame, text="Your cart is empty.", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)
    else:
        for index, (item, price, quantity) in enumerate(order_cart):
            cart_label = tk.Label(item_frame, text=f"{item} - ₹{price:.2f} x {quantity}", font=("Arial", 14), bg="#f9f9f9")
            cart_label.pack(anchor="w")

            remove_button = tk.Button(item_frame, text="Remove", 
                                      command=lambda idx=index, win=cart_window: remove_and_refresh(idx, win), 
                                      bg="#F44336", fg="white")
            remove_button.pack(anchor="w", padx=20)

        total = sum(price * quantity for _, price, quantity in order_cart)
        total_label = tk.Label(item_frame, text=f"Total: ₹{total:.2f}", font=("Arial", 18), bg="#f9f9f9", fg="#4CAF50")
        total_label.pack(anchor="w")

# Clear cart
def clear_cart():
    global order_cart
    order_cart.clear()
    update_total()
    messagebox.showinfo("Cart Cleared", "Your cart has been cleared.")

# Update total
def update_total():
    total = sum(price * quantity for _, price, quantity in order_cart)
    total_var.set(f"Total: ₹{total:.2f}")

# Display items in category
def display_items(category):
    items_window = tk.Toplevel()
    items_window.title(f"{category} Menu")
    items_window.geometry("700x600")
    items_window.configure(bg="#f9f9f9")

    header_frame = tk.Frame(items_window, bg="#4CAF50")
    header_frame.pack(fill=tk.X)

    label = tk.Label(header_frame, text=f"{category} Menu", font=("Arial", 24), bg="#4CAF50", fg="white")
    label.pack(pady=10)

    item_frame = tk.Frame(items_window)
    item_frame.pack(pady=10)

    for item, details in food_menu[category].items():
        frame = tk.Frame(item_frame, bd=2, relief=tk.RAISED, padx=10, pady=5, bg="#ffffff")
        frame.pack(pady=5, fill=tk.X)

        quantity_var = tk.IntVar(value=1)
        quantity_dropdown = ttk.Combobox(frame, textvariable=quantity_var, values=list(range(1, 11)), state='readonly', width=3)
        quantity_dropdown.pack(side=tk.LEFT, padx=5)

        button = tk.Button(frame, text=f"{item} - ₹{details['price']:.2f}", font=("Arial", 14), bg="#4CAF50", fg="white",
                           command=lambda i=item, p=details['price'], q=quantity_var: add_to_cart(i, p, q.get()))
        button.pack(side=tk.LEFT)

        description_label = tk.Label(frame, text=details['description'], font=("Arial", 10), wraplength=300, bg="#ffffff")
        description_label.pack(side=tk.LEFT, padx=5)

        if os.path.exists(details['image']):
            img = Image.open(details['image'])
            img = img.resize((50, 50), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img, bg="#ffffff")
            img_label.image = img
            img_label.pack(side=tk.RIGHT)

# Checkout
def checkout():
    if not order_cart:
        messagebox.showwarning("Empty Cart", "Your cart is empty. Add items before checking out.")
        return

    checkout_window = tk.Toplevel()
    checkout_window.title("Checkout")
    checkout_window.geometry("400x400")
    checkout_window.configure(bg="#f9f9f9")

    checkout_summary = tk.Label(checkout_window, text="Checkout Summary", font=("Arial", 24), bg="#4CAF50", fg="white")
    checkout_summary.pack(pady=10)

    item_frame = tk.Frame(checkout_window, bg="#f9f9f9")
    item_frame.pack(pady=10)

    total = 0
    for item, price, quantity in order_cart:
        total += price * quantity
        item_label = tk.Label(item_frame, text=f"{item} - ₹{price:.2f} x {quantity}", font=("Arial", 14), bg="#f9f9f9")
        item_label.pack(anchor="w")

    total_label = tk.Label(item_frame, text=f"Total: ₹{total:.2f}", font=("Arial", 18, "bold"), bg="#f9f9f9", fg="#4CAF50")
    total_label.pack(anchor="w")

    if messagebox.askyesno("Checkout", "Proceed to checkout?"):
        order_history.append(order_cart.copy())
        save_order_history()
        messagebox.showinfo("Checkout", f"Your total is: ₹{total:.2f}\nPay Cash At The Counter\nThank you for your order!")
        clear_cart()

# View order history
def view_order_history():
    history_window = tk.Toplevel()
    history_window.title("Order History")
    history_window.geometry("400x400")
    history_window.configure(bg="#f9f9f9")

    header_frame = tk.Frame(history_window, bg="#4CAF50")
    header_frame.pack(fill=tk.X)

    label = tk.Label(header_frame, text="Order History", font=("Arial", 24), bg="#4CAF50", fg="white")
    label.pack(pady=10)

    item_frame = tk.Frame(history_window, bg="#f9f9f9")
    item_frame.pack(pady=10)

    if not order_history:
        tk.Label(item_frame, text="No orders have been placed yet.", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)
    else:
        for idx, order in enumerate(order_history, start=1):
            order_label = tk.Label(item_frame, text=f"Order {idx}:", font=("Arial", 16, "bold"), bg="#f9f9f9")
            order_label.pack(anchor="w")
            for item, price, quantity in order:
                history_label = tk.Label(item_frame, text=f"  {item} - ₹{price:.2f} x {quantity}", font=("Arial", 14), bg="#f9f9f9")
                history_label.pack(anchor="w")
            tk.Label(item_frame, text="", bg="#f9f9f9").pack()

    close_button = tk.Button(history_window, text="Close", command=history_window.destroy, font=("Arial", 16), bg="#F44336", fg="white")
    close_button.pack(pady=10)

# Main app
def kiosk_food_ordering_system():
    global total_var
    root = tk.Tk()
    root.title("SRM Food Order")
    root.geometry("700x600")
    root.configure(bg="#f9f9f9")

    label = tk.Label(root, text="Welcome to SRM Canteen", font=("Arial", 26), bg="#4CAF50", fg="white")
    label.pack(pady=20)

    total_var = tk.StringVar(value="Total: ₹0.00")
    total_label = tk.Label(root, textvariable=total_var, font=("Arial", 18), bg="#f9f9f9")
    total_label.pack(pady=10)

    category_frame = tk.Frame(root, bg="#f9f9f9")
    category_frame.pack(pady=10)

    for category in food_menu.keys():
        button = tk.Button(category_frame, text=category, font=("Arial", 16), bg="#2196F3", fg="white",
                           command=lambda c=category: display_items(c))
        button.pack(side=tk.LEFT, padx=5)

    view_cart_button = tk.Button(root, text="View Cart", font=("Arial", 16), command=view_cart, bg="#4CAF50", fg="white")
    view_cart_button.pack(pady=20)

    clear_cart_button = tk.Button(root, text="Clear Cart", font=("Arial", 16), command=clear_cart, bg="#F44336", fg="white")
    clear_cart_button.pack(pady=10)

    checkout_button = tk.Button(root, text="Checkout", font=("Arial", 16), command=checkout, bg="#4CAF50", fg="white")
    checkout_button.pack(pady=10)

    order_history_button = tk.Button(root, text="Order History", font=("Arial", 16), command=view_order_history, bg="#2196F3", fg="white")
    order_history_button.pack(pady=10)

    load_order_history()
    root.mainloop()

# Start the app
kiosk_food_ordering_system()