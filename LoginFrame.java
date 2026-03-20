import javax.swing.*;
import java.awt.*;
public class LoginFrame extends JFrame {
    private static final long serialVersionUID = 1L;
    private final DatabaseManager dbManager;
    private JTextField usernameField;
    private JPasswordField passwordField;
    private JTextField nameField;
    private JTextField emailField;
    private User loggedInUser;
    public LoginFrame() {
        dbManager = new DatabaseManager();
        loggedInUser = null;
        setTitle("Habit Tracker - Login");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(10, 10));
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.addTab("Login", createLoginPanel());
        tabbedPane.addTab("Register", createRegisterPanel());
        add(tabbedPane, BorderLayout.CENTER);
        setVisible(true);
    }
    private JPanel createLoginPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        JLabel titleLabel = new JLabel("Login to Habit Tracker");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(titleLabel, gbc);
        gbc.gridwidth = 1;
        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.WEST;
        panel.add(new JLabel("Username:"), gbc);
        usernameField = new JTextField(20);
        gbc.gridx = 1;
        panel.add(usernameField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 2;
        panel.add(new JLabel("Password:"), gbc);
        passwordField = new JPasswordField(20);
        gbc.gridx = 1;
        panel.add(passwordField, gbc);
        JButton loginButton = new JButton("Login");
        loginButton.addActionListener(e -> handleLogin());
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(loginButton, gbc);
        passwordField.addActionListener(e -> handleLogin());
        return panel;
    }
    private JPanel createRegisterPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        JLabel titleLabel = new JLabel("Create New Account");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(titleLabel, gbc);
        gbc.gridwidth = 1;
        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.WEST;
        panel.add(new JLabel("Full Name:"), gbc);
        nameField = new JTextField(20);
        gbc.gridx = 1;
        panel.add(nameField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 2;
        panel.add(new JLabel("Email:"), gbc);
        emailField = new JTextField(20);
        gbc.gridx = 1;
        panel.add(emailField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 3;
        panel.add(new JLabel("Username:"), gbc);
        JTextField regUsernameField = new JTextField(20);
        gbc.gridx = 1;
        panel.add(regUsernameField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 4;
        panel.add(new JLabel("Password:"), gbc);
        JPasswordField regPasswordField = new JPasswordField(20);
        gbc.gridx = 1;
        panel.add(regPasswordField, gbc);
        JButton registerButton = new JButton("Create Account");
        registerButton.addActionListener(e -> handleRegister(
            nameField.getText(),
            emailField.getText(),
            regUsernameField.getText(),
            new String(regPasswordField.getPassword())
        ));
        gbc.gridx = 0;
        gbc.gridy = 5;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(registerButton, gbc);
        return panel;
    }
    private void handleLogin() {
        String username = usernameField.getText().trim();
        String password = new String(passwordField.getPassword());
        if (username.isEmpty() || password.isEmpty()) {
            JOptionPane.showMessageDialog(this, 
                "Please enter both username and password!", 
                "Login Error", 
                JOptionPane.ERROR_MESSAGE);
            return;
        }
        loggedInUser = dbManager.loginUser(username, password);
        if (loggedInUser != null) {
            JOptionPane.showMessageDialog(this, 
                "Welcome back, " + loggedInUser.getName() + "!", 
                "Login Successful", 
                JOptionPane.INFORMATION_MESSAGE);
            openMainApplication();
        } else {
            JOptionPane.showMessageDialog(this, 
                "Invalid username or password!", 
                "Login Failed", 
                JOptionPane.ERROR_MESSAGE);
            passwordField.setText("");
        }
    }
    private void handleRegister(String name, String email, String username, String password) {
        if (name.isEmpty() || email.isEmpty() || username.isEmpty() || password.isEmpty()) {
            JOptionPane.showMessageDialog(this, 
                "Please fill in all fields!", 
                "Registration Error", 
                JOptionPane.ERROR_MESSAGE);
            return;
        }
        if (password.length() < 6) {
            JOptionPane.showMessageDialog(this, 
                "Password must be at least 6 characters long!", 
                "Registration Error", 
                JOptionPane.ERROR_MESSAGE);
            return;
        }
        int userId = dbManager.registerUser(name, username, email, password);
        if (userId > 0) {
            JOptionPane.showMessageDialog(this, 
                "Account created successfully! Please login.", 
                "Registration Successful", 
                JOptionPane.INFORMATION_MESSAGE);
            nameField.setText("");
            emailField.setText("");
        } else {
            JOptionPane.showMessageDialog(this, 
                "Registration failed! Username may already exist.", 
                "Registration Error", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    private void openMainApplication() {
        SwingUtilities.invokeLater(() -> {
            new HabitTrackerApp(loggedInUser, dbManager);
            dispose();
        });
    }
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        SwingUtilities.invokeLater(() -> {
            new LoginFrame();
        });
    }
}