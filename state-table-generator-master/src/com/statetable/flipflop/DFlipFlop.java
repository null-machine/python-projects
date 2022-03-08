package com.statetable.flipflop;

/**
 * The D Flip-flop is also known as a "data" or "delay" flip-flop. It
 * captures the value of the D-input at a definite portion of the clock 
 * cycle (such as the rising edge of the clock). That captured value becomes
 * the Q output. At other times, the output Q does not change. 
 * 
 * The D Flip flop can be viewed as a memory cell, a zero-order hold, or a
 * delay line. 
 * 
 * <p>
 * The <code> DFlipFlop</code> is an idealization of this definition in
 * code form. It has 3 methods; namely, <code>setCurrentState</code>: which sets
 * the bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state,
 * and <code>setBit</code>: which sets the current bit.
 * 
 * @author Joshua Isaac De Castro Pabilona
 * @author Riana Joy Salinas King
 */
public class DFlipFlop extends OneBitFlipFlop {
    
    private int d = 0;
    private int q = 0;
    private int qpri = 0;

    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its rules. If <b>D=0</b> this resets the next state.
     * And if <b>D=1</b>, the sets the next state.
     * @return the next state of the bit stored in this flip-flop
     */
    @Override
    public int getNextState() {
        if(d == 0) {
            this.qpri = 0;
        } 
        else {
            this.qpri = 1;
        }
        return this.qpri;
    }

    /**
     * Sets the bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param bit the value to be assigned to D
     */
    @Override
    public void setBit(int bit) {
        this.d = bit;
    }

    /**
     * Sets the current state of this flip-flop to some
     * predefined value. It can only have either of 2 values, binary
     * zero and binary one. <b>{0, 1}></b>
     * @param currentState the current state of this flip-flop
     */
    @Override
    public void setCurrentState(int currentState) {
        this.q = currentState;
    }
} // end DFlipFlop class
