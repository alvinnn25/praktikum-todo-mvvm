import tkinter as tk
from tkinter import messagebox
from typing import List, Optional
from Model.task import Task
from ViewModel.task_viewmodel import TaskViewModel


class TaskView:
    # Palet warna modern
    BG_COLOR = "#F3F4F6"
    CARD_COLOR = "#FFFFFF"
    PRIMARY_COLOR = "#4F46E5"
    PRIMARY_HOVER = "#4338CA"
    SUCCESS_COLOR = "#10B981"
    SUCCESS_HOVER = "#059669"
    DANGER_COLOR = "#EF4444"
    DANGER_HOVER = "#DC2626"
    TEXT_PRIMARY = "#1F2937"
    TEXT_MUTED = "#9CA3AF"
    SELECT_BG = "#EEF2FF"
    BORDER_COLOR = "#E5E7EB"

    PLACEHOLDER_TEXT = "Tulis tugas baru di sini..."

    def __init__(self, root: tk.Tk, viewmodel: TaskViewModel):
        self.root = root
        self.viewmodel = viewmodel
        self._displayed_tasks: List[Task] = []

        self._configure_window()
        self._setup_ui()

        # Mendaftarkan View sebagai Observer ke ViewModel
        self.viewmodel.add_observer(self.on_tasks_updated)

    def _configure_window(self) -> None:
        self.root.title("Aplikasi Manajemen Tugas (To-Do)")
        width, height = 460, 560
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

    def _setup_ui(self) -> None:
        # 1. Header Banner
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, padx=24, pady=20)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="Daftar Tugas Saya",
            font=("Segoe UI", 16, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="#FFFFFF",
        )
        title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            header_frame,
            text="0 dari 0 tugas selesai",
            font=("Segoe UI", 10),
            bg=self.PRIMARY_COLOR,
            fg="#E0E7FF",
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        # 2. Area Input Tugas (Card)
        input_wrapper = tk.Frame(self.root, bg=self.BG_COLOR, padx=20, pady=16)
        input_wrapper.pack(fill=tk.X)

        input_card = tk.Frame(
            input_wrapper,
            bg=self.CARD_COLOR,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=10,
            pady=6,
        )
        input_card.pack(fill=tk.X)

        self.task_entry = tk.Entry(
            input_card,
            font=("Segoe UI", 11),
            bg=self.CARD_COLOR,
            fg=self.TEXT_MUTED,
            relief=tk.FLAT,
            insertbackground=self.PRIMARY_COLOR,
        )
        self.task_entry.insert(0, self.PLACEHOLDER_TEXT)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 8))

        self.task_entry.bind("<FocusIn>", self._clear_placeholder)
        self.task_entry.bind("<FocusOut>", self._restore_placeholder)
        self.task_entry.bind("<Return>", lambda _: self._handle_add())

        add_btn = tk.Button(
            input_card,
            text="+ Tambah",
            font=("Segoe UI", 10, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="#FFFFFF",
            activebackground=self.PRIMARY_HOVER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._handle_add,
        )
        add_btn.pack(side=tk.RIGHT)
        self._bind_hover(add_btn, self.PRIMARY_COLOR, self.PRIMARY_HOVER)

        # 3. Area Daftar Tugas (Listbox Card)
        list_wrapper = tk.Frame(self.root, bg=self.BG_COLOR, padx=20)
        list_wrapper.pack(fill=tk.BOTH, expand=True)

        list_card = tk.Frame(
            list_wrapper,
            bg=self.CARD_COLOR,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=8,
            pady=8,
        )
        list_card.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_card, relief=tk.FLAT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            list_card,
            font=("Segoe UI", 11),
            bg=self.CARD_COLOR,
            fg=self.TEXT_PRIMARY,
            selectbackground=self.SELECT_BG,
            selectforeground=self.PRIMARY_COLOR,
            activestyle="none",
            relief=tk.FLAT,
            highlightthickness=0,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Pintasan klik ganda & tombol Delete
        self.task_listbox.bind("<Double-Button-1>", lambda _: self._handle_toggle())
        self.task_listbox.bind("<Delete>", lambda _: self._handle_delete())

        hint_label = tk.Label(
            list_wrapper,
            text="Tips: Klik ganda tugas untuk menandai selesai",
            font=("Segoe UI", 8, "italic"),
            bg=self.BG_COLOR,
            fg=self.TEXT_MUTED,
        )
        hint_label.pack(anchor="w", pady=(6, 0))

        # 4. Tombol Aksi Bawah
        btn_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=20, pady=16)
        btn_frame.pack(fill=tk.X)

        toggle_btn = tk.Button(
            btn_frame,
            text="✓ Tandai Selesai / Belum",
            font=("Segoe UI", 10, "bold"),
            bg=self.SUCCESS_COLOR,
            fg="#FFFFFF",
            activebackground=self.SUCCESS_HOVER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self._handle_toggle,
        )
        toggle_btn.pack(side=tk.LEFT)
        self._bind_hover(toggle_btn, self.SUCCESS_COLOR, self.SUCCESS_HOVER)

        delete_btn = tk.Button(
            btn_frame,
            text="Hapus Tugas",
            font=("Segoe UI", 10, "bold"),
            bg=self.DANGER_COLOR,
            fg="#FFFFFF",
            activebackground=self.DANGER_HOVER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self._handle_delete,
        )
        delete_btn.pack(side=tk.RIGHT)
        self._bind_hover(delete_btn, self.DANGER_COLOR, self.DANGER_HOVER)

    # Efek hover tombol
    def _bind_hover(self, button: tk.Button, normal_bg: str, hover_bg: str) -> None:
        button.bind("<Enter>", lambda _: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda _: button.config(bg=normal_bg))

    # Pengaturan teks placeholder pada kotak input
    def _clear_placeholder(self, _) -> None:
        if self.task_entry.get() == self.PLACEHOLDER_TEXT:
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg=self.TEXT_PRIMARY)

    def _restore_placeholder(self, _) -> None:
        if not self.task_entry.get().strip():
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, self.PLACEHOLDER_TEXT)
            self.task_entry.config(fg=self.TEXT_MUTED)

    # Dipanggil otomatis oleh ViewModel saat data berubah (Observer)
    def on_tasks_updated(self, tasks: List[Task]) -> None:
        self._displayed_tasks = tasks
        self.task_listbox.delete(0, tk.END)

        completed_count = 0
        for idx, task in enumerate(tasks):
            if task.is_completed:
                completed_count += 1
                self.task_listbox.insert(tk.END, f"  ✔   {task.title}")
                self.task_listbox.itemconfig(idx, fg=self.TEXT_MUTED)
            else:
                self.task_listbox.insert(tk.END, f"  ○   {task.title}")
                self.task_listbox.itemconfig(idx, fg=self.TEXT_PRIMARY)

        total = len(tasks)
        self.subtitle_label.config(text=f"{completed_count} dari {total} tugas selesai")

    def _handle_add(self) -> None:
        raw_title = self.task_entry.get()
        if raw_title == self.PLACEHOLDER_TEXT or not raw_title.strip():
            messagebox.showwarning("Peringatan", "Nama tugas tidak boleh kosong.")
            return

        self.viewmodel.add_task(raw_title)
        self.task_entry.delete(0, tk.END)
        self.task_entry.config(fg=self.TEXT_PRIMARY)

    def _get_selected_task(self) -> Optional[Task]:
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Pilih salah satu tugas terlebih dahulu.")
            return None
        return self._displayed_tasks[selection[0]]

    def _handle_toggle(self) -> None:
        task = self._get_selected_task()
        if task:
            self.viewmodel.toggle_task(task.id)

    def _handle_delete(self) -> None:
        task = self._get_selected_task()
        if task:
            self.viewmodel.delete_task(task.id)