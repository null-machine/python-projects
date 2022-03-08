package com.statetable.flipflop;

/**
 * JK Flip flop augments the behavior of the RS Flip flop (J=SET K=RESET)
 * by interpreting the J=K=1 condition as a flip or toggle command. Specifically,
 * the combination J=1 K=0 is a command to set the flip-flop; the combination 
 * J=0 K=1 is a command to reset the flip-flop. Setting J=K=0 does not result
 * in a D Flip flop but rather will hold the current state. 
 *
 * <p>
 * The <code>JKFlipFlop</code> is an idealization of this definition in
 * code form. It has 4 methods; namely, <code>setCurrentState</code>: which sets
 * the current bit to be stored in the flip-flop, <code>getNextState</code>: which gets
 * the next state according to an implementing flip-flop's "rules" and current state,
 * <code>setFirstBit</code>: which sets the J either 1 or 0, and lastly, <code>setSecondBit</code>: 
 * which sets the K either to 0 or 1.
 * 
 * @author Riana Joy Salinas King
 * @author Joshua Isaac De Castro Pabilona
 */
public class JKFlipFlop extends TwoBitFlipFlop {

    private int j = 0;
    private int k = 0;
    private int q = 0;
    private int qpri = 0;
    
    public JKFlipFlop() {

    }
    
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
     * @param firstBit the value to be assigned to J
     */
    @Override
    public void setFirstBit(int firstBit) {
        this.j = firstBit;
    }

    /**
     * Sets the second bit of this flip-flop to either 0
     * or 1.<b>{0, 1}></b>
     * @param secondBit the value to be assigned to K
     */
    @Override
    public void setSecondBit(int secondBit) {
        this.k = secondBit;
    }

    /**
     * Returns the next state of the bit stored in this flip-flop according
     * to its rules. If <b>J=K=0</b> then no changes would be made to the current state.
     * If <b>J=0 & K=1</b>, this resets the next state. If <b>J=1 & K=0</b>, this sets the next state. 
     * And if <b>J=K=1</b>, the next state toggles or complements the current state.
     * @return the next state of the bit stored in this flip-flop
     */
    @Override
    public int getNextState() {
        if (j == 0 && k == 0) {
            this.qpri = q; // no change
        } else if (j == 0 && k == 1) {
            this.qpri = 0; // reset state
        } else if (j == 1 && k == 0) {
            this.qpri = 1; // set state
        } else { // complement
            if (this.q == 0) {
                this.qpri = 1;
            } else {
                this.qpri = 0;
            }
        }
        return this.qpri;
    }
}
