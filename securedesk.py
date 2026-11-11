import tkinter as tk

FAKE_CUSTOMERS = [
    {
        "Customer": "Test Customer One",
        "Card number": "0000 1111 2222 3333",
        "Account number": "000000000001",
        "Phone": "+00 00000 00000",
        "Balance": "0.00",
    },
    {
        "Customer": "Test Customer Two",
        "Card number": "0000 4444 5555 6666",
        "Account number": "000000000002",
        "Phone": "+00 11111 11111",
        "Balance": "0.00",
    },
]


class SecureDeskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SecureDesk - Card Operations")
        self.resizable(False, False)
        width, height = 800, 500
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.customer_index = 0
        self.current_screen = None

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.show_login()

    def switch_to(self, frame):
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = frame
        frame.pack(fill="both", expand=True)

    def show_login(self):
        self.username_var.set("")
        self.password_var.set("")

        frame = tk.Frame(self)
        tk.Label(frame, text="SecureDesk - Card Operations", font=("Segoe UI", 20, "bold")).pack(pady=(70, 5))
        tk.Label(frame, text="Fake login for demo purposes - any value works", fg="gray").pack(pady=(0, 25))

        form = tk.Frame(frame)
        form.pack()
        tk.Label(form, text="Username", width=10, anchor="e").grid(row=0, column=0, pady=6)
        username_entry = tk.Entry(form, textvariable=self.username_var, width=30)
        username_entry.grid(row=0, column=1, pady=6)
        tk.Label(form, text="Password", width=10, anchor="e").grid(row=1, column=0, pady=6)
        password_entry = tk.Entry(form, textvariable=self.password_var, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=6)

        tk.Button(frame, text="Login", width=16, command=self.show_record).pack(pady=25)

        self.bind("<Return>", lambda event: self.show_record())
        self.switch_to(frame)
        username_entry.focus_set()

    def show_record(self):
        self.unbind("<Return>")
        self.username_var.set("")
        self.password_var.set("")

        customer = FAKE_CUSTOMERS[self.customer_index]

        frame = tk.Frame(self)
        header = tk.Frame(frame)
        header.pack(fill="x", padx=30, pady=(25, 5))
        tk.Label(header, text="Customer Record", font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Button(header, text="Logout", width=10, command=self.show_login).pack(side="right")

        tk.Label(
            frame,
            text="FAKE DEMO DATA - not real customers",
            fg="white",
            bg="#b00020",
            padx=10,
            pady=2,
        ).pack(anchor="w", padx=30, pady=(0, 20))

        details = tk.Frame(frame)
        details.pack(anchor="w", padx=30)
        for row, (label, value) in enumerate(customer.items()):
            tk.Label(details, text=f"{label}:", font=("Segoe UI", 13, "bold"), width=16, anchor="w").grid(
                row=row, column=0, pady=7, sticky="w"
            )
            tk.Label(details, text=value, font=("Consolas", 14), anchor="w").grid(
                row=row, column=1, pady=7, sticky="w"
            )

        footer = tk.Frame(frame)
        footer.pack(side="bottom", fill="x", padx=30, pady=25)
        tk.Label(
            footer,
            text=f"Customer {self.customer_index + 1} of {len(FAKE_CUSTOMERS)}",
            fg="gray",
        ).pack(side="left")
        tk.Button(footer, text="Next customer", width=16, command=self.next_customer).pack(side="right")

        self.switch_to(frame)

    def next_customer(self):
        self.customer_index = (self.customer_index + 1) % len(FAKE_CUSTOMERS)
        self.show_record()


if __name__ == "__main__":
    SecureDeskApp().mainloop()
