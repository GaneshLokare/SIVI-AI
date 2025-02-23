# roles/base_role.py
from abc import ABC, abstractmethod

class BaseRole(ABC):
    @abstractmethod
    def get_system_message(self):
        pass



