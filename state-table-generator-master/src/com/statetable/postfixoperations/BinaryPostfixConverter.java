package com.statetable.postfixoperations;

import java.util.StringTokenizer;

/**
 * 
 * @author Joshua Isaac De Castro Pabilona
 */
public final class BinaryPostfixConverter {

    private String infixExpression = null;
    private String postfixExpression = null;

    public BinaryPostfixConverter() {

    }

    /**
     * Constructor for the InfixToPostfix class.
     *
     * @param infixExpression
     */
    public BinaryPostfixConverter(String infixExpression) {
        this.infixExpression = infixExpression;
        this.convertToPostfix();
    }

    public void setInfixExpression(String infixExpression) {
        this.infixExpression = infixExpression;
        this.convertToPostfix();
    }

    public String getPostfixExpression() {
        return this.postfixExpression;
    }
    
    private boolean isAlpha(String token) {
        return Character.isLetter(token.charAt(0));
    }

    public boolean isNumeric(String s) {
        return s.matches("[-+]?\\d*\\.?\\d+");
    }

    private void convertToPostfix() {
        StringTokenizer tokens = new StringTokenizer(this.infixExpression);
        StringBuilder sb = new StringBuilder();
        Stack operators = new ArrayStack();

        while (tokens.hasMoreTokens()) {
            String token = tokens.nextToken();
            if (isAlpha(token)) {
                sb.append(token).append(" ");
            } // end if
            else if (isNumeric(token)) {
                throw new InvalidExpressionException("Error, invalid infix expression!");
            } else if (token.equals("(")) { //if the read token is a left parenthesis
                operators.push(token);
            } // end else if
            else if (token.equals(")")) { //if the read token is a right parenthesis
                while (!(((String) operators.top()).equals("("))) {
                    sb.append((String) operators.pop()).append(" ");
                }
                operators.pop(); //when it exits at the while, it will point at "(", and we discard it
            }//end else if
            else // if the read token is an operator..
            {
                while (!(operators.isEmpty()) && (checkPrecedence(token) < checkPrecedence((String) operators.top()))) {
                    sb.append((String) operators.pop()).append(" ");
                }
                operators.push(token);
            }//end else
        }//end while

        while (!operators.isEmpty()) {
            if (((String) operators.top()).equals("(") || ((String) operators.top()).equals(")")) {
                throw new ParenthesisMismatchException("Error, misplaced parenthesis in expression!");
            }
            sb.append((String) operators.pop()).append(" ");
        }
        this.postfixExpression = sb.toString().trim();
    }

    private int checkPrecedence(String token) {
        if (token.equals("'")) {
            return 4;
        } else if (token.equals("*")) {
            return 3;
        } else if (token.equals(".")) {
            return 2;
        } else { // if token is an OR (+)
            return 1;
        }
    }
} // end while
