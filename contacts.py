import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
import sqlite3

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        self.create_widgets()
        self.connect_db()
        self.load_contacts()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg='#d1e0e0')
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        contacts_label = tk.Label(left_frame, text="CONTACTS", bg='#d1e0e0', fg='#003333', font=Font(size=20, weight='bold'))
        contacts_label.pack(side=tk.TOP, anchor='nw', pady=20, padx=20)

        self.contact_info_label = tk.Label(left_frame, text="No contact selected", bg='#d1e0e0', fg='#003333', font=Font(size=14))
        self.contact_info_label.pack(side=tk.TOP, anchor='nw', pady=10, padx=20)

        update_button = tk.Button(left_frame, text="Update Contact", font=Font(size=12), bg='#d1e0e0', command=self.update_contact)
        update_button.pack(side=tk.TOP, anchor='nw', pady=5, padx=20)

        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_section = tk.Frame(right_frame, bg='white', bd=1, relief=tk.SOLID)
        top_section.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        settings_button = tk.Menubutton(top_section, text="⚙️", font=Font(size=20), bg='white', borderwidth=0)
        settings_button.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)
        settings_menu = tk.Menu(settings_button, tearoff=0)
        settings_menu.add_command(label="Show All Contacts", command=self.show_all_contacts)
        settings_button.config(menu=settings_menu)

        delete_button = tk.Button(top_section, text="🗑️", font=Font(size=20), bg='white', borderwidth=0, command=self.delete_contact)
        delete_button.pack(side=tk.RIGHT, anchor='ne', padx=10, pady=10)

        add_button = tk.Button(top_section, text="+", font=Font(size=20), bg='white', borderwidth=0, command=self.add_contact)
        add_button.pack(side=tk.RIGHT, anchor='ne', padx=10, pady=10)

        search_button = tk.Button(top_section, text="🔍", font=Font(size=20), bg='white', borderwidth=0, command=self.search_contact)
        search_button.pack(side=tk.RIGHT, anchor='ne', padx=10, pady=10)

        profile_frame = tk.Frame(top_section, bg='white')
        profile_frame.pack(expand=True)

        profile_label = tk.Label(profile_frame, text="👤", font=Font(size=100), bg='white')
        profile_label.pack()

        bottom_section = tk.Frame(right_frame, bg='white', bd=1, relief=tk.SOLID)
        bottom_section.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(bottom_section, columns=('Name', 'Phone'), show='headings', style='Custom.Treeview')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Custom.Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.map('Custom.Treeview', background=[('selected', '#347083')])

    def connect_db(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()

    def load_contacts(self):
        self.contacts = []
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute('SELECT * FROM contacts')
        rows = self.cursor.fetchall()
        for row in rows:
            self.contacts.append({'id': row[0], 'name': row[1], 'phone': row[2], 'email': row[3], 'address': row[4]})
            self.tree.insert('', tk.END, values=(row[1], row[2]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            contact = self.tree.item(selected_item, 'values')
            for c in self.contacts:
                if c['name'] == contact[0] and c['phone'] == contact[1]:
                    self.contact_info_label.config(
                        text=f"Name: {c['name']}\nPhone: {c['phone']}\nEmail: {c['email']}\nAddress: {c['address']}"
                    )

    def add_contact(self):
        contact_info = self.get_contact_info()
        if contact_info:
            self.cursor.execute('''
                INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)
            ''', (contact_info['name'], contact_info['phone'], contact_info['email'], contact_info['address']))
            self.conn.commit()
            self.load_contacts()

    def update_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            contact = self.tree.item(selected_item, 'values')
            for c in self.contacts:
                if c['name'] == contact[0] and c['phone'] == contact[1]:
                    contact_info = self.get_contact_info(c)
                    if contact_info:
                        self.cursor.execute('''
                            UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?
                        ''', (contact_info['name'], contact_info['phone'], contact_info['email'], contact_info['address'], c['id']))
                        self.conn.commit()
                        self.load_contacts()
                        self.contact_info_label.config(
                            text=f"Name: {contact_info['name']}\nPhone: {contact_info['phone']}\nEmail: {contact_info['email']}\nAddress: {contact_info['address']}"
                        )
        else:
            messagebox.showwarning("Warning", "Please select a contact")

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            contact = self.tree.item(selected_item, 'values')
            for c in self.contacts:
                if c['name'] == contact[0] and c['phone'] == contact[1]:
                    self.cursor.execute('DELETE FROM contacts WHERE id = ?', (c['id'],))
                    self.conn.commit()
                    self.load_contacts()
                    self.contact_info_label.config(text="No contact selected")
                    break
        else:
            messagebox.showwarning("Warning", "Please select a contact")

    def search_contact(self):
        query = simpledialog.askstring("Search", "Enter name or phone number:")
        if query:
            self.tree.delete(*self.tree.get_children())
            for contact in self.contacts:
                if query.lower() in contact['name'].lower() or query in contact['phone']:
                    item_id = self.tree.insert('', tk.END, values=(contact['name'], contact['phone']))
                    self.tree.selection_set(item_id)
                    self.tree.focus(item_id)
                    self.tree.item(item_id, tags=('searched',))
                    break

        self.tree.tag_configure('searched', background='green')

    def get_contact_info(self, contact=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Contact Information")

        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.insert(0, contact['name'] if contact else "")

        tk.Label(dialog, text="Phone:").grid(row=1, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        phone_entry.insert(0, contact['phone'] if contact else "")

        tk.Label(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        email_entry = tk.Entry(dialog)
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        email_entry.insert(0, contact['email'] if contact else "")

        tk.Label(dialog, text="Address:").grid(row=3, column=0, padx=10, pady=10)
        address_entry = tk.Entry(dialog)
        address_entry.grid(row=3, column=1, padx=10, pady=10)
        address_entry.insert(0, contact['address'] if contact else "")

        contact_info = {"name": None, "phone": None, "email": None, "address": None}

        def save():
            contact_info["name"] = name_entry.get()
            contact_info["phone"] = phone_entry.get()
            contact_info["email"] = email_entry.get()
            contact_info["address"] = address_entry.get()
            if all(contact_info.values()):
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "All fields must be filled")

        save_button = tk.Button(dialog, text="Save", command=save)
        save_button.grid(row=4, columnspan=2, pady=10)

        self.root.wait_window(dialog)
        return contact_info if all(contact_info.values()) else None

    def show_all_contacts(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("All Contacts")

        tree = ttk.Treeview(dialog, columns=('Name', 'Phone', 'Email', 'Address'), show='headings', style='Custom.Treeview')
        tree.heading('Name', text='Name')
        tree.heading('Phone', text='Phone')
        tree.heading('Email', text='Email')
        tree.heading('Address', text='Address')
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        for contact in self.contacts:
            tree.insert('', tk.END, values=(contact['name'], contact['phone'], contact['email'], contact['address']))

        close_button = tk.Button(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
