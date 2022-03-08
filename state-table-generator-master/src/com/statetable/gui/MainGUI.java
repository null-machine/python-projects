package com.statetable.gui;

import com.statetable.flipflop.DFlipFlop;
import com.statetable.flipflop.JKFlipFlop;
import com.statetable.flipflop.OneBitFlipFlop;
import com.statetable.flipflop.RSFlipFlop;
import com.statetable.flipflop.TFlipFlop;
import com.statetable.flipflop.TwoBitFlipFlop;
import com.statetable.postfixoperations.BinaryPostfixCalculator;
import com.statetable.postfixoperations.BinaryPostfixConverter;
import com.statetable.postfixoperations.InvalidExpressionException;
import com.statetable.postfixoperations.ParenthesisMismatchException;
import com.statetable.utility.BinaryString;
import com.statetable.utility.IOHelper;
import com.statetable.utility.Variable;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JSpinner;
import javax.swing.JSpinner.DefaultEditor;
import javax.swing.JTextField;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;

/**
 * The main class for the application deployment.
 *
 * @author Joshua Isaac De Castro Pabilona
 */
public class MainGUI extends javax.swing.JFrame {

    private int numFlipFlops = 0;
    private int numInputs = 0;
    private int numOutputs = 0;
    private int numFlipFlopFunctions = 0;
    private boolean twoBitFlipFlop = true; // default is JK, so this must be true at the beginning

    private String currentActiveFlipFlop = "JK Flip-flop"; // default is the JK Flip-flop (cause i want to)
    private List<JTextField> flipFlopFunctionTextFields = null;
    private List<JTextField> outputFunctionTextFields = null;

    public int getSpinnerValue(JSpinner spinner) {
        try {
            spinner.commitEdit();
        } catch (ParseException pe) {
            {
                // Edited value is invalid, spinner.getValue() will return
                // the last valid value, you could revert the spinner to show that:
                JComponent editor = spinner.getEditor();
                if (editor instanceof DefaultEditor) {
                    ((DefaultEditor) editor).getTextField().setValue(spinner.getValue());
                }
                // reset the value to some known value:
                spinner.setValue(0);
                // or treat the last valid value as the current, in which
                // case you don't need to do anything.
            }
        }
        return (Integer) spinner.getValue();
    }

    public void reinitialize(JComponent component) {
        component.removeAll();
        component.revalidate();
        component.repaint();
    }

    public void reinitializeProgram() {
        numFlipFlops = 0;
        numInputs = 0;
        numOutputs = 0;
        twoBitFlipFlop = true;
        currentActiveFlipFlop = "JK Flip-flop";
        flipFlopFunctionTextFields = null;
        outputFunctionTextFields = null;
        spnFlipNum.setValue(0);
        spnInputNum.setValue(0);
        spnOutputNum.setValue(0);
        cbFlipType.setSelectedIndex(0);
    }

    public void doFlipFlopInitialization() {
        flipFlopFunctionTextFields = new ArrayList<>(); // reset all lists everytime this is called
        reinitialize(pnlFlipFunc); // repaint panel
        numFlipFlopFunctions = 0;

        MainGUI.this.numFlipFlops = getSpinnerValue(spnFlipNum);

        if (twoBitFlipFlop) { // if it is a JK or an RS flip-flop; flipFlopFunctions = 2xspinnerValue    
            numFlipFlopFunctions = 2 * MainGUI.this.numFlipFlops;
            String[] coeff = (currentActiveFlipFlop.equals("JK Flip-flop")) ? new String[]{"J", "K"} : new String[]{"R", "S"};
            for (int i = 0, c = 0; i < numFlipFlopFunctions; i++, c++) {
                JLabel label = new JLabel();
                label.setText(coeff[i % 2] + Character.toString((char) ((int) (c / 2) + 65)) + ": ");
                pnlFlipFunc.add(label);
                JTextField textField = new JTextField();
                flipFlopFunctionTextFields.add(textField);
                pnlFlipFunc.add(textField);
            }
        } else { // if it is a D or a T flip-flop
            numFlipFlopFunctions = MainGUI.this.numFlipFlops;
            String coeff = (currentActiveFlipFlop.equals("D Flip-flop")) ? "D" : "T";
            for (int i = 0; i < numFlipFlopFunctions; i++) {
                JLabel label = new JLabel();
                label.setText(coeff + Character.toString((char) ((int) (i) + 65)) + ": ");
                pnlFlipFunc.add(label);
                JTextField textField = new JTextField();
                flipFlopFunctionTextFields.add(textField);
                pnlFlipFunc.add(textField);
            }
        }
    }

    class ItemChangeListener implements ItemListener {

        @Override
        public void itemStateChanged(ItemEvent event) {
            if (event.getStateChange() == ItemEvent.SELECTED) {
                String item = (String) event.getItem(); // works up to here
                currentActiveFlipFlop = item;
                twoBitFlipFlop = currentActiveFlipFlop.equals("JK Flip-flop") || currentActiveFlipFlop.equals("RS Flip-flop");
                doFlipFlopInitialization();
            }
        }
    } // end inner class ItemChangeListener

    class SpinnerListener implements ChangeListener {

        @Override
        public void stateChanged(ChangeEvent event) { // everytime a spinner changes...
            // first, check which spinner changed
            if (event.getSource() == spnFlipNum) { // if <b>spnFlipNum</b> has been changed
                doFlipFlopInitialization(); // NOTE: check the fuction right above these two listeners
            } else if (event.getSource() == spnInputNum) { // if <b>spnInputNum</b> has been canged
                MainGUI.this.numInputs = getSpinnerValue(spnInputNum); // assign new number of inputs 
            } else { // spnOutputNum changed
                outputFunctionTextFields = new ArrayList<>(); // reinitialize
                reinitialize(pnlOutputFunc);
                numOutputs = 0;
//
                numOutputs = getSpinnerValue(spnOutputNum);
                for (int i = 1; i <= numOutputs; i++) {
                    JLabel label = new JLabel();
                    label.setText(String.valueOf(i) + ": ");
                    pnlOutputFunc.add(label);
                    JTextField textField = new JTextField();
                    outputFunctionTextFields.add(textField);
                    pnlOutputFunc.add(textField);
                }
            }
        }
    } // end inner class SpinnerListener 

    /**
     * Creates new form mainGUI
     */
    public MainGUI() {
        initComponents();
        cbFlipType.addItemListener(new ItemChangeListener());
        spnFlipNum.addChangeListener(new SpinnerListener());
        spnInputNum.addChangeListener(new SpinnerListener());
        spnOutputNum.addChangeListener((new SpinnerListener()));
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        pnlConfig = new javax.swing.JPanel();
        lblFlipType = new javax.swing.JLabel();
        cbFlipType = new javax.swing.JComboBox();
        lblFlipNum = new javax.swing.JLabel();
        spnFlipNum = new javax.swing.JSpinner();
        lblInputNum = new javax.swing.JLabel();
        spnInputNum = new javax.swing.JSpinner();
        lblOutputNum = new javax.swing.JLabel();
        spnOutputNum = new javax.swing.JSpinner();
        btnGenerate = new javax.swing.JButton();
        btnReset = new javax.swing.JButton();
        scrlpnTab = new javax.swing.JScrollPane();
        tpFunc = new javax.swing.JTabbedPane();
        pnlFlipFunc = new javax.swing.JPanel();
        pnlOutputFunc = new javax.swing.JPanel();
        pnlTable = new javax.swing.JPanel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("State Table Generator v1.69");
        setResizable(false);

        pnlConfig.setBorder(javax.swing.BorderFactory.createTitledBorder("State Table Configurations"));

        lblFlipType.setText("Flip-flop Type: ");

        cbFlipType.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "JK Flip-flop", "RS Flip-flop", "D Flip-flop", "T Flip-flop" }));
        cbFlipType.setToolTipText("The desired flip-flop to be simulated.");

        lblFlipNum.setText("Number of Flip-flops: ");

        spnFlipNum.setModel(new javax.swing.SpinnerNumberModel(0, 0, 8, 1));
        spnFlipNum.setToolTipText("The number of desired flip-flops. (Positive integer values only)");

        lblInputNum.setText("Number of Inputs: ");

        spnInputNum.setModel(new javax.swing.SpinnerNumberModel(0, 0, 8, 1));
        spnInputNum.setToolTipText("The number of desired inputs. (Positive integer values only)");

        lblOutputNum.setText("Number of Outputs: ");

        spnOutputNum.setModel(new javax.swing.SpinnerNumberModel(0, 0, 8, 1));
        spnOutputNum.setToolTipText("The number of desired outputs. (Positive integer values only)");

        btnGenerate.setText("Generate State Table");
        btnGenerate.setToolTipText("Generates the state table for current configurations.");
        btnGenerate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnGenerateActionPerformed(evt);
            }
        });

        btnReset.setText("Reset ");
        btnReset.setToolTipText("Resets table for new input.");
        btnReset.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnResetActionPerformed(evt);
            }
        });

        scrlpnTab.setHorizontalScrollBarPolicy(javax.swing.ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);

        tpFunc.setToolTipText("");

        pnlFlipFunc.setLayout(new java.awt.GridLayout(0, 2));
        tpFunc.addTab("Flip-flop Functions", pnlFlipFunc);

        pnlOutputFunc.setLayout(new java.awt.GridLayout(0, 2));
        tpFunc.addTab("Output Functions", pnlOutputFunc);

        scrlpnTab.setViewportView(tpFunc);

        javax.swing.GroupLayout pnlConfigLayout = new javax.swing.GroupLayout(pnlConfig);
        pnlConfig.setLayout(pnlConfigLayout);
        pnlConfigLayout.setHorizontalGroup(
            pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(pnlConfigLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(lblFlipNum, javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(lblInputNum, javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(lblOutputNum, javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(lblFlipType, javax.swing.GroupLayout.Alignment.TRAILING))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(cbFlipType, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(spnInputNum, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(spnOutputNum, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(spnFlipNum))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(scrlpnTab, javax.swing.GroupLayout.DEFAULT_SIZE, 577, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(btnReset, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(btnGenerate, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );

        pnlConfigLayout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {btnGenerate, btnReset});

        pnlConfigLayout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {cbFlipType, spnFlipNum, spnInputNum, spnOutputNum});

        pnlConfigLayout.setVerticalGroup(
            pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(pnlConfigLayout.createSequentialGroup()
                .addGap(13, 13, 13)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblFlipType)
                    .addComponent(cbFlipType, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblFlipNum)
                    .addComponent(spnFlipNum, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblInputNum)
                    .addComponent(spnInputNum, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblOutputNum)
                    .addComponent(spnOutputNum, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addGroup(pnlConfigLayout.createSequentialGroup()
                .addGroup(pnlConfigLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, pnlConfigLayout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(btnReset)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(btnGenerate))
                    .addComponent(scrlpnTab))
                .addContainerGap())
        );

        pnlTable.setBorder(javax.swing.BorderFactory.createTitledBorder("State Table"));

        javax.swing.GroupLayout pnlTableLayout = new javax.swing.GroupLayout(pnlTable);
        pnlTable.setLayout(pnlTableLayout);
        pnlTableLayout.setHorizontalGroup(
            pnlTableLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        pnlTableLayout.setVerticalGroup(
            pnlTableLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 395, Short.MAX_VALUE)
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(pnlTable, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(pnlConfig, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(pnlTable, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(pnlConfig, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void btnResetActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnResetActionPerformed
        this.dispose();
        new MainGUI().setVisible(true);
    }//GEN-LAST:event_btnResetActionPerformed

    private void btnGenerateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnGenerateActionPerformed

        if (this.numFlipFlops == 0) {
            JOptionPane.showMessageDialog(this, "At least one flip-flop is required.");
            reinitializeProgram();
            return;
        }

        // STEP 1 : ERROR CHECKING
        // START GENERATING DATA FOR THE STATE TABLE
        List<TwoBitFlipFlop> twoBitFlipFlops = null;
        List<OneBitFlipFlop> oneBitFlipFlops = null;
        if (this.twoBitFlipFlop) { // detected two-bit flip-flop
            twoBitFlipFlops = new ArrayList<>();
            if (this.currentActiveFlipFlop.equals("JK Flip-flop")) { // detected JK Flip-flop
                for (int i = 0; i < this.numFlipFlops; i++) {
                    twoBitFlipFlops.add(new JKFlipFlop()); // populate list with JK flip-flops
                }
            } else { // detected RS Flip-flop
                for (int i = 0; i < this.numFlipFlops; i++) {
                    twoBitFlipFlops.add(new RSFlipFlop()); // populate list with RS flip-flops
                }
            }
        } // end if block 
        else { // detected one bit flip-flop
            oneBitFlipFlops = new ArrayList<>();
            if (this.currentActiveFlipFlop.equals("T Flip-flop")) {  // detected T Flip-flop
                for (int i = 0; i < this.numFlipFlops; i++) {
                    oneBitFlipFlops.add(new TFlipFlop()); // populate list with T flip-flops
                }
            } else { // detected D Flip-flop
                for (int i = 0; i < this.numFlipFlops; i++) { // populate list with D flip-flops
                    oneBitFlipFlops.add(new DFlipFlop());
                }
            }
        } // end else block

        List<String> flipFlopFunctions = new ArrayList<>(); // flipFlopFunctions that wil be stored here 
        // need to be converted into a nice string
        // with single spaces between characters, and it must also be in its RPN form (postfix)
        List<String> outputFunctions = new ArrayList<>(); // same with here
        BinaryPostfixConverter converter = new BinaryPostfixConverter(); // the object used to convert infix expressions to postfi

        try {
            // this can't be null anyway, handled in errors
            for (JTextField textField : this.flipFlopFunctionTextFields) {// important: chronological order, flip-flop flipFlopFunctions come first
                String function = textField.getText();
                System.out.println(function + String.valueOf(function.length()));
                if (function.equals("")) {
                    JOptionPane.showMessageDialog(this, "One or more flip-flop input function text fields are detected to be null.");
                    reinitializeProgram();
                    return;
                }
                function = IOHelper.fixIrregularInput(function); // all of the whitespaces are fixed
                converter.setInfixExpression(function);
                function = converter.getPostfixExpression(); // RPN, + whitespace fixed
                flipFlopFunctions.add(function);
            }
            // output functions, however, are optional
            if (!(this.outputFunctionTextFields == null)) {
                for (JTextField textField : this.outputFunctionTextFields) {
                    String function = textField.getText();
                    if (function.equals("")) { // but you cannot have null textfields
                        JOptionPane.showMessageDialog(this, "One or more output function text fields are detected to be null.");
                        reinitializeProgram();
                        return;
                    }
                    function = IOHelper.fixIrregularInput(function);
                    converter.setInfixExpression(function);
                    function = converter.getPostfixExpression();
                    outputFunctions.add(function);
                }
            }
        } catch (InvalidExpressionException exp) {
            JOptionPane.showMessageDialog(this, "One or more function text fields are detected to have invalid input.");
            reinitializeProgram();
            return;
        } catch (ParenthesisMismatchException exp) {
            JOptionPane.showMessageDialog(this, "Syntax error: parentheses mismatched.");
            reinitializeProgram();
            return;

        }

        Vector<String> columnNames = new Vector<>();

        // STEP 2: MAKE THE HEADERS
        // CURRENT STATE
        for (int i = 0; i < this.numFlipFlops; i++) {
            StringBuilder sb = new StringBuilder();
            String header = Character.toString((char) (i + 65));
            sb.append(header).append("(t)");
            columnNames.add(sb.toString());
        }
        // INPUTS
        for (int i = 0; i < this.numInputs; i++) {
            StringBuilder sb = new StringBuilder();
            String header = "in";
            sb.append(header).append(String.valueOf(i + 1));
            columnNames.add(sb.toString());
        }
        // FLIP FLOP INPUT FUNCTIONS
        String coeff[] = null;
        if (this.twoBitFlipFlop) {
            coeff = (this.currentActiveFlipFlop.equals("JK Flip-flop")) ? new String[]{"J", "K"} : new String[]{"R", "S"};
            for (int i = 0, c = 0; i < this.numFlipFlopFunctions; i++, c++) {
                String header = "" + coeff[i % 2] + Character.toString((char) ((c / 2) + 65));
                columnNames.add(header);
            }
        } else {
            coeff = this.currentActiveFlipFlop.equals("D Flip-flop") ? new String[]{"D"} : new String[]{"T"};
            for (int c = 0; c < this.numFlipFlopFunctions; c++) {
                String header = "" + coeff[0] + Character.toString((char) (c + 65));
                columnNames.add(header);
            }
        }
        // NEXT STATE
        for (int i = 0; i < this.numFlipFlops; i++) {
            StringBuilder sb = new StringBuilder();
            String header = Character.toString((char) (i + 65));
            sb.append(header).append("(t+1)");
            columnNames.add(sb.toString());
        }
        // OUTPUTS
        for (int i = 0; i < this.numOutputs; i++) {
            StringBuilder sb = new StringBuilder();
            String header = "out";
            sb.append(header).append(String.valueOf(i + 1));
            columnNames.add(sb.toString());
        }
        // HEADERS COMPLETE
        // INITIALIZE TABLE
        // if there's a table already
        reinitialize(this.pnlTable); // remove it
        JTable table = new JTable(new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        });
        table.setFillsViewportHeight(true);
        table.getTableHeader().setFont(new Font("SansSerif", Font.BOLD, 12));
        JScrollPane scrollPane = new JScrollPane(table, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        pnlTable.setLayout(new BorderLayout());
        pnlTable.add(scrollPane, BorderLayout.CENTER);
        pnlTable.revalidate();
        pnlTable.repaint();

        int totalExp = this.numFlipFlops + this.numInputs;
        int rows = (int) Math.pow(2, totalExp);

        for (int i = 0; i < rows; i++) {
            Vector<String> rowData = new Vector<>();
            BinaryString binStr = new BinaryString(totalExp, i); // takes a decimal value; converts it to a BINARY STRING
            List<Integer> bits = binStr.getBits(); // then we get the bits of the binary string 
            int variableName = 0; // 0 is A, increment; 1 is B; increment, 2 is C, so on so forth. (in ascii)
            // this is where most of the magic happens dynamically
            List<Variable> variables = new ArrayList<>();
            int flipFlopFunctionCounter = 0;

            for (Integer bit : bits) {
                Variable var = new Variable(bit, variableName);
                variables.add(var);
                variableName++;
//              System.out.print(String.valueOf(bit) + "|");
                rowData.add(String.valueOf(bit));
            }
            // end magic

            // after this all of the bits have been stored to their respective variable
            for (String function : flipFlopFunctions) {
                for (Variable variable : variables) {
                    function = IOHelper.replace(function, variable.getVarName(), Integer.toString(variable.getValue()));
                } // end substitution for loop
                // puro numbers
                BinaryPostfixCalculator calculator = new BinaryPostfixCalculator(function); // per function, calculate the result
//              System.out.print(calculator.getResult());
                rowData.add(String.valueOf(calculator.getResult()));
                if (twoBitFlipFlop) {
                    TwoBitFlipFlop flipFlop = twoBitFlipFlops.get((int) flipFlopFunctionCounter / 2);
                    if (flipFlopFunctionCounter % 2 == 0) { //
                        flipFlop.setFirstBit(calculator.getResult());
                    } else {
                        flipFlop.setSecondBit(calculator.getResult());
                    }
                } else {
                    oneBitFlipFlops.get(flipFlopFunctionCounter).setBit(calculator.getResult());
                }
                flipFlopFunctionCounter++;
            } // end function for loop

            if (!(twoBitFlipFlops == null)) {
                int f = 0;
                for (TwoBitFlipFlop flipFlop : twoBitFlipFlops) {

                    flipFlop.setCurrentState(variables.get(f).getValue());
//                  System.out.print(flipFlop.getNextState()); // NEXT STATE PRINTING
                    if (flipFlop.getNextState() == 69) {
                        rowData.add("Indeterminate");
                    } else {
                        rowData.add(String.valueOf(flipFlop.getNextState()));
                    }
                    f++;
                }
            }
            if (!(oneBitFlipFlops == null)) {
                for (OneBitFlipFlop flipFlop : oneBitFlipFlops) {
                    int f = 0;
                    flipFlop.setCurrentState(variables.get(f).getValue());
//                  System.out.print(flipFlop.getNextState()); // NEXT STATE PRINTING
                    rowData.add(String.valueOf(flipFlop.getNextState()));
                    f++;
                }
            }

            for (String function : outputFunctions) {
                for (Variable variable : variables) {
                    function = IOHelper.replace(function, variable.getVarName(), Integer.toString(variable.getValue()));
                } // end substitution for loop
                BinaryPostfixCalculator calculator = new BinaryPostfixCalculator(function); // per function, calculate the result
//              System.out.print(calculator.getResult()); OUTPUT PRINTING
                rowData.add(String.valueOf(calculator.getResult()));
            }

//            System.out.println();
            DefaultTableModel model = (DefaultTableModel) table.getModel();
            model.addRow(rowData);
        } // end outermost for loop (row counter)
        reinitializeProgram();
    }//GEN-LAST:event_btnGenerateActionPerformed

    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(MainGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(MainGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(MainGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(MainGUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new MainGUI().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnGenerate;
    private javax.swing.JButton btnReset;
    private javax.swing.JComboBox cbFlipType;
    private javax.swing.JLabel lblFlipNum;
    private javax.swing.JLabel lblFlipType;
    private javax.swing.JLabel lblInputNum;
    private javax.swing.JLabel lblOutputNum;
    private javax.swing.JPanel pnlConfig;
    private javax.swing.JPanel pnlFlipFunc;
    private javax.swing.JPanel pnlOutputFunc;
    private javax.swing.JPanel pnlTable;
    private javax.swing.JScrollPane scrlpnTab;
    private javax.swing.JSpinner spnFlipNum;
    private javax.swing.JSpinner spnInputNum;
    private javax.swing.JSpinner spnOutputNum;
    private javax.swing.JTabbedPane tpFunc;
    // End of variables declaration//GEN-END:variables
}
