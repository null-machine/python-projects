package com.statetable.postfixoperations;
/**
 * Runtime exception thrown when one tries to perform operation top or
 * pop on an empty stack
 * @author Joshua Isaac De Castro Pabilona
 *
 * Adapted from the book 
 * "Data Structures and Algorithms in Java"
 * by Michael Goodrich and Robert Tamassia
 */
public class StackEmptyException extends RuntimeException {
	public StackEmptyException(String err) {
		super(err);
	}
}
