import ctypes
import tkinter as tk
from tkinter import messagebox, ttk

# Enable High-DPI Scaling for crisp fonts on high-resolution screens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class DreamyTodoListApp:

    def __init__(self, root):
        self.root = root

        # ---------------- WINDOW SETTINGS ----------------
        self.root.title("Dreamy To-Do List")
        self.root.geometry("520x700")
        self.root.minsize(380, 550)  # Fits small screens / mobile desktop tools
        self.root.configure(bg="#FEF0F5")  # Soft Blush Pink

        self.tasks = []

        # Configure Progressbar Style
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Dreamy.Horizontal.TProgressbar",
            thickness=14,
            troughcolor="#FDE7F0",
            background="#ED78A0",
            borderwidth=0,
            relief="flat",
        )

        self.create_interface()

    def create_interface(self):
        # Scrollable Main Canvas
        self.container_canvas = tk.Canvas(
            self.root, bg="#FEF0F5", highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.container_canvas.yview,
            bg="#FEF0F5",
        )

        self.main_frame = tk.Frame(self.container_canvas, bg="#FEF0F5")
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.container_canvas.configure(
                scrollregion=self.container_canvas.bbox("all")
            ),
        )

        self.canvas_window = self.container_canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )
        self.container_canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        # Make main container stretch dynamically with window width
        self.container_canvas.bind(
            "<Configure>",
            lambda event: self.container_canvas.itemconfig(
                self.canvas_window, width=event.width
            ),
        )

        self.container_canvas.pack(
            side="left", fill="both", expand=True, padx=8, pady=5
        )
        self.scrollbar.pack(side="right", fill="y")

        # Enable MouseWheel scrolling
        self.root.bind_all(
            "<MouseWheel>",
            lambda event: self.container_canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"
            ),
        )

        # ---------------- HEADER AREA ----------------
        header_frame = tk.Frame(self.main_frame, bg="#FEF0F5")
        header_frame.pack(fill="x", pady=(10, 5))

        # Sticky Note (Left) - Uses Label for clean auto-wrap
        sticky_note = tk.Label(
            header_frame,
            text="Small steps\nbig dreams ♡",
            font=("Times New Roman", 9),
            bg="#FEFAF8",
            fg="#793252",
            padx=10,
            pady=8,
            relief="solid",
            bd=1,
            highlightbackground="#FDCEDD",
        )
        sticky_note.pack(side="left", padx=5)

        # Title & Subtitle (Center)
        center_title_frame = tk.Frame(header_frame, bg="#FEF0F5")
        center_title_frame.pack(side="left", expand=True, fill="x")

        title = tk.Label(
            center_title_frame,
            text="🎀 To-Do List",
            font=("Times New Roman", 20),
            bg="#FEF0F5",
            fg="#793252",
        )
        title.pack()

        subtitle = tk.Label(
            center_title_frame,
            text="Plan today ✨ Achieve tomorrow ♡",
            font=("Times New Roman", 10),
            bg="#FEF0F5",
            fg="#793252",
        )
        subtitle.pack(pady=2)

        # ---------------- INPUT CARD ----------------
        input_card = tk.Frame(
            self.main_frame,
            bg="#FEFAF8",
            padx=10,
            pady=8,
            highlightbackground="#FDCEDD",
            highlightthickness=2,
        )
        input_card.pack(fill="x", pady=10, padx=5)

        heart_icon = tk.Label(
            input_card,
            text="♡",
            font=("Times New Roman", 12),
            bg="#FEFAF8",
            fg="#793252",
        )
        heart_icon.pack(side="left", padx=(2, 5))

        self.task_entry = tk.Entry(
            input_card,
            font=("Times New Roman", 11),
            bg="#FEFAF8",
            fg="#793252",
            insertbackground="#793252",
            bd=0,
            relief="flat",
        )
        self.task_entry.insert(0, "What do you want to do today? ✨")
        self.task_entry.bind(
            "<FocusIn>",
            lambda e: self.task_entry.delete(0, tk.END)
            if self.task_entry.get() == "What do you want to do today? ✨"
            else None,
        )
        self.task_entry.pack(
            side="left", fill="x", expand=True, padx=5, ipady=4
        )

        add_button = tk.Button(
            input_card,
            text="+ Add Task",
            font=("Times New Roman", 10),
            bg="#ED78A0",
            fg="white",
            activebackground="#D9658D",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.add_task,
        )
        add_button.pack(side="right")

        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # ---------------- TASKS CONTAINER ----------------
        tasks_header_frame = tk.Frame(self.main_frame, bg="#FEF0F5")
        tasks_header_frame.pack(fill="x", padx=5, pady=(5, 0))

        tk.Label(
            tasks_header_frame,
            text="💖 Your Tasks 💖",
            font=("Times New Roman", 12),
            bg="#FEF0F5",
            fg="#793252",
        ).pack(side="left")
        tk.Label(
            tasks_header_frame,
            text="🌱 Progress creates results ♡",
            font=("Times New Roman", 9),
            bg="#FEF0F5",
            fg="#793252",
        ).pack(side="right")

        list_container = tk.Frame(
            self.main_frame,
            bg="#FEFAF8",
            padx=2,
            pady=2,
            highlightbackground="#FDCEDD",
            highlightthickness=2,
        )
        list_container.pack(fill="x", padx=5, pady=5)

        # Empty State Placeholder
        self.empty_state_frame = tk.Frame(
            list_container, bg="#FEFAF8", height=130
        )
        self.empty_state_frame.pack(fill="both", expand=True, pady=15)

        tk.Label(
            self.empty_state_frame,
            text="♡",
            font=("Times New Roman", 22),
            bg="#FEFAF8",
            fg="#ED78A0",
        ).pack()

        tk.Label(
            self.empty_state_frame,
            text="No tasks yet!",
            font=("Times New Roman", 12),
            bg="#FEFAF8",
            fg="#793252",
        ).pack(pady=(2, 0))
        
        # Fixed syntax issue (removed extra double comma from line 271)
        tk.Label(
            self.empty_state_frame,
            text="Add your first task and make it happen! ♡",
            font=("Times New Roman", 10),
            bg="#FEFAF8",
            fg="#793252",
        ).pack()

        # Task Listbox
        list_scrollbar = tk.Scrollbar(list_container, bg="#FDE7F0")
        self.task_listbox = tk.Listbox(
            list_container,
            height=6,
            font=("Times New Roman", 11),
            bg="#FEFAF8",
            fg="#793252",
            selectbackground="#FDCEDD",
            selectforeground="#793252",
            activestyle="none",
            bd=0,
            relief="flat",
            highlightthickness=0,
            yscrollcommand=list_scrollbar.set,
        )
        list_scrollbar.config(command=self.task_listbox.yview)

        # ---------------- ACTION BUTTONS (RESPONSIVE GRID) ----------------
        button_frame = tk.Frame(self.main_frame, bg="#FEF0F5")
        button_frame.pack(fill="x", pady=8, padx=5)

        # Standard Tkinter buttons with wrap enabled so text stays visible on narrow screens
        complete_btn = tk.Button(
            button_frame,
            text="✓ Complete ♡",
            font=("Times New Roman", 10),
            bg="#ED78A0",
            fg="white",
            activebackground="#D9658D",
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.complete_task,
        )
        complete_btn.pack(side="left", expand=True, fill="x", padx=(0, 3))

        remove_btn = tk.Button(
            button_frame,
            text="✕ Remove ♡",
            font=("Times New Roman", 10),
            bg="#FDCEDD",
            fg="#793252",
            activebackground="#FDE7F0",
            activeforeground="#793252",
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.remove_task,
        )
        remove_btn.pack(side="left", expand=True, fill="x", padx=(3, 3))

        clear_btn = tk.Button(
            button_frame,
            text="🧹 Clear Completed ♡",
            font=("Times New Roman", 10),
            bg="#B293DD",
            fg="white",
            activebackground="#9A7BC4",
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.clear_completed,
        )
        clear_btn.pack(side="left", expand=True, fill="x", padx=(3, 0))

        # ---------------- PROGRESS SECTION ----------------
        progress_card = tk.Frame(
            self.main_frame,
            bg="#FEFAF8",
            padx=12,
            pady=10,
            highlightbackground="#FDCEDD",
            highlightthickness=1,
        )
        progress_card.pack(fill="x", pady=5, padx=5)

        progress_header = tk.Frame(progress_card, bg="#FEFAF8")
        progress_header.pack(fill="x")

        tk.Label(
            progress_header,
            text="📊 Progress Tracking ♡",
            font=("Times New Roman", 11),
            bg="#FEFAF8",
            fg="#793252",
        ).pack(side="left")
        tk.Label(
            progress_header,
            text="✨ You got this ♡",
            font=("Times New Roman", 9),
            bg="#FEFAF8",
            fg="#793252",
        ).pack(side="right")

        self.progress = ttk.Progressbar(
            progress_card,
            orient="horizontal",
            mode="determinate",
            style="Dreamy.Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", pady=6)

        progress_info_frame = tk.Frame(progress_card, bg="#FEFAF8")
        progress_info_frame.pack(fill="x")

        self.progress_label = tk.Label(
            progress_info_frame,
            text="♡ 0% Completed",
            font=("Times New Roman", 9),
            bg="#FEFAF8",
            fg="#793252",
        )
        self.progress_label.pack(side="left")

        self.task_counter = tk.Label(
            progress_info_frame,
            text="🌸 Total Tasks: 0 | Completed: 0",
            font=("Times New Roman", 9),
            bg="#FEFAF8",
            fg="#793252",
        )
        self.task_counter.pack(side="right")

        # ---------------- FOOTER & EXIT ----------------
        footer_frame = tk.Frame(self.main_frame, bg="#FEF0F5")
        footer_frame.pack(fill="x", pady=(10, 15))

        exit_btn = tk.Button(
            footer_frame,
            text="🚪 Exit Application",
            font=("Times New Roman", 10),
            bg="#FEFAF8",
            fg="#793252",
            activebackground="#FDE7F0",
            activeforeground="#793252",
            relief="solid",
            bd=1,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.exit_application,
        )
        exit_btn.pack()

        tk.Label(
            footer_frame,
            text="Better days are coming ♡",
            font=("Times New Roman", 9),
            bg="#FEF0F5",
            fg="#793252",
        ).pack(pady=(5, 0))

    # =====================================================
    # LOGIC FUNCTIONS
    # =====================================================

    def add_task(self):
        task = self.task_entry.get().strip()

        if not task or task == "What do you want to do today? ✨":
            messagebox.showwarning(
                "Empty Task", "Please enter a task before adding ♡"
            )
            return

        self.tasks.append({"name": task, "completed": False})
        self.task_entry.delete(0, tk.END)

        self.update_task_list()
        self.update_progress()

    def update_task_list(self):
        if len(self.tasks) == 0:
            self.task_listbox.pack_forget()
            self.empty_state_frame.pack(fill="both", expand=True, pady=15)
        else:
            self.empty_state_frame.pack_forget()
            self.task_listbox.pack(
                side="left", fill="both", expand=True, padx=5, pady=5
            )

            self.task_listbox.delete(0, tk.END)
            for index, task in enumerate(self.tasks, start=1):
                status = "✓" if task["completed"] else "○"
                self.task_listbox.insert(
                    tk.END, f" {status}   {index}.  {task['name']}"
                )

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning(
                "Select Task", "Please select a task to mark as completed ♡"
            )
            return

        index = selected[0]
        if self.tasks[index]["completed"]:
            messagebox.showinfo(
                "Already Completed", "This task is already completed ♡"
            )
            return

        self.tasks[index]["completed"] = True
        self.update_task_list()
        self.update_progress()

    def remove_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning(
                "Select Task", "Please select a task to remove ♡"
            )
            return

        index = selected[0]
        task_name = self.tasks[index]["name"]

        answer = messagebox.askyesno(
            "Remove Task", f"Do you want to remove:\n\n{task_name}?"
        )
        if answer:
            self.tasks.pop(index)
            self.update_task_list()
            self.update_progress()

    def clear_completed(self):
        completed_tasks = [t for t in self.tasks if t["completed"]]
        if not completed_tasks:
            messagebox.showinfo(
                "No Completed Tasks", "There are no completed tasks to clear ♡"
            )
            return

        if messagebox.askyesno(
            "Clear Completed", "Remove all completed tasks?"
        ):
            self.tasks = [t for t in self.tasks if not t["completed"]]
            self.update_task_list()
            self.update_progress()

    def update_progress(self):
        total = len(self.tasks)
        completed = sum(t["completed"] for t in self.tasks)
        pct = (completed / total * 100) if total > 0 else 0

        self.progress["value"] = pct
        self.progress_label.config(text=f"♡ {pct:.0f}% Completed")
        self.task_counter.config(
            text=f"🌸 Total Tasks: {total} | Completed: {completed}"
        )

    def exit_application(self):
        if messagebox.askyesno(
            "Exit Application", "Are you sure you want to exit? ♡"
        ):
            self.root.destroy()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = DreamyTodoListApp(root)
    root.mainloop()