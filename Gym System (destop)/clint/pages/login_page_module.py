import tkinter as tk  # مكتبة لإنشاء واجهات رسومية في بايثون
from tkinter import messagebox  # مكتبة لعرض رسائل صغيرة مثل تنبيه أو خطأ
from PIL import Image, ImageTk  # لتعامل مع الصور

class LoginPage:  # تعريف كلاس لإنشاء صفحة تسجيل الدخول
    def __init__(self, root, launch_next_page_callback):  # دالة المُشيد لاستقبال النافذة وجلب وظيفة الانتقال للصفحة التالية
        self.root = root  # تخزين النافذة الرئيسية
        self.launch_next_page_callback = launch_next_page_callback  # وظيفة الانتقال للصفحة التالية
        self.root.title("Login to go gym")  # تحديد عنوان النافذة
        self.root.geometry("500x500")  # ضبط أبعاد النافذة

        # Load and add the background image
        self.bg_image = Image.open("C:/Users/vip/Desktop/Gym System (destop)/gymbg.png")         
        self.bg_image = self.bg_image.resize((450, 400))  # تغيير حجم الصورة لتناسب النافذة
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  # تحويل الصورة لتنسيق يتوافق مع Tkinter
        self.bg_label = tk.Label(self.root, image=self.bg_photo)  # إنشاء عنصر لعرض الصورة
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # وضع الصورة بحيث تغطي النافذة بالكامل

        self.username_var = tk.StringVar()  # متغير لتخزين اسم المستخدم
        self.password_var = tk.StringVar()  # متغير لتخزين كلمة المرور

        # Labels and Entries for Username and Password
        tk.Label(self.root, text="Username", font=("Arial", 14),).place(x=200, y=180)  # نص إدخال اسم المستخدم
        tk.Entry(self.root, textvariable=self.username_var, font=("Arial", 14), width=20).place(x=130, y=220)  # حقل إدخال اسم المستخدم

        tk.Label(self.root, text="Password", font=("Arial", 14),).place(x=200, y=260)  # نص إدخال كلمة المرور
        tk.Entry(self.root, textvariable=self.password_var, font=("Arial", 14), width=20).place(x=130, y=300)  # حقل إدخال كلمة المرور

        # Login Button
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.login, fg="black", width=11, bd=3, activebackground="white", activeforeground="red",).place(x=180, y=360)  
        # زر تسجيل الدخول مع تحديد شكل الخط وخلفيته وتأثيرات عند الضغط عليه

        # Handle closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)  # التعامل مع إغلاق النافذة

    def login(self):  # دالة تسجيل الدخول
        username = self.username_var.get()  # جلب اسم المستخدم من الحقل
        password = self.password_var.get()  # جلب كلمة المرور من الحقل

        if username == "" or password == "":  # التحقق من أن الحقول ليست فارغة
            messagebox.showerror("Error", "Please enter both username and password.")  # رسالة خطأ إذا الحقول فارغة
        elif username == "admin" and password == "admin":  # تحقق من بيانات الدخول
            self.root.destroy()  # إغلاق نافذة تسجيل الدخول
            self.launch_next_page_callback()  # الانتقال للصفحة التالية
        else:  # إذا كانت البيانات خاطئة
            messagebox.showerror("Error", "Invalid credentials")  # رسالة خطأ للبيانات غير الصحيحة

    def close_program(self):  # دالة لإغلاق البرنامج بالكامل
        self.root.destroy()  # إغلاق النافذة
        exit()  # إنهاء البرنامج
