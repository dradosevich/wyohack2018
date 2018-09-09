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

import static javafx.geometry.Pos.CENTER;

public class Controller {
    public JFXTextField tag;
    public JFXSpinner spinner;
    public ComboBox<String> indics;
    public JFXTextField bos;
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

    void refresh() {
        System.out.println("#Children: " + group.getChildren().size());
        group.getChildren().remove(image_view);
        group.getChildren().remove(bos);
        tag.setText("");
        indics.getSelectionModel().select(2);
        t_view.getItems().clear();
        System.out.println("#Children: " + group.getChildren().size());
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
        indics.getItems().add("I-1");
        indics.getItems().add("I-2");
        indics.getItems().add("Both");
        System.out.println("items: " + indics.getItems().toString());
        indics.getSelectionModel().select(2);
        group.getChildren().add(indics);
        stage.setScene(scene);
        stage.show();
    }


    @FXML
    public void initialize() {
        tag.setPadding(new Insets(7));
        coin_col.setCellValueFactory(new PropertyValueFactory<>("Coin"));
        buy_col.setCellValueFactory(new PropertyValueFactory<>("Buy"));
        val_col.setCellValueFactory(new PropertyValueFactory<>("Val"));
        spinner.setVisible(false);
    }


    @FXML
    public void enter() throws IOException {
        if(tag.getText().equals("")){
            return;
        }
        t_view.getItems().removeAll();
        t_view.getItems().clear();
        t_view.refresh();

        System.out.println("#Children: " + group.getChildren().size());
        group.getChildren().remove(bos);
        group.getChildren().remove(image_view);
        System.out.println("#Children: " + group.getChildren().size());

        stage.setScene(scene);
        stage.show();

        String drop = indics.getSelectionModel().getSelectedItem();
        String i;
        switch (drop) {
            case "I-1":
                i = "1";
                break;
            case "I-2":
                i = "2";
                break;
            default:
                i = "3";
                break;
        }

        String command = "python .\\back.py " + i + " " + tag.getText() + " 0";
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

        String bs = t_view.getSelectionModel().getSelectedItem().getBuy();
        group.getChildren().remove(bos);
        bos.setAlignment(CENTER);
        bos.setEditable(false);
        if(bs.equalsIgnoreCase("buy")) {
            bos.setText("BUY");
            bos.setStyle("-fx-background-color: #22a522;" + "-fx-font-size: 18px;" + "-fx-font-weight: bold;" + "-fx-text-fill: white;");
        } else {
            bos.setText("SELL");
            bos.setStyle("-fx-background-color: #db1515;" + "-fx-font-size: 18px;" + "-fx-font-weight: bold;" + "-fx-text-fill: white;");
        }

        String name = t_view.getSelectionModel().getSelectedItem().getCoin();
        String current = new java.io.File( "." ).getCanonicalPath();

        System.out.println("Current dir:"+current);
        name = current + "\\Charts\\" + name + ".png";
        System.out.println(name);

        Image img = new Image(new FileInputStream(name));

        group.getChildren().remove(image_view);
        image_view = new ImageView(img);
        image_view.setX(377);
        image_view.setY(116);
        image_view.setFitHeight(339);
        image_view.setFitWidth(450);
        image_view.setVisible(true);
        image_view.setCache(true);

        group.getChildren().add(bos);
        group.getChildren().add(image_view);
        stage.setScene(scene);
        stage.show();
    }
}

