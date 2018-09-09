package sample;

import com.jfoenix.controls.JFXButton;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.image.Image;
import javafx.scene.input.MouseEvent;

import javafx.scene.image.ImageView;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URL;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class Controller {

    private  ObservableList<TableRow> data = FXCollections.observableArrayList();
    public String[] textLines = new String[150];

    //public TableRow[] Tab = new TableRow[150];


    @FXML
    private JFXButton refresh_button;

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

    public void getData(){
        String[] token_values;
        String current_line;
        int i = 0;
        File file = new File("Market.csv");

        try{
            Scanner inStream = new Scanner(file, "UTF-8");
            inStream.useDelimiter("\n");
            if(inStream.hasNextLine())
                current_line = inStream.nextLine();
            while(inStream.hasNextLine()){
                //textLines[i] = current_line;
                current_line = inStream.nextLine();
                System.out.println(current_line);
                token_values = current_line.split(",");
                TableRow Tab = new TableRow();
                Tab.setCoin(token_values[0]);
                Tab.setBuy(token_values[1]);
                Tab.setVal(token_values[2]);
                t_view.getItems().add(Tab);
                i++;
            }
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }


    }

    @FXML
    public void initialize() throws IOException {
    coin_col.setCellValueFactory(new PropertyValueFactory<>("Coin"));
    buy_col.setCellValueFactory(new PropertyValueFactory<>("Buy"));
    val_col.setCellValueFactory(new PropertyValueFactory<>("Val"));
    //Runtime.getRuntime().exec("python back.py");
    getData();
    }


    @FXML
    public void refresh(javafx.scene.input.MouseEvent mouseEvent) throws IOException {
        t_view.getItems().clear();
       Runtime.getRuntime().exec("python .\\back.py 3 DAI 0");
//       System.out.println("Waiting");
//        try {
//            TimeUnit.SECONDS.sleep(45);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
//        System.out.println(("Done Waiting"));
        getData();
    }

    @FXML
    public void highlightRow(MouseEvent mouseEvent) throws IOException {
        String name = t_view.getSelectionModel().getSelectedItem().getCoin();
        String current = new java.io.File( "." ).getCanonicalPath();

        System.out.println("Current dir:"+current);
        name = current + "\\Charts\\" + name + ".png";
        System.out.println(name);

        Image img = new Image("file:" + name, 100, 100, false, false);

        image_view = new ImageView();
        image_view.setImage(img);
        image_view.setVisible(true);

    }
}

