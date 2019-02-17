
import tkinter as tk
def toggle():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    if t_btn.config('text')[-1] == 'Pause':
        t_btn.config(text='Continue')
    else:
        t_btn.config(text='Pause')
root = tk.Tk()
t_btn = tk.Button(text="Pause", width=12, command=toggle)
t_btn.pack(pady=5)
root.mainloop()
