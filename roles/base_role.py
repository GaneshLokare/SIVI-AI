# roles/base_role.py
from abc import ABC, abstractmethod
from langchain.schema import SystemMessage

class BaseRole(ABC):
    @abstractmethod
    def get_system_message(self):
        pass



