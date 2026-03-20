from datetime import date
from typing import Dict

class IFileExporter:
    def export(self, habit_name: str, logs: Dict[date, bool]) -> None:
        ...