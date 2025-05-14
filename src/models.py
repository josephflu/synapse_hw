from abc import abstractmethod, ABC


class LoggerInterface(ABC):
    @abstractmethod
    def info(self, msg: str = ""):
        pass

    @abstractmethod
    def warning(self, msg: str):
        pass

    @abstractmethod
    def error(self, msg: str, ex: Exception = None):
        pass