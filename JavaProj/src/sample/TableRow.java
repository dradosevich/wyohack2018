package sample;

public class TableRow {
    private String coin;
    private String buy;
    private String val;

    public void TableRow(){
        this.coin = null;
        this.buy = null;
        this.val = null;
    }

    public void TableRow(String s, String y, String z){
        this.coin = s;
        this.buy = y;
        this.val = z;
    }

    public String getCoin(){
        return coin;
    }
    public String getBuy(){
        return buy;
    }
    public String getVal(){
        return val;
    }


    public void setCoin(String s){
        coin = s;
    }
    public void setBuy(String s){
        buy = s;
    }
    public void setVal(String s){
        val = s;
    }

}
