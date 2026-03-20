public class User extends TrackerEvent {
    private String username;
    private String email;
    public User(int id, String name, String username, String email) {
        super(id, name);
        this.username = username;
        this.email = email;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    @Override
    public String getDetails() {
        return "User: " + getName() + " (@" + username + ")";
    }
    @Override
    public String toString() {
        return getName() + " (@" + username + ")";
    }
}