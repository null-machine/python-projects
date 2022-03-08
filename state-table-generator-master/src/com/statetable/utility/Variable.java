package com.statetable.utility;

/**
 * @author Joshua Isaac De Castro Pabilona
 */
public class Variable {
    private int value = 0;
    private String varName = null;
     
    public Variable(int value, int index) {
        this.value = value;
        this.varName = Character.toString(((char)(index+65)));   
    }
   
    public String getVarName() {
        return this.varName;
    }
    
    public int getValue() {
        return this.value;
    }
    
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.varName).append(" = ").append(Integer.toString(this.value));
        return sb.toString();
    }
}
