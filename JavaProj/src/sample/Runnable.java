package sample;

public class Runnable implements java.lang.Runnable {
    Controller controller;

    void setController(Controller c) {
        controller = c;
    }

    public void run() {
        controller.refresh_lite();
    }
}
