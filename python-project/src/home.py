info_window.iconbitmap("Gym.ico")
        try:
            img = Image.open(customer[4])
            img = img.resize((60, 60), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(info_window, image=photo, bg="white").pack(pady=10)
            info_window.image = photo  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            tk.Label(info_window, text="No Photo", bg="white", fg="blue", width=10, height=5, relief="solid").pack(pady=10)
        tk.Label(info_window, text=f"Name: {customer[1]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"Start Date: {customer[6]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"End Date: {customer[7]}", bg="white", fg="blue").pack(pady=10)
        tk.Button(info_window, text="Delete Member", command=lambda: self.delete_member(customer, info_window), bg="blue", fg="white").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(info_window, text="Update Member", command=lambda: self.update_member(customer, info_window), bg="blue", fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

    def delete_member(self, customer, window):
        # Logic to delete the member from the database or list
        pass

    def update_member(self, customer, window):
        # Logic to update the member's information
        pass

    def show_member_info(self, customer):
        info_window = tk.Toplevel()
        info_window.title("Member Information")
        info_window.geometry("300x300")
        info_window.configure(bg="white")
        info_window.iconbitmap("Gym.ico")
        try:
            img = Image.open(customer[4])
            img = img.resize((60, 60), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(info_window, image=photo, bg="white").pack(pady=10)
            info_window.image = photo  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            tk.Label(info_window, text="No Photo", bg="white", fg="blue", width=10, height=5, relief="solid").pack(pady=10)
        tk.Label(info_window, text=f"Name: {customer[1]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"Start Date: {customer[6]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"End Date: {customer[7]}", bg="white", fg="blue").pack(pady=10)
        tk.Button(info_window, text="Delete Member", command=lambda: self.delete_member(customer, info_window), bg="blue", fg="white").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(info_window, text="Update Member", command=lambda: self.update_member(customer, info_window), bg="blue", fg="white").pack(side=tk.RIGHT, padx=10, pady=10)