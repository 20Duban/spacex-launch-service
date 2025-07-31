from abc import ABC, abstractmethod
from domain.launch import Launch


class IRepository(ABC):

    @abstractmethod
    def upsert(self, launch: Launch) -> bool:
        pass
    
    @abstractmethod
    def batch_upsert(self, launches: list[Launch]):
        pass
