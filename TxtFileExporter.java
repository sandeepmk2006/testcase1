import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDate;
import java.util.Map;
import java.util.TreeMap;
public class TxtFileExporter implements IFileExporter {
    private String outputFileName;
    public TxtFileExporter(String outputFileName) {
        this.outputFileName = outputFileName;
    }
    public String getOutputFileName() {
        return outputFileName;
    }
    public void setOutputFileName(String outputFileName) {
        this.outputFileName = outputFileName;
    }
    @Override
    public void export(String habitName, Map<LocalDate, Boolean> logs) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(outputFileName))) {
            writer.println("===========================================");
            writer.println("       HABIT TRACKER REPORT");
            writer.println("===========================================");
            writer.println("Habit: " + habitName);
            writer.println("Generated: " + LocalDate.now());
            writer.println("===========================================");
            writer.println();
            TreeMap<LocalDate, Boolean> sortedLogs = new TreeMap<>(logs);
            int totalDays = sortedLogs.size();
            int completedDays = 0;
            writer.println("Daily Log:");
            writer.println("-------------------------------------------");
            for (Map.Entry<LocalDate, Boolean> entry : sortedLogs.entrySet()) {
                String status = entry.getValue() ? "[X] Completed" : "[ ] Not Completed";
                writer.println(entry.getKey() + " - " + status);
                if (entry.getValue()) {
                    completedDays++;
                }
            }
            writer.println("-------------------------------------------");
            writer.println();
            writer.println("Summary:");
            writer.println("Total Days Tracked: " + totalDays);
            writer.println("Days Completed: " + completedDays);
            writer.println("Days Missed: " + (totalDays - completedDays));
            if (totalDays > 0) {
                double percentage = (completedDays * 100.0) / totalDays;
                writer.println("Completion Rate: " + String.format("%.1f", percentage) + "%");
            }
            writer.println("===========================================");
            System.out.println("Report exported successfully to " + outputFileName);
        } catch (IOException e) {
            System.err.println("Error exporting report: " + e.getMessage());
        }
    }
}