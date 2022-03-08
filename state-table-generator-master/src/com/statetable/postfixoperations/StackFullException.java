package com.statetable.postfixoperations;
/**
 * Runtime exception when one tries to push on a stack that
 * is already full.
 * 
 * @author Joshua Isaac De Castro Pabilona
 *
 */
public class StackFullException extends RuntimeException {
	public StackFullException(String err){
		super(err);
	}
}
