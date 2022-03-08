package com.statetable.postfixoperations;

/**
 * Runtime exception thrown when one tries to input an expression with
 * mismatched parentheses.
 *
 * @author Joshua Isaac De Castro Pabilona
 */
public class ParenthesisMismatchException extends RuntimeException {

    public ParenthesisMismatchException(String err) {
        super(err);
    }
}
