package sample;

import com.jfoenix.controls.JFXSpinner;
import com.jfoenix.controls.JFXTextField;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.Group;
import javafx.scene.Scene;
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

    @FXML
    public void initialize() {
        tag.setPadding(new Insets(7));
        coin_col.setCellValueFactory(new PropertyValueFactory<>("Coin"));
        buy_col.setCellValueFactory(new PropertyValueFactory<>("Buy"));
        val_col.setCellValueFactory(new PropertyValueFactory<>("Val"));
        spinner.setVisible(false);
        //getData();
    }


    @FXML
    public void enter() throws IOException {
        t_view.getItems().removeAll();
        t_view.getItems().clear();
        t_view.refresh();
        if(group.getChildren().size() > 1)
          group.getChildren().remove(1,group.getChildren().size()-1);

        String command = "python .\\back.py 3 " + tag.getText() + " 0";
        System.out.println("Command: " + command);

        spinner.setVisible(true);
        System.out.print("Calling Process...");
        Process proc = Runtime.getRuntime().exec(command);
        try {
            proc.waitFor();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Done!");
        spinner.setVisible(false);

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

