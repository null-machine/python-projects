package com.statetable.postfixoperations;
/**
 * Implementation of the Stack interface using a fixed-length array.
 * An exception is thrown if a push operation is attempted when the size
 * of the stack is equal to the length of the array.
 * 
 * @author Joshua Isaac De Castro Pabilona
 * @see StackFullException
 * 
 * Adapted from the book 
 * "Data Structures and Algorithms in Java"
 * by Michael Goodrich and Robert Tamassia
 *
 */
public class ArrayStack implements Stack {
	/**
	 * Default length of the array used to implement the stack.
	 */
	public static final int CAPACITY = 1000;
	
	/**
	 * Length of the array used to implement the stack
	 */
	private int capacity;
	
	/**
	 * Array used to implement the stack.
	 */
	private Object s[];
	
	/**
	 * Index of the top element of the stack in the array.
	 */
	private int top = -1;
	
	/**
	 * Initialize the stack to use an array of default length CAPACITY
	 */
	public ArrayStack(){
		this(CAPACITY);
	}
	
	/**
	 * Initialize the stack to use an array of given length
	 * 
	 * @param capacity length of the array
	 */
	public ArrayStack(int capacity) {
		this.capacity = capacity;
		s = new Object[this.capacity];
	}

	@Override
	public boolean isEmpty() {		
		return (top < 0);
	}	
			
	@Override
	public Object pop() throws StackEmptyException {		
		Object elem;
		if (isEmpty())
			throw new StackEmptyException("Stack is empty.");
		elem = s[top];
		s[top--] = null;  // dereference s[top] for garbage collection
		return elem;
	}

	/**
	 * @exception StackFullException if the array if full
	 */
	@Override
	public void push(Object element) throws StackFullException {
		if (size() == capacity)
			throw new StackFullException("Stack overflow.");
		s[++top] = element;
	}
	
	@Override
	public int size() {		
		return (top + 1);
	}
	
	@Override
	public Object top() throws StackEmptyException {
		if (isEmpty())
			throw new StackEmptyException("Stack is empty.");		
		return s[top];
	}

}