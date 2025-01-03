import random
import string
import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Helper functions for encryption and decryption
def derive_key(password):
    chars = "".join(sorted(set(" " + string.punctuation + string.digits + string.ascii_letters + string.whitespace)))
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    random.seed(hashed_password)  # Seed random with the hashed password
    key = list(chars)
    random.shuffle(key)  # Shuffle consistently based on the password
    return chars, key

def encrypt_message(plain_text, key, chars):
    cipher_text = ""
    for letter in plain_text:
        try:
            index = chars.index(letter)
            cipher_text += key[index]
        except ValueError:
            raise ValueError(f"Character '{letter}' is not supported for encryption.")
    return cipher_text

def decrypt_message(cipher_text, key, chars):
    plain_text = ""
    for letter in cipher_text:
        try:
            index = key.index(letter)
            plain_text += chars[index]
        except ValueError:
            raise ValueError(f"Character '{letter}' is not supported for decryption.")
    return plain_text

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def save_message_to_file(filename, message, encrypted=False):
    folder_path = "messages"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path, filename), "w") as f:
        f.write("Encrypted: " + str(encrypted) + "\n")
        f.write("Message: " + message + "\n")
    messagebox.showinfo("Success", f"Message saved to {filename}")

# GUI application
def main():
    def encrypt_action():
        plain_text = input_text.get("1.0", tk.END).strip()
        if not plain_text:
            messagebox.showerror("Error", "Please enter a message to encrypt.")
            return

        encryption_password = password_entry.get()
        if not encryption_password:
            messagebox.showerror("Error", "Please set a password for encryption.")
            return

        try:
            chars, key = derive_key(encryption_password)
            cipher_text = encrypt_message(plain_text, key, chars)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", cipher_text)
            messagebox.showinfo("Success", "Message encrypted successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def decrypt_action():
        cipher_text = input_text.get("1.0", tk.END).strip()
        if not cipher_text:
            messagebox.showerror("Error", "Please enter a message to decrypt.")
            return

        decryption_password = password_entry.get()
        if not decryption_password:
            messagebox.showerror("Error", "Please enter the password used for encryption.")
            return

        try:
            chars, key = derive_key(decryption_password)
            plain_text = decrypt_message(cipher_text, key, chars)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", plain_text)
            messagebox.showinfo("Success", "Message decrypted successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def generate_password_action():
        length = password_length_spinbox.get()
        if not length.isdigit():
            messagebox.showerror("Error", "Please enter a valid password length.")
            return

        password = generate_random_password(int(length))
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", password)

    def save_action():
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filename:
            return

        message = output_text.get("1.0", tk.END).strip()
        save_message_to_file(filename, message, encrypted=True)

    # Create main window
    root = tk.Tk()
    root.title("Encryption/Decryption Manager")

    # Input message
    tk.Label(root, text="Input Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    input_text = tk.Text(root, height=5, width=50, wrap="word")
    input_text.grid(row=0, column=1, padx=5, pady=5)

    # Password entry
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    password_entry = tk.Entry(root, show="*", width=50)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Output message
    tk.Label(root, text="Output Message:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    output_text = tk.Text(root, height=5, width=50, wrap="word")
    output_text.grid(row=2, column=1, padx=5, pady=5)

    # Password length for random generation
    tk.Label(root, text="Password Length:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    password_length_spinbox = tk.Spinbox(root, from_=6, to=64, width=10)
    password_length_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Buttons
    encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_action, bg="red", fg="white", width=15)
    encrypt_button.grid(row=4, column=0, padx=5, pady=5)

    decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_action, bg="green", fg="white", width=15)
    decrypt_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    generate_password_button = tk.Button(root, text="Generate Password", command=generate_password_action, bg="black", fg="white", width=20)
    generate_password_button.grid(row=5, column=0, padx=5, pady=5)

    save_button = tk.Button(root, text="Save Encrypted File", command=save_action, bg="blue", fg="white", width=20)
    save_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
