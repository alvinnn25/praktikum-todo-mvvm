from typing import Callable, List
from Model.task import Task
from Model.task_repository import TaskRepository

class TaskViewModel:
    def __init__(self):
        self._repository = TaskRepository()
        self._observers: List[Callable[[List[Task]], None]] = []

    def add_observer(self, callback: Callable[[List[Task]], None]) -> None:
        self._observers.append(callback)
        callback(self._repository.get_all())

    def remove_observer(self, callback: Callable[[List[Task]], None]) -> None:
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self) -> None:
        tasks = self._repository.get_all()
        for callback in self._observers:
            callback(tasks)

    def add_task(self, title: str) -> None:
        clean_title = title.strip()
        if clean_title:
            self._repository.add(clean_title)
            self._notify_observers()

    def toggle_task(self, task_id: int) -> None:
        self._repository.toggle_status(task_id)
        self._notify_observers()

    def delete_task(self, task_id: int) -> None:
        self._repository.delete(task_id)
        self._notify_observers()