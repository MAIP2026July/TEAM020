import tkinter as tk

FAKE_INVOICES = [
    ("INV-0001", "Test Customer Alpha", "0.00"),
    ("INV-0002", "Test Customer Beta", "0.00"),
    ("INV-0003", "Test Customer Gamma", "0.00"),
]


def main():
    root = tk.Tk()
    root.title("FakeLedger - Test Application 2")
    root.geometry("520x320")

    tk.Label(root, text="FAKE DATA - FOR TESTING ONLY", bg="#b00020", fg="white", font=("Segoe UI", 11, "bold")).pack(fill="x")
    tk.Label(root, text="Fake invoice list", font=("Segoe UI", 16, "bold")).pack(pady=(14, 8))
    for number, customer, amount in FAKE_INVOICES:
        tk.Label(root, text=f"{number}    {customer}    Amount: {amount}", font=("Consolas", 12)).pack(anchor="w", padx=30, pady=3)
    tk.Button(root, text="Close", width=12, command=root.destroy).pack(side="bottom", pady=16)

    root.mainloop()


if __name__ == "__main__":
    main()
