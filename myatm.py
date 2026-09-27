import tkinter as tk
from tkinter import messagebox
def show_message(text):
    message_display.config(text=text)





# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()
window.configure(bg="lightblue")

window.title("ATM Machine")
window.geometry("500x650")
window.resizable(False, False)
label = tk.Label(window,text="welcome to ATM",font = "Arial,40", bg = "red")
label.pack()


correct_pin = "2006"
balance = 10000
entered_pin = ""
transaction_type = ""


# =========================================================
# LOGIN CONTAINER
# =========================================================

login_container = tk.Frame(
    window,
    bg = "lightgrey",
    width=350,
    height=130,
    highlightbackground="black",
    highlightthickness=2
)

login_container.place(
    relx=0.5,
    y=40,
    anchor="n"
)


tk.Label(
    login_container,
    text="ENTER PIN",
    font=("Arial", 18, "bold"),
    bg="lightgrey"
).pack(pady=10)


pin_display = tk.Entry(
    login_container,
    show="*",
    font=("Arial", 20),
    justify="center",
    width=15
)

pin_display.pack()


# =========================================================
# PIN FUNCTIONS
# =========================================================

def number_click(number):
    global entered_pin

    if len(entered_pin) < 4:
        entered_pin += str(number)

        pin_display.delete(0, tk.END)
        pin_display.insert(0, entered_pin)


def cancel_pin():
    global entered_pin

    entered_pin = ""

    pin_display.delete(0, tk.END)


def enter_pin():

    global entered_pin

    if entered_pin == correct_pin:

        # Hide login and keypad
        login_container.place_forget()
        keypad_frame.place_forget()

        # Show ATM menu
        atm_container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

    else:

        messagebox.showerror(
            "ATM",
            "Wrong PIN"
        )

        cancel_pin()


# =========================================================
# NUMBER KEYPAD
# =========================================================

keypad_frame = tk.Frame(window)

keypad_frame.place(
    relx=0.5,
    y=190,
    anchor="n"
)


number = 1

for row in range(3):

    for column in range(3):

        button = tk.Button(
            keypad_frame,
            text=str(number),
            font=("Arial", 16, "bold"),
            width=6,
            height=2,
            bg = "grey",
            command=lambda n=number: number_click(n)
            
        )

        button.grid(
            row=row,
            column=column,
            padx=5,
            pady=5
        )

        number += 1


# =========================================================
# 0 BUTTON
# =========================================================

zero_button = tk.Button(
    keypad_frame,
    text="0",
    font=("Arial", 16, "bold"),
    width=6,
    height=2,
    bg = "grey",
    command=lambda: number_click(0)
)

zero_button.grid(
    row=3,
    column=1,
    padx=5,

    pady=5
)


# =========================================================
# CANCEL PIN BUTTON
# =========================================================

cancel_button = tk.Button(
    keypad_frame,
    text="CANCEL",
    font=("Arial", 12, "bold"),
    width=8,
    height=2,
    bg = "red",
    command=cancel_pin
)

cancel_button.grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)


# =========================================================
# ENTER PIN BUTTON
# =========================================================

enter_button = tk.Button(
    keypad_frame,
    text="ENTER",
    font=("Arial", 12, "bold"),
    width=8,
    height=2,
    bg = "green",
    command=enter_pin
)

enter_button.grid(
    row=3,
    column=2,
    padx=5,
    pady=5
)


# =========================================================
# ATM MENU CONTAINER
# =========================================================

atm_container = tk.Frame(
    window,
    width=350,
    height=300,
    bg="lightskyblue",
    highlightbackground="black",
    highlightthickness=2
)
message_display = tk.Label(
    atm_container,
    text="Welcome to ATM",
    font=("Arial", 18, "bold"),
    bg="black",
    fg="white",
    width=25,
    height=3,
    anchor="center"
)
message_display.pack(pady=20)


# =========================================================
# CHECK BALANCE
# =========================================================

def check_balance():

    messagebox.showinfo(
        "Balance",
        f"Your Balance is ₹{balance}"
    )


# =========================================================
# SHOW AMOUNT SCREEN
# =========================================================

def show_amount_screen(type):

    global transaction_type

    transaction_type = type

    # Hide ATM menu
    atm_container.place_forget()

    # Show amount container
    amount_container.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    amount_title.config(
        text=f"{type} AMOUNT"
    )

    amount_entry.delete(
        0,
        tk.END
    )


# =========================================================
# CANCEL AMOUNT
# =========================================================

def cancel_amount():

    amount_container.place_forget()

    atm_container.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


# =========================================================
# CONFIRM DEPOSIT / WITHDRAW
# =========================================================

def confirm_transaction():

    global balance

    try:

        amount = float(
            amount_entry.get()
        )

        if amount <= 0:

            messagebox.showerror(
                "Error",
                "Enter valid amount"
            )

            return


        # ---------------- DEPOSIT ----------------

        if transaction_type == "DEPOSIT":

            balance += amount

            messagebox.showinfo(
                "Deposit",
                f"₹{amount} deposited successfully\n\n"
                f"New Balance: ₹{balance}"
            )


        # ---------------- WITHDRAW ----------------

        elif transaction_type == "WITHDRAW":

            if amount > balance:

                messagebox.showerror(
                    "Error",
                    "Insufficient Balance"
                )

                return


            balance -= amount

            messagebox.showinfo(
                "Withdraw",
                f"₹{amount} withdrawn successfully\n\n"
                f"Remaining Balance: ₹{balance}"
            )


        # Go back to ATM menu

        amount_container.place_forget()

        atm_container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )


    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter amount in numbers"
        )


# =========================================================
# ATM MENU
# =========================================================

tk.Label(
    atm_container,
    text="ATM MENU",
    font=("Arial", 22, "bold"),
    bg="lightgray"
).pack(pady=25)


# CHECK BALANCE BUTTON

tk.Button(
    atm_container,
    text="1.CHECK BALANCE",
    width=20,
    anchor="w",
    font=("Arial", 12),
    command=check_balance
).pack(pady=7)


# DEPOSIT BUTTON

tk.Button(
    atm_container,
    text="2.DEPOSIT",
    width=20,
    anchor="w",
    font=("Arial", 12),
    command=lambda: show_amount_screen("DEPOSIT")
).pack(pady=7)


# WITHDRAW BUTTON

tk.Button(
    atm_container,
    text="3.WITHDRAW",
    width=20,
    anchor="w",
    font=("Arial", 12),
    command=lambda: show_amount_screen("WITHDRAW")
).pack(pady=7)


# =========================================================
# AMOUNT CONTAINER
# =========================================================

amount_container = tk.Frame(
    window,
    width=350,
    height=250,
    bg="lightgray",
    highlightbackground="black",
    highlightthickness=2
)


# TITLE

amount_title = tk.Label(
    amount_container,
    text="ENTER AMOUNT",
    font=("Arial", 20, "bold"),
    bg="lightgray"
)

amount_title.pack(pady=30)


# AMOUNT ENTRY

amount_entry = tk.Entry(
    amount_container,
    font=("Arial", 18),
    justify="center"
)

amount_entry.pack(pady=10)


# ENTER AMOUNT

tk.Button(
    amount_container,
    text="ENTER",
    width=15,
    
    font=("Arial", 12, "bold"),
    command=confirm_transaction
).pack(pady=5)


# CANCEL AMOUNT

tk.Button(
    amount_container,
    text="CANCEL",
    
    width=15,
    font=("Arial", 12, "bold"),
    command=cancel_amount
).pack(pady=5)


# =========================================================
# START PROGRAM
# =========================================================

window.mainloop()