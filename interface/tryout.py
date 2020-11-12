import tkinter as tk

m = tk.Tk()
m.title('Trial')
button = tk.Button(m, text = 'Hallo!', command = m.destroy)
button.pack()
m.mainloop()