package com.statetable.postfixoperations;

import java.util.StringTokenizer;

/**
 *
 * @author Joshua Isaac
 */
public class BinaryPostfixCalculator {

    private String boolPostfix;

    public BinaryPostfixCalculator() {
        this.boolPostfix = null;
    }

    public BinaryPostfixCalculator(String boolPostfix) {
        this.boolPostfix = boolPostfix;
    }

    public void setPostfixExpression(String boolPostfix) {
        this.boolPostfix = boolPostfix;
    }

    public int getResult() {
        StringTokenizer tokens = new StringTokenizer(this.boolPostfix);
        Stack postfixValues = new ArrayStack();

        while (tokens.hasMoreTokens()) {
            String token = tokens.nextToken();
            if (isBoolOperator(token)) {
                if (token.equals("'")) { //NOT
                    boolean operand = (Boolean) postfixValues.pop();
                    postfixValues.push(!operand);
                } else {
                    boolean secondOperand = (Boolean) postfixValues.pop();
                    boolean firstOperand = (Boolean) postfixValues.pop();
                    boolean result = false;
                    if (token.equals("*")) { //XOR
                        result = firstOperand ^ secondOperand;
                    } else if (token.equals(".")) { //AND
                        result = firstOperand && secondOperand;
                    } else if (token.equals("+")) { //OR
                        result = firstOperand || secondOperand;
                    }
                    postfixValues.push(result);
                }
            } // end if
            else {
                postfixValues.push(intToBool(token));
            } // end else
        } // end while
        return boolToInt((Boolean)postfixValues.pop());
    }

    private boolean isBoolOperator(String token) {
        return (token.equals("'"))
                || (token.equals("*"))
                || (token.equals("."))
                || (token.equals("+"));
    }

    private boolean intToBool(String token) {
        if (isInteger(token)) {
            int intVal = Integer.parseInt(token);
            return intVal == 1;
        }
        return false;
    }

    private int boolToInt(boolean bool) {
        if (bool == true) {
            return 1;
        } else {
            return 0;
        }
    }

    private boolean isInteger(String token) {
        try {
            int test;
            test = Integer.parseInt(token);
        } catch (NumberFormatException e) {
            return false;
        }
        return true;
    }

} // end BooleanPostfixCalculator
