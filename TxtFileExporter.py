from datetime import date
from typing import Dict
import csv

class TxtFileExporter:
    def __init__(self, output_file_name: str):
        self.output_file_name = output_file_name

    def get_output_file_name(self) -> str:
        return self.output_file_name

    def set_output_file_name(self, output_file_name: str) -> None:
        self.output_file_name = output_file_name

    def export(self, habit_name: str, logs: Dict[date, bool]) -> None:
        try:
            with open(self.output_file_name, 'w', newline='') as file:
                file.write("===========================================\n")
                file.write("       HABIT TRACKER REPORT\n")
                file.write("===========================================\n")
                file.write(f"Habit: {habit_name}\n")
                file.write(f"Generated: {date.today()}\n")
                file.write("===========================================\n")
                file.write("\n")
                sorted_logs = dict(sorted(logs.items()))
                total_days = len(sorted_logs)
                completed_days = 0
                file.write("Daily Log:\n")
                file.write("-------------------------------------------\n")
                for log_date, status in sorted_logs.items():
                    status_str = "[X] Completed" if status else "[ ] Not Completed"
                    file.write(f"{log_date} - {status_str}\n")
                    if status:
                        completed_days += 1
                file.write("-------------------------------------------\n")
                file.write("\n")
                file.write("Summary:\n")
                file.write(f"Total Days Tracked: {total_days}\n")
                file.write(f"Days Completed: {completed_days}\n")
                file.write(f"Days Missed: {total_days - completed_days}\n")
                if total_days > 0:
                    percentage = (completed_days * 100.0) / total_days
                    file.write(f"Completion Rate: {percentage:.1f}%\n")
                file.write("===========================================\n")
                print(f"Report exported successfully to {self.output_file_name}")
        except Exception as e:
            print(f"Error exporting report: {str(e)}")