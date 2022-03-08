package com.statetable.flipflop;
/**
 * A flip-flop stores a single bit (binary digit) of data; one of its two states
 * represents a binary one and the other represents a binary zero. Such data
 * storage can be used for storage of <b>state</b>, and such a circuit is
 * described as sequential logic. When used in a finite-state machine, the
 * output and next state depend not only on its current input, but also on its
 * current state (and hence, previous inputs).
 *
 * <p>
 * The <code>FlipFlop</code> interface is an idealization of this definition in
 * code form. It has 2 methods; namely, <code>setCurrentState</code>: which sets
 * the bit to be stored in the flip-flop, and <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state.
 *
 * @author Joshua Isaac De Castro Pabilona
 * @author Riana Joy Salinas King
 */
public interface FlipFlop {

    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its "rules" and current state.
     * @return the next state of the bit stored in this flip-flop
     */
    public abstract int getNextState();

    /**
     * Sets the current state of this flip-flop to some
     * predefined value. It can only have either of 2 values, binary
     * zero and binary one. <b>{0, 1}></b>
     * @param currentState the current state of this flip-flop
     */
    public abstract void setCurrentState(int currentState);
}
