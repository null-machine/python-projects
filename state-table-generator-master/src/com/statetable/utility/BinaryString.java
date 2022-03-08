package com.statetable.utility;

import java.util.ArrayList;
import java.util.List;

/**
 * Class <code>BinaryString</code> is a class specifically designed for ease of working with
 * Binary Strings. It allows for no-tears bit caching, and automatic generation of a binary string given a
 * decimal, positive integer value. 
 * @author Joshua Isaac De Castro Pabilona
 */
public class BinaryString {
  
   private int bitlength;
   private List<Integer> bits;
   
   private BinaryString() {
       // force the client to use the parameterized constructor
   }
   /**
    * Initializes a <code>BinaryString</code> object with value <i>decimalVal</i>
    * and bit length <i>bitLength</i>
    * @param bitLength the length of the desired binary string (total exponent)
    * @param decimalVal the decimal value of a certain string
    */
   public BinaryString(int bitLength, int decimalVal) {
       this.bitlength = bitLength;
       bits = new ArrayList<>(this.bitlength);
       String binaryString = Integer.toBinaryString(decimalVal);
       if(bitLength != binaryString.length()) {
            binaryString = String.format(("%" + bitLength + "s"), binaryString).replace(' ', '0');
       }
       binaryString = binaryString.trim();
       String[] splitBinaryString = binaryString.split("(?!^)"); // the regex is called a NEGATIVE LOOKAHEAD
       for(String substr : splitBinaryString) {
           this.bits.add(Integer.parseInt(substr));
       }   
   } 
   /**
    * Gets the bits of this <code>BinaryString</code> object.
    * @return the bits of a binary string
    */
   public List<Integer> getBits() {
       return this.bits;
   }
   
   /**
    * Returns a string representation of this binary string.
    * @return a string representation of the binary string
    */
   @Override
   public String toString() {
       StringBuilder sb = new StringBuilder();
       for(Integer integer : bits) {
           sb.append(integer);
       }
       return sb.toString();   
   }
} // end class BinaryString
