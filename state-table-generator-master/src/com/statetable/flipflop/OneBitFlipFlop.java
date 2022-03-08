package com.statetable.flipflop;

/**
 * OneBitFlipFlop is an interface implementation for T flip flop and D flip flop.
 * 
 * <p>
 * The <code>OneBitFlipFlop</code> interface is an idealization of this definition in
 * code form. It has 3 methods; namely, <code>setCurrentState</code>: which sets
 * the bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state, 
 * and <code>setBit</code>: which sets the bit of the flipflop to either 0 or 1.
 *
 * @author Joshua Isaac De Castro Pabilona
 * @author Riana Joy Salinas King
 */
public abstract class OneBitFlipFlop {
    
    /**
     * Sets the bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param bit the value to be assigned to the bit of the flip-flop
     */
    public abstract void setBit(int bit);   
   
    /**
     * Sets the current state of this flip-flop to some
     * predefined value. It can only have either of 2 values, binary
     * zero and binary one. <b>{0, 1}></b>
     * @param currentState the current state of this flip-flop
     */
    public abstract void setCurrentState(int currentState);
    
    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its rules. 
     * @return the next state of the bit stored in this flip-flop
     */
    public abstract int getNextState();
}
