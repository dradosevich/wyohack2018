package sample;

import com.jfoenix.controls.datamodels.treetable.RecursiveTreeObject;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class User extends RecursiveTreeObject<User> {

    private StringProperty userName;
    private StringProperty age;
    private StringProperty department;

    public User(String department, String age, String userName) {
        this.department = new SimpleStringProperty(department);
        this.userName = new SimpleStringProperty(userName);
        this.age = new SimpleStringProperty(age);
    }



}
