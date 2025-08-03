import tkinter as tk
from tkinter import messagebox, simpledialog
import contacts_manager as cm

contacts = cm.load_contacts()

def update_listbox():
    listbox.delete(0, tk.END)
    for name, phone in contacts.items():
        listbox.insert(tk.END, f"{name} → {phone}")

def add_contact():
    name = simpledialog.askstring("Add Contact", "Enter contact name:")
    if not name:
        return
    phone = simpledialog.askstring("Add Contact", "Enter phone number:")
    if not phone:
        return
    if cm.add_contact(contacts, name, phone):
        update_listbox()
        messagebox.showinfo("Success", f"Contact '{name}' added.")
    else:
        messagebox.showwarning("Warning", "Contact already exists.")

def edit_contact():
    try:
        selection = listbox.get(listbox.curselection())
        old_name = selection.split(" → ")[0]
    except tk.TclError:
        messagebox.showwarning("Warning", "Please select a contact to edit.")
        return

    new_name = simpledialog.askstring("Edit Contact", "Enter new name:", initialvalue=old_name)
    if not new_name:
        return
    new_phone = simpledialog.askstring("Edit Contact", "Enter new phone number:", initialvalue=contacts[old_name])
    if not new_phone:
        return

    if cm.edit_contact(contacts, old_name, new_name, new_phone):
        update_listbox()
        messagebox.showinfo("Success", f"Contact '{old_name}' updated.")
    else:
        messagebox.showwarning("Warning", "Edit failed (duplicate name or contact not found).")

def delete_contact():
    try:
        selection = listbox.get(listbox.curselection())
        name = selection.split(" → ")[0]
    except tk.TclError:
        messagebox.showwarning("Warning", "Please select a contact to delete.")
        return

    if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete '{name}'?"):
        if cm.delete_contact(contacts, name):
            update_listbox()
            messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")
        else:
            messagebox.showwarning("Warning", "Delete failed.")

def search_contact():
    query = simpledialog.askstring("Search Contact", "Enter name to search:")
    if not query:
        return
    result = {name: phone for name, phone in contacts.items() if query.lower() in name.lower()}
    listbox.delete(0, tk.END)
    for name, phone in result.items():
        listbox.insert(tk.END, f"{name} → {phone}")
    if not result:
        messagebox.showinfo("Search", "No contacts found.")

def reset_list():
    update_listbox()

root = tk.Tk()
root.title("Phonebook App")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

listbox = tk.Listbox(frame, width=40, height=15)
listbox.pack(side=tk.LEFT, padx=(0,10))

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", width=15, command=add_contact).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Edit Contact", width=15, command=edit_contact).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Delete Contact", width=15, command=delete_contact).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Search", width=15, command=search_contact).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Show All", width=15, command=reset_list).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=1, column=2, padx=5, pady=5)

update_listbox()

root.mainloop()
