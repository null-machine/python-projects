package com.statetable.flipflop;

/**
 * The T Flip-flop changes state ("toggles") whenever the clock input is
 * strobed. If the T input is low, the flip-flop holds the previous value.
 * 
 * <p>
 * The <code>TFlipFlop</code> is an idealization of this definition in
 * code form. It has 3 methods; namely, <code>setCurrentState</code>: which sets
 * the bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state,
 * and <code>setBit</code>: which sets the current bit.
 * 
 * @author Joshua Isaac De Castro Pabilona
 * @author Riana Joy Salinas King
 */
public class TFlipFlop extends OneBitFlipFlop {

    private int t = 0;
    private int q = 0;
    private int qpri = 0;

    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its rules. If <b>T=0</b> this holds the current state.
     * And if <b>D=1</b>, this complements the current state.
     * @return the next state of the bit stored in this flip-flop
     */
    @Override
    public int getNextState() {
        if (t == 0) { // no change
            this.qpri = q;
        } else { // complement
            if (this.q == 0) {
                this.qpri = 1;
            } else {
                this.qpri = 0;
            }
        }
        return this.qpri;
    }

    /**
     * Sets the bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param bit the value to be assigned to T
     */
    @Override
    public void setBit(int bit) {
        this.t = bit;
    }

    /**
     * Sets the current state of this flip-flop to some
     * predefined value. It can only have either of 2 values, binary
     * zero and binary one. <b>{0, 1}></b>
     * @param currentState the current state of this flip-flop
     */
    @Override
    public void setCurrentState(int bit) {
        this.q = bit;
    }
} // end class TFlipFlop
