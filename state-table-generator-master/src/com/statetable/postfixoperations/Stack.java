package com.statetable.postfixoperations;
/**
 * Interface for a stack: a collection of objects
 * that are inserted and removed according to
 * the last-in first-out principle
 * 
 * @author Joshua Isaac De Castro Pabilona
 * @see StackEmptyException
 * 
 * Adapted from the book 
 * "Data Structures and Algorithms in Java"
 * by Michael Goodrich and Robert Tamassia
 *
 */
public interface Stack {
	
	/** 
	 * @return number of elements in the stack
	 */
	public int size();
	
	/**
	 * @return true if the stack is empty, false otherwise.
	 */
	public boolean isEmpty();
	
	/**
	 * @return top element in the stack
	 * @exception StackEmptyException if the stack is empty.
	 */
	public Object top() throws StackEmptyException;
	
	/**
	 * Insert an element at the top of the stack
	 * @param element element to be inserted
	 * 
	 */
	public void push(Object element);
	
	/**
	 * Remove the top element from the stack
	 * @return element removed
	 * @exception StackEmptyException if the stack is empty
	 * 
	 */
	public Object pop() throws StackEmptyException;
}
