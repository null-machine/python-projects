package com.statetable.utility;
/**
 * Runtime exception thrown when one tries to run 
 * the program with null inputs.
 * @author Joshua Isaac De Castro Pabilona
 */
public class InputNullException extends RuntimeException {
    public InputNullException(String err) {
        super(err);  
    }  
}
