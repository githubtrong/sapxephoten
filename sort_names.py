import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from icu import Collator, Locale

# Thiết lập Collator cho tiếng Việt
collator = Collator.createInstance(Locale("vi_VN"))

def process_names(input_text):
    names = [name.strip() for name in input_text.strip().split("\n") if name.strip()]
    if not names:
        return None, None

    separated_names = []
    for full_name in names:
        parts = full_name.split()
        if len(parts) == 1:
            separated_names.append(("", parts[0]))
        else:
            last_name = " ".join(parts[:-1])
            first_name = parts[-1]
            separated_names.append((last_name, first_name))

    # Sắp xếp theo Collator
    separated_names.sort(key=lambda x: (collator.getSortKey(x[1]), collator.getSortKey(x[0])))

    return names, separated_names

def save_to_file(separated_names):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{'STT':<5}{'Họ':<30}{'Tên':<15}\n")
            f.write("-" * 50 + "\n")
            for i, (last_name, first_name) in enumerate(separated_names, start=1):
                f.write(f"{i:<5}{last_name:<30}{first_name:<15}\n")
        messagebox.showinfo("Thành công", f"Danh sách đã được lưu vào file: {file_path}")

def copy_to_clipboard():
    rows = tree.get_children()
    if not rows:
        messagebox.showwarning("Cảnh báo", "Không có dữ liệu để sao chép!")
        return

    clipboard_text = "STT\tHọ\tTên\n"
    for row in rows:
        stt, last_name, first_name = tree.item(row, 'values')
        clipboard_text += f"{stt}\t{last_name}\t{first_name}\n"

    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    root.update()
    messagebox.showinfo("Thành công", "Dữ liệu đã được sao chép vào clipboard.")

def on_process():
    input_text = text_input.get("1.0", tk.END)
    _, separated_names = process_names(input_text)
    if separated_names is None:
        messagebox.showwarning("Cảnh báo", "Danh sách không hợp lệ hoặc trống!")
        return

    for row in tree.get_children():
        tree.delete(row)

    for i, (last_name, first_name) in enumerate(separated_names, start=1):
        tree.insert("", "end", values=(i, last_name, first_name))

def on_save():
    input_text = text_input.get("1.0", tk.END)
    _, separated_names = process_names(input_text)
    if separated_names is None:
        messagebox.showwarning("Cảnh báo", "Không có danh sách để lưu!")
        return
    save_to_file(separated_names)

# Giao diện chính
root = tk.Tk()
root.title("Quản lý danh sách họ tên")
root.geometry("800x600")

style = ttk.Style()
style.configure("Treeview", font=("Arial", 14))
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_input = tk.Label(frame_input, text="Nhập danh sách họ tên (mỗi tên trên một dòng):", font=("Arial", 14))
label_input.pack(anchor="w")

text_input = tk.Text(frame_input, height=10, width=70, font=("Arial", 14))
text_input.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_process = ttk.Button(frame_buttons, text="Xử lý", command=on_process)
btn_process.grid(row=0, column=0, padx=10)

btn_save = ttk.Button(frame_buttons, text="Lưu vào file", command=on_save)
btn_save.grid(row=0, column=1, padx=10)

btn_copy = ttk.Button(frame_buttons, text="Sao chép", command=copy_to_clipboard)
btn_copy.grid(row=0, column=2, padx=10)

frame_output = tk.Frame(root)
frame_output.pack(pady=20)

label_output = tk.Label(frame_output, text="Kết quả xử lý:", font=("Arial", 14))
label_output.pack(anchor="w")

columns = ("STT", "Họ", "Tên")
tree = ttk.Treeview(frame_output, columns=columns, show="headings", height=15)

tree.heading("STT", text="STT")
tree.heading("Họ", text="Họ")
tree.heading("Tên", text="Tên")

tree.column("STT", width=50, anchor="center")
tree.column("Họ", width=400, anchor="w")
tree.column("Tên", width=200, anchor="w")

tree.pack()

root.mainloop()
