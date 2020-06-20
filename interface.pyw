import tkinter as tk

window = tk.Tk()

window.title('GTA V Horse Race Auto bet')
window.geometry("400x200+10+20")

app_status_label = tk.Label(window, text="App Status: disabled")
app_status_label.pack(anchor=tk.NW)

status_button = tk.Button(window, text="This is Button widget")
status_button.bind('<Button-1>', lambda *e: status_button.config(text='Pipo'))
status_button.pack(anchor=tk.S)

# btn.place(x=80, y=100)



window.mainloop()
