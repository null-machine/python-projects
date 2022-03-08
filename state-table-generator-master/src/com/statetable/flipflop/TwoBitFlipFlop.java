package com.statetable.flipflop;

/**
 * 
 * TwoBitFlipFlop is an interface that holds the JK flip flop and the RS flipflop
 * 
 * <p>
 * The <code>TwoBitFlipFlop</code> interface is an idealization of this definition in
 * code form. It has 4 methods; namely, <code>setCurrentState</code>: which sets
 * the bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state, 
 * <code>setFirstBit</code>: which sets the first bit of the flipflop to either 0 or 1,
 * and <code>setSecondBit</code>: which sets the second bit of the flipflop to either 0 or 1.
 *
 * @author Joshua Isaac De Castro Pabilona
 * @author Riana Joy Salinas King
 */
public abstract class TwoBitFlipFlop implements FlipFlop {
    public abstract void setCurrentState(int currentState);
    public abstract int getNextState();
    public abstract void setFirstBit(int firstBit);
    public abstract void setSecondBit(int secondBit);  
}
