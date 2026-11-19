import json
import os
from typing import List
from Model.task import Task

class TaskRepository:
    # Variabel untuk menyimpan satu-satunya objek (Singleton)
    _instance = None

    # Bagian ini memastikan objek TaskRepository hanya dibuat 1 kali saja
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskRepository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._file_path = "tasks_data.json"
        self._tasks: List[Task] = []
        self._next_id = 1
        self._load_from_local()
        self._initialized = True

    # Membaca data tugas dari file lokal saat aplikasi dibuka
    def _load_from_local(self) -> None:
        if os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._tasks = [Task(**item) for item in data]
                if self._tasks:
                    self._next_id = max(t.id for t in self._tasks) + 1

    # Menyimpan data tugas ke file lokal (tasks_data.json)
    def _save_to_local(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump([t.__dict__ for t in self._tasks], file, indent=2)

    def get_all(self) -> List[Task]:
        return list(self._tasks)

    def add(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self._tasks.append(task)
        self._save_to_local()
        return task

    def toggle_status(self, task_id: int) -> None:
        for task in self._tasks:
            if task.id == task_id:
                task.is_completed = not task.is_completed
                self._save_to_local()
                break

    def delete(self, task_id: int) -> None:
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self._save_to_local()