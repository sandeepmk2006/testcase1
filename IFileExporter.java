import java.time.LocalDate;
import java.util.Map;
public interface IFileExporter {
    void export(String habitName, Map<LocalDate, Boolean> logs);
}