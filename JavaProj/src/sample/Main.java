package sample;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TableView;
import javafx.stage.Stage;

import javax.swing.table.TableColumn;
import javax.swing.text.html.ImageView;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;


public class Main extends Application {


    @Override
    public void start(Stage primaryStage) throws Exception{
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));
        primaryStage.setTitle("Currency Exchange");
        primaryStage.setScene(new Scene(root, 975, 950));
        primaryStage.setMaxHeight(530);
        primaryStage.setMinHeight(530);
        primaryStage.setMaxWidth(870);
        primaryStage.setMinWidth(870);
        primaryStage.show();
    }




    public static void main(String[] args) {
        launch(args);
    }
}
