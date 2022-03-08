package com.statetable.flipflop;

/**
 * RS Flip flop (S=SET R=RESET) by interpreting the R=S=0 is a command that keeps 
 * current state. Specifically, the combination R=1 S=0 is a command to reset the 
 * flip-flop; the combination R=0 S=1 is a command to set the flip-flop. Setting 
 * R=S=1 is a restricted combination or a forbidden state. 
 *
 * <p>
 * The <code>RSFlipFlop</code> is an idealization of this definition in
 * code form. It has 4 methods; namely, <code>setCurrentState</code>: which sets
 * the current bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state,
 * <code>setFirstBit</code>: which sets the R either 1 or 0, and lastly, <code>setSecondBit</code>: 
 * which sets the S either to 0 or 1.
 * 
 * @author Riana Joy Salinas King
 * @author Joshua Isaac De Castro Pabilona
 */
public class RSFlipFlop extends TwoBitFlipFlop {

    private int s = 0;
    private int r = 0;
    private int q = 0;
    private int qpri = 0;

    /**
     * Sets the current state of this flip-flop to some
     * predefined value. It can only have either of 2 values, binary
     * zero and binary one. <b>{0, 1}></b>
     * @param currentState the current state of this flip-flop
     */
    @Override
    public void setCurrentState(int currentBit) {
        this.q = currentBit;
    }

    /**
     * Sets the first bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param firstBit the value to be assigned to R
     */
    @Override
    public void setFirstBit(int firstBit) {
        this.r = firstBit;
    }

    /**
     * Sets the second bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param secondBit the value to be assigned to S
     */
    @Override
    public void setSecondBit(int secondBit) {
        this.s = secondBit;
    }

    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its rules. If <b>R=S=0</b> then no changes would be made to the current state.
     * If <b>R=0 & S=1</b>, this sets the next state. If <b>R=1 & S=0</b>, this resets the next state. 
     * And if <b>R=S=1</b>, this outputs an indeterminate since it is a forbidden state.
     * @return the next state of the bit stored in this flip-flop
     */
    @Override
    public int getNextState() {
        if (r == 0 && s == 0) {
            this.qpri = q; // no change
        } else if (r == 1 && s == 0) {
            this.qpri = 0; // reset state
        } else if (r == 0 && s == 1) {
            this.qpri = 1; // set state
        } else { // 69 means undefined
            this.qpri = 69;
        }
        return this.qpri;
    }
}
