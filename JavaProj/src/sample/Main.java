package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {


    @Override
    public void start(Stage primaryStage) throws Exception{
        FXMLLoader loader = new FXMLLoader(getClass().getResource("sample.fxml"));
        Parent root = loader.load();
        Group group = new Group(root);
        Scene scene = new Scene(group, 870, 515);

        primaryStage.setTitle("Currency Exchange");
        primaryStage.setScene(scene);
        primaryStage.setMaxHeight(1530);
        primaryStage.setMinHeight(530);
        primaryStage.setMaxWidth(170);
        primaryStage.setMinWidth(870);
        primaryStage.show();

        Controller controller = loader.getController();
        controller.setStage(primaryStage);
        controller.setGroup(group);
        controller.setScene(scene);
        controller.initializeCB();
    }




    public static void main(String[] args) {
        launch(args);
    }

}
