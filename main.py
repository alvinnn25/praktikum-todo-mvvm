import tkinter as tk
from ViewModel.task_viewmodel import TaskViewModel
from View.task_view import TaskView

if __name__ == "__main__":
    root = tk.Tk()
    viewmodel = TaskViewModel()
    app = TaskView(root, viewmodel)
    root.mainloop()