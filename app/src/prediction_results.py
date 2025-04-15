from models import TaskResult    
class ResultsStore:
    """
    Used a singleton for this as well as there has to be dictionary.
    Without this, if I did results_dict = {}, then it would make a new empty dictionary
    every time this file was imported.
    """
    _instance = None
    _results_dict: dict[str, TaskResult]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResultsStore, cls).__new__(cls)
            cls._instance._results_dict = {}
        return cls._instance

    def get_results_dict(self) -> dict[str, TaskResult]:
        return self._results_dict

results_dict = ResultsStore().get_results_dict()