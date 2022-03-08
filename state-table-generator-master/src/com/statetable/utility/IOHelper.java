package com.statetable.utility;

/**
 * Class <code>IOHelper</code> is a utility class which 
 * has 2 methods for IO operations such as input correcting
 * and character replacement; namely, <code>fixIrregularInput</code>
 * and <code>replace</code>.
 * @author Joshua Isaac De Castro Pabilona
 */
public class IOHelper {

    /**
     * Manipulates the string such that the final string returned should 
     * have a singular whitespace character in between characters, with no
     * trailing whitespace.
     * @param string the string to be manipulated
     * @return the string after manipulation
     */
    public static String fixIrregularInput(String string) {
        StringBuilder sb = new StringBuilder();
        string = string.trim();
        String[] splitString = string.split("\\s+");
        int i = 0;
        for (String substring : splitString) {
            if (i == 0) {
                sb.append(substring);
            } else {
                sb.append(" ").append(substring);
            }
            i++;
        }
        string = sb.toString();
        sb.setLength(0); // resets the StringBuilder for subsequent use

        //After this point, there is only 1 whitespace between characters and no trailing whitespaces
        
        String[] splitStringWF = string.split(" "); // split by the lone whitespace character
        for (String substring : splitStringWF) {
            if (substring.length() == 1) {
                sb.append(substring).append(" ");
            } else {
                String[] splitSubstringWF = substring.split("");
                for (String subSubstring : splitSubstringWF) {
                    sb.append(subSubstring).append(" ");
                }
            }
        } // end for loop

        string = sb.toString();
        string = string.trim();

        return string;
    }
    /**
     * Replaces a character in a string with another character.
     * @param string the string to be manipulated
     * @param c_before The character to be replaced
     * @param c_after the character replacing c_before
     * @return a string with all occurrences of c_before replaced by c_after
     */
    public static String replace(String string, String c_before, String c_after) {
        return string.replace(c_before.charAt(0), c_after.charAt(0));  
    }
} // end class IOHelper
