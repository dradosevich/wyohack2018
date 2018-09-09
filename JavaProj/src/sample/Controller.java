package sample;

import com.jfoenix.controls.JFXSpinner;
import com.jfoenix.controls.JFXTextField;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.image.Image;

import javafx.scene.image.ImageView;
import javafx.stage.Stage;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class Controller {
    public JFXTextField tag;
    public JFXSpinner spinner;
    public ComboBox indics;
    private Stage stage;
    private Scene scene;
    private Group group;

    @FXML
    private TableView<TableRow> t_view;

    @FXML
    private TableColumn<TableRow, String> coin_col;

    @FXML
    private TableColumn<TableRow, String> buy_col;

    @FXML
    private TableColumn<TableRow, String> val_col;

    @FXML
    private ImageView image_view;

    //@FXML
    //private ComboBox<String> indics;

    void setStage(Stage s) {
        stage = s;
    }

    void setScene(Scene s) {
        scene = s;
    }

    void setGroup(Group g) {
        group = g;
    }

    private void getData(){
        String[] token_values;
        String current_line;
        File file = new File("Market.csv");

        try{
            Scanner inStream = new Scanner(file, StandardCharsets.UTF_8);
            inStream.useDelimiter("\n");
            if(inStream.hasNextLine())
                inStream.nextLine();
            while(inStream.hasNextLine()){
                current_line = inStream.nextLine();
                System.out.println(current_line);
                token_values = current_line.split(",");
                TableRow Tab = new TableRow();
                Tab.setCoin(token_values[0]);
                Tab.setBuy(token_values[1]);
                Tab.setVal(token_values[2]);
                t_view.getItems().add(Tab);
            }
        } catch(IOException e) {
            e.printStackTrace();
        }

    }

    void initializeCB() {
        //indics = new ComboBox<>();
        //indics.getItems().clear();
        for(int i = 1; i <= 10; i++) {
            indics.getItems().add(Integer.toString(i));
        }
        System.out.println("items: " + indics.getItems().toString());
        indics.getSelectionModel().select(2);
        group.getChildren().add(indics);
        stage.setScene(scene);
        stage.show();
    }


    @FXML
    public void initialize() {
        tag.setPadding(new Insets(7));
//        indics = new ComboBox<>();
//        for(int i = 1; i <= 10; i++) {
//            indics.getItems().add(Integer.toString(i));
//        }
//        System.out.println("items: " + indics.getItems().toString());
//        indics.getSelectionModel().select(3);
//        HBox hbox = new HBox(indics);



        coin_col.setCellValueFactory(new PropertyValueFactory<>("Coin"));
        buy_col.setCellValueFactory(new PropertyValueFactory<>("Buy"));
        val_col.setCellValueFactory(new PropertyValueFactory<>("Val"));
        spinner.setVisible(false);
    }


    @FXML
    public void enter() throws IOException {
        t_view.getItems().removeAll();
        t_view.getItems().clear();
        t_view.refresh();
        System.out.println("#Children: " + group.getChildren().size());
        if(group.getChildren().size() > 2) {
            group.getChildren().remove(1, group.getChildren().size() - 1);
            //group.getChildren().add(indics);
            stage.setScene(scene);
            stage.show();
        }

        String command = "python .\\back.py " + indics.getSelectionModel().getSelectedItem().toString() + " " + tag.getText() + " 0";
        System.out.println("Command: " + command);

        System.out.print("Calling Process...");
        Process proc = Runtime.getRuntime().exec(command);
        spinner.setVisible(true);
        try {
            proc.waitFor();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        spinner.setVisible(false);
        System.out.println("Done!");

        getData();
    }

    @FXML
    public void highlightRow() throws IOException {
        if(t_view.getSelectionModel().getSelectedItem() == null) {return; }

        String name = t_view.getSelectionModel().getSelectedItem().getCoin();
        String current = new java.io.File( "." ).getCanonicalPath();

        System.out.println("Current dir:"+current);
        name = current + "\\Charts\\" + name + ".png";
        System.out.println(name);

        Image img = new Image(new FileInputStream(name));

        image_view = new ImageView(img);
        image_view.setX(377);
        image_view.setY(116);
        image_view.setFitHeight(339);
        image_view.setFitWidth(450);
        image_view.setVisible(true);
        image_view.setCache(true);

        group.getChildren().add(image_view);
        stage.setScene(scene);
        stage.show();
    }
}

