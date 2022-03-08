package com.statetable.postfixoperations;

/**
 * Runtime exception when one tries to input an <b>invalid</b> infix expression
 * for use with class <code>BinaryPostfixConverter</code>.
 * <p>
 * Invalid infix expressions include:
 * a) Numeric tokens in the infix expression
 * b) Syntax Error (missing operators)
 * 
 * @author Joshua Isaac De Castro Pabilona
 */
public class InvalidExpressionException extends RuntimeException {

    public InvalidExpressionException(String err) {
        super(err);
    }
}
