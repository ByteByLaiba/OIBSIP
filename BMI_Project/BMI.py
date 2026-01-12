import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

class HealthTracker:
    def __init__(self, window):
        self.window = window
        self.window.title("Health & Wellness Tracker")
        self.window.geometry("520x620")
        self.window.configure(bg="#ffc8dd")
        
        self.init_db()
        self.build_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def init_db(self):
        try:
            self.db = sqlite3.connect("bmi_data.db")
            self.cur = self.db.cursor()
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
            """)
            self.db.commit()
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Cannot initialize database: {err}")
            self.window.destroy()
    
    def build_ui(self):
        top_frame = tk.Frame(self.window, bg="#cdb4db", height=90)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        tk.Label(
            top_frame,
            text="✨ Health & Wellness Tracker ✨",
            font=("Georgia", 22, "bold"),
            bg="#cdb4db",
            fg="white"
        ).pack(expand=True)
        
        container = tk.Frame(self.window, bg="#ffc8dd")
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        form_box = tk.LabelFrame(
            container,
            text="Your Information",
            font=("Georgia", 13, "bold"),
            bg="#ffafcc",
            fg="#4a4a4a",
            padx=20,
            pady=20
        )
        form_box.pack(fill=tk.X, pady=(0, 18))
        
        tk.Label(form_box, text="Name:", font=("Georgia", 11, "bold"), bg="#ffafcc", fg="#4a4a4a").grid(
            row=0, column=0, sticky="w", pady=8
        )
        self.name_field = tk.Entry(form_box, font=("Georgia", 11), width=28, bd=0, relief=tk.FLAT)
        self.name_field.grid(row=0, column=1, pady=8, padx=12, ipady=4)
        
        tk.Label(form_box, text="Weight (kg):", font=("Georgia", 11, "bold"), bg="#ffafcc", fg="#4a4a4a").grid(
            row=1, column=0, sticky="w", pady=8
        )
        self.weight_field = tk.Entry(form_box, font=("Georgia", 11), width=28, bd=0, relief=tk.FLAT)
        self.weight_field.grid(row=1, column=1, pady=8, padx=12, ipady=4)
        
        tk.Label(form_box, text="Height (m):", font=("Georgia", 11, "bold"), bg="#ffafcc", fg="#4a4a4a").grid(
            row=2, column=0, sticky="w", pady=8
        )
        self.height_field = tk.Entry(form_box, font=("Georgia", 11), width=28, bd=0, relief=tk.FLAT)
        self.height_field.grid(row=2, column=1, pady=8, padx=12, ipady=4)
        
        calc_btn = tk.Button(
            form_box,
            text="Calculate",
            command=self.compute_bmi,
            bg="#cdb4db",
            fg="white",
            font=("Georgia", 13, "bold"),
            cursor="heart",
            bd=0,
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        calc_btn.grid(row=3, column=0, columnspan=2, pady=18)
        self.make_rounded(calc_btn)
        
        self.output_box = tk.LabelFrame(
            container,
            text="Your Results",
            font=("Georgia", 13, "bold"),
            bg="#bde0fe",
            fg="#4a4a4a",
            padx=20,
            pady=20
        )
        self.output_box.pack(fill=tk.X, pady=(0, 18))
        
        self.output_label = tk.Label(
            self.output_box,
            text="Fill in your details and click Calculate",
            font=("Georgia", 12),
            bg="#bde0fe",
            fg="#4a4a4a",
            justify=tk.CENTER
        )
        self.output_label.pack()
        
        action_bar = tk.Frame(container, bg="#ffc8dd")
        action_bar.pack(fill=tk.X)
        
        history_btn = tk.Button(
            action_bar,
            text="💜 History",
            command=self.display_history,
            bg="#a2d2ff",
            fg="white",
            font=("Georgia", 11, "bold"),
            cursor="heart",
            bd=0,
            relief=tk.FLAT,
            width=13,
            pady=8
        )
        history_btn.pack(side=tk.LEFT, padx=6)
        self.make_rounded(history_btn)
        
        chart_btn = tk.Button(
            action_bar,
            text="📊 Chart",
            command=self.display_chart,
            bg="#cdb4db",
            fg="white",
            font=("Georgia", 11, "bold"),
            cursor="heart",
            bd=0,
            relief=tk.FLAT,
            width=13,
            pady=8
        )
        chart_btn.pack(side=tk.LEFT, padx=6)
        self.make_rounded(chart_btn)
        
        clear_btn = tk.Button(
            action_bar,
            text="🗑️ Clear All",
            command=self.erase_all,
            bg="#ffafcc",
            fg="white",
            font=("Georgia", 11, "bold"),
            cursor="heart",
            bd=0,
            relief=tk.FLAT,
            width=13,
            pady=8
        )
        clear_btn.pack(side=tk.LEFT, padx=6)
        self.make_rounded(clear_btn)
        
        self.window.bind('<Return>', lambda event: self.compute_bmi())
    
    def make_rounded(self, widget):
        widget.config(highlightthickness=0)
    
    def compute_bmi(self):
        try:
            user_name = self.name_field.get().strip()
            weight_input = self.weight_field.get().strip()
            height_input = self.height_field.get().strip()
            
            if not user_name:
                messagebox.showwarning("Missing Info", "Please enter your name")
                self.name_field.focus()
                return
            
            if not weight_input:
                messagebox.showwarning("Missing Info", "Please enter your weight")
                self.weight_field.focus()
                return
            
            if not height_input:
                messagebox.showwarning("Missing Info", "Please enter your height")
                self.height_field.focus()
                return
            
            user_weight = float(weight_input)
            user_height = float(height_input)
            
            if user_weight <= 0:
                messagebox.showerror("Invalid", "Weight must be positive")
                self.weight_field.focus()
                return
            
            if user_height <= 0:
                messagebox.showerror("Invalid", "Height must be positive")
                self.height_field.focus()
                return
            
            if user_height > 3:
                messagebox.showwarning("Check Input", "Height seems high. Use meters (e.g., 1.65)")
                self.height_field.focus()
                return
            
            result = user_weight / (user_height ** 2)
            result = round(result, 2)
            
            if result < 18.5:
                status = "Underweight"
                shade = "#5a9fd4"
                tip = "Consider a nutritious diet to gain healthy weight."
            elif result < 25:
                status = "Normal"
                shade = "#6b5b95"
                tip = "Amazing! Keep up your healthy habits."
            elif result < 30:
                status = "Overweight"
                shade = "#d96098"
                tip = "Try balanced meals and regular activity."
            else:
                status = "Obese"
                shade = "#c44569"
                tip = "Please talk to a healthcare provider."
            
            self.output_label.config(
                text=f"BMI: {result}\nStatus: {status}\n\n{tip}",
                fg=shade,
                font=("Georgia", 12, "bold")
            )
            
            self.cur.execute(
                "INSERT INTO bmi_records VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (user_name, user_weight, user_height, result, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.db.commit()
            
            messagebox.showinfo("Success", f"BMI saved successfully!\n\nBMI: {result}\nStatus: {status}")
            
        except ValueError:
            messagebox.showerror("Invalid", "Please enter valid numbers")
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Cannot save: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")
    
    def display_history(self):
        try:
            self.cur.execute(
                "SELECT id, name, bmi, category, date FROM bmi_records ORDER BY date DESC"
            )
            data = self.cur.fetchall()
            
            if not data:
                messagebox.showinfo("No Data", "No history available")
                return
            
            hist_win = tk.Toplevel(self.window)
            hist_win.title("History - All Users")
            hist_win.geometry("720x420")
            hist_win.configure(bg="#ffc8dd")
            
            tk.Label(
                hist_win,
                text="BMI History for Everyone",
                font=("Georgia", 15, "bold"),
                bg="#ffc8dd",
                fg="#4a4a4a"
            ).pack(pady=12)
            
            list_frame = tk.Frame(hist_win, bg="#ffc8dd")
            list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
            
            scroll = ttk.Scrollbar(list_frame)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            table = ttk.Treeview(
                list_frame,
                columns=("Name", "Date", "BMI", "Category"),
                show="headings",
                yscrollcommand=scroll.set
            )
            table.pack(fill=tk.BOTH, expand=True)
            
            scroll.config(command=table.yview)
            
            table.heading("Name", text="Name")
            table.heading("Date", text="Date & Time")
            table.heading("BMI", text="BMI")
            table.heading("Category", text="Category")
            
            table.column("Name", width=160)
            table.column("Date", width=210)
            table.column("BMI", width=110)
            table.column("Category", width=160)
            
            for item in data:
                table.insert("", tk.END, values=(item[1], item[4], item[2], item[3]))
            
            def remove_item():
                chosen = table.selection()
                if not chosen:
                    messagebox.showwarning("No Selection", "Select a record first")
                    return
                
                if messagebox.askyesno("Confirm", "Delete selected record(s)?"):
                    for selected in chosen:
                        vals = table.item(selected)['values']
                        self.cur.execute(
                            "DELETE FROM bmi_records WHERE name=? AND date=? AND bmi=?",
                            (vals[0], vals[1], vals[2])
                        )
                        table.delete(selected)
                    self.db.commit()
                    messagebox.showinfo("Done", "Record(s) deleted")
            
            del_btn = tk.Button(
                hist_win,
                text="Delete Selected",
                command=remove_item,
                bg="#ffafcc",
                fg="white",
                font=("Georgia", 11, "bold"),
                bd=0,
                relief=tk.FLAT,
                pady=8
            )
            del_btn.pack(pady=12)
            self.make_rounded(del_btn)
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Cannot load history: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")
    
    def display_chart(self):
        user_name = self.name_field.get().strip()
        
        if not user_name:
            messagebox.showwarning("Missing Info", "Enter a name to view their chart")
            self.name_field.focus()
            return
        
        try:
            self.cur.execute(
                "SELECT bmi, date FROM bmi_records WHERE name=? ORDER BY date",
                (user_name,)
            )
            data = self.cur.fetchall()
            
            if not data:
                messagebox.showinfo("No Data", f"No records for {user_name}")
                return
            
            if len(data) < 2:
                messagebox.showinfo("Need More Data", f"{user_name} needs at least 2 records")
                return
            
            values = [item[0] for item in data]
            timestamps = [datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S") for item in data]
            
            chart_win = tk.Toplevel(self.window)
            chart_win.title(f"BMI Chart - {user_name}")
            chart_win.geometry("820x620")
            
            figure, axis = plt.subplots(figsize=(10, 6))
            axis.plot(timestamps, values, marker='o', linestyle='-', linewidth=2, markersize=8, color="#cdb4db")
            
            axis.axhline(y=18.5, color='#a2d2ff', linestyle='--', alpha=0.7, label='Underweight')
            axis.axhline(y=25, color='#cdb4db', linestyle='--', alpha=0.7, label='Normal')
            axis.axhline(y=30, color='#ffafcc', linestyle='--', alpha=0.7, label='Overweight')
            
            axis.set_xlabel("Date", fontsize=12, fontweight='bold')
            axis.set_ylabel("BMI", fontsize=12, fontweight='bold')
            axis.set_title(f"BMI Progress for {user_name}", fontsize=14, fontweight='bold')
            axis.grid(True, alpha=0.3)
            axis.legend()
            
            axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            figure.autofmt_xdate()
            
            display = FigureCanvasTkAgg(figure, master=chart_win)
            display.draw()
            display.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Cannot load data: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")
    
    def erase_all(self):
        try:
            self.cur.execute("SELECT COUNT(*) FROM bmi_records")
            total = self.cur.fetchone()[0]
            
            if total == 0:
                messagebox.showinfo("No Data", "Database is empty")
                return
            
            if messagebox.askyesno(
                "Confirm Deletion",
                f"Delete ALL {total} record(s)?\nThis cannot be undone!"
            ):
                self.cur.execute("DELETE FROM bmi_records")
                self.db.commit()
                messagebox.showinfo("Done", "All records deleted")
                self.output_label.config(text="Fill in your details and click Calculate", fg="#4a4a4a")
        
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Cannot clear: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"Something went wrong: {err}")
    
    def exit_app(self):
        try:
            self.db.close()
        except:
            pass
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTracker(root)
    root.mainloop()