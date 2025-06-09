import tkinter as tk
from tkinter import ttk, messagebox
from contacts import ContactManager

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng quản lý danh bạ")

        self.manager = ContactManager()
        self.selected_index = None

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # --- Form nhập ---
        tk.Label(root, text="Họ tên:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(root, text="Số điện thoại:").grid(row=1, column=0)
        phone_entry = tk.Entry(root, textvariable=self.phone_var, validate="key")
        phone_entry['validatecommand'] = (root.register(self.validate_phone), '%P')
        phone_entry.grid(row=1, column=1)

        tk.Label(root, text="Email:").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.email_var).grid(row=2, column=1)

        # --- Buttons ---
        tk.Button(root, text="Thêm", command=self.add_contact, bg='#90ee90').grid(row=3, column=0)
        tk.Button(root, text="Sửa", command=self.edit_contact, bg='#90ee90').grid(row=3, column=1)
        tk.Button(root, text="Xoá", command=self.delete_contact, bg='#ff7f7f').grid(row=3, column=2)

        # --- Tìm kiếm ---
        tk.Label(root, text="Tìm theo tên:").grid(row=4, column=0)
        tk.Entry(root, textvariable=self.search_var).grid(row=4, column=1)
        tk.Button(root, text="Tìm", command=self.search_contact, bg='#90ee90').grid(row=4, column=2)
        tk.Button(root, text="Tải lại", command=self.load_data, bg='#90ee90').grid(row=4, column=3)

        # --- Bảng Treeview ---
        self.tree = ttk.Treeview(root, columns=('Name', 'Phone', 'Email'), show='headings')
        self.tree.heading('Name', text='Họ tên')
        self.tree.heading('Phone', text='Số điện thoại')
        self.tree.heading('Email', text='Email')
        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        self.load_data()

    def validate_phone(self, value):
        return value.isdigit() or value == ""

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        sorted_contacts = sorted(self.manager.contacts, key=lambda c: c['name'].lower())
        for contact in sorted_contacts:
            self.tree.insert('', tk.END, values=(contact['name'], contact['phone'], contact['email']))
        self.clear_form()

    def clear_form(self):
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.selected_index = None

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            sorted_contacts = sorted(self.manager.contacts, key=lambda c: c['name'].lower())
            contact = sorted_contacts[index]
            self.name_var.set(contact['name'])
            self.phone_var.set(contact['phone'])
            self.email_var.set(contact['email'])
            self.selected_index = self.manager.contacts.index(contact)

    def add_contact(self):
        contact = {
            'name': self.name_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip()
        }

        if not contact['name'] or not contact['phone']:
            messagebox.showwarning("Lỗi", "Tên và số điện thoại không được để trống.")
            return

        if not contact['phone'].isdigit():
            messagebox.showerror("Sai định dạng", "Số điện thoại chỉ được chứa số.")
            return

        for existing in self.manager.contacts:
            if contact['name'].lower() == existing['name'].lower():
                messagebox.showerror("Trùng tên", "Tên này đã tồn tại trong danh bạ.")
                return
            if contact['phone'] == existing['phone']:
                messagebox.showerror("Trùng số điện thoại", "Số điện thoại này đã tồn tại trong danh bạ.")
                return

        self.manager.add_contact(contact)
        self.load_data()

    def edit_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Chưa chọn", "Hãy chọn liên hệ để sửa.")
            return

        new_contact = {
            'name': self.name_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip()
        }

        if not new_contact['phone'].isdigit():
            messagebox.showerror("Sai định dạng", "Số điện thoại chỉ được chứa số.")
            return

        self.manager.update_contact(self.selected_index, new_contact)
        self.load_data()

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Chưa chọn", "Hãy chọn liên hệ để xoá.")
            return

        confirm = messagebox.askyesno("Xác nhận xoá", "Bạn có chắc muốn xoá liên hệ này?")
        if confirm:
            self.manager.delete_contact(self.selected_index)
            self.load_data()

    def highlight_match(self, name, keyword):
        parts = name.split()
        highlighted_parts = []
        for part in parts:
            if part.lower().startswith(keyword):
                highlighted_parts.append(part.upper())
            else:
                highlighted_parts.append(part)
        return ' '.join(highlighted_parts)

    def search_contact(self):
        keyword = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())

        def match(name):
            return any(part.startswith(keyword) for part in name.lower().split())

        filtered = [c for c in self.manager.contacts if match(c['name'])]
        sorted_filtered = sorted(filtered, key=lambda c: c['name'].lower())

        for contact in sorted_filtered:
            highlighted_name = self.highlight_match(contact['name'], keyword)
            self.tree.insert('', tk.END, values=(highlighted_name, contact['phone'], contact['email']))

# --- Chạy chương trình ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
