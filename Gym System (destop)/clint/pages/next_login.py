import tkinter as tk

def launch_next_page(gym_app_creator):
    # Welcome Page
    root = tk.Tk()
    root.title("Welcome Page")
    root.geometry("500x450")
    
    # Canvas 1: Header
    canvas1 = tk.Canvas(
        root,
        bg="gray25",
        highlightthickness=0
    )
    canvas1.place(x=0, y=0, width=502, height=80)

    # Canvas 2: Footer
    canvas2 = tk.Canvas(
        root,
        bg="gray25",
        highlightthickness=0
    )
    canvas2.place(x=0, y=372, width=502, height=80)

    # Canvas 3: Main Content Area
    canvas3 = tk.Canvas(
        root,
        bg="linen",
        highlightthickness=2, highlightbackground="black"
    )
    canvas3.place(x=-1, y=80, width=503, height=295)

    # Label: Title
    title_label = tk.Label(
        root,
        text="Welcome to Gym App",
        bg="gray25",
        fg="white",
        font=("Arial", 20, "bold")
    )
    title_label.place(x=100, y=20, width=300, height=40)

    # Button 1: "Open the App"
    button1 = tk.Button(
        root,
        text="Open the App",
        fg="black",
        font=("bold italic", 17),
        bd=2,  # تحديد سمك البوردر
        bg="lightgray",  # لون الخلفية الأساسي
        activebackground="white",  # لون الخلفية عند التفعيل
        activeforeground="red",  # لون النص عند التفعيل
        relief="solid",  # إضافة حواف صلبة
        command=lambda: launch_main_app(root, gym_app_creator)  # الانتقال للنافذة التالية
    )
    button1.place(x=135, y=150, width=250, height=64)

    button2 = tk.Button(
        root,
        text="Visit Our Website",
        fg="black",
        font=("bold italic", 17),
        bd=2,  # تحديد سمك البوردر
        bg="lightgray",  # لون الخلفية الأساسي
        activebackground="white",  
        activeforeground="red",
        relief="solid",  # إضافة حواف صلبة
    )
    button2.place(x=135, y=235, width=250, height=64)


    root.protocol("WM_DELETE_WINDOW", lambda: close_program(root))

    root.mainloop()

def launch_main_app(current_window, gym_app_creator):

    current_window.destroy()
    root = tk.Tk()
    gym_app_creator(root)
    root.mainloop()

def close_program(window):
    window.destroy()
    exit()
