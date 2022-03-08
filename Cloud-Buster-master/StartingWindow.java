/* StartingWindow.java
 * V 1.9
 * Jiayi Wu, Sarita Sou
 * 12/20/2018
 * Runs the starting menu.
 */

//Imports
import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.ImageIcon;
import javax.swing.BorderFactory;
import javax.swing.border.EmptyBorder;
import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Dimension;

class StartingWindow extends JFrame {

JFrame thisFrame;

//Constructor - this runs first
StartingWindow() {
super("Cloud Buster");
this.thisFrame = this;

//configure the window
this.setSize(1024,768);
this.setLocationRelativeTo(null); //start the frame in the center of the screen
this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
this.setResizable (false);
JPanel decPanel = new DecoratedPanel();
decPanel.setBorder(new EmptyBorder(620, 82, 68, 68));
JPanel mainPanel = new JPanel();
mainPanel.setLayout(new BorderLayout());
mainPanel.setBackground(new Color(0, 0, 0, 0));

//Create a JButton for the centerPanel
ImageIcon sb =new ImageIcon("start.png");
JButton startButton = new JButton(sb);
startButton.setBackground(new Color(0, 0, 0, 0));
startButton.setRolloverIcon(new ImageIcon("startPressed.png"));
startButton.setBorder(BorderFactory.createEmptyBorder());
startButton.setFocusPainted(false);
startButton.addActionListener(new StartButtonListener());
JPanel bottomPanel = new JPanel();
bottomPanel.setBackground(new Color(0, 0, 0, 0));
bottomPanel.add(startButton);

//Add all panels to the mainPanel according to border layout
mainPanel.add(bottomPanel,BorderLayout.SOUTH);
decPanel.add(mainPanel);

//add the main panel to the frame
this.add(decPanel);

//Start the app
this.setVisible(true);
}

//INNER CLASS - Overide Paint Component for JPANEL
private class DecoratedPanel extends JPanel {

DecoratedPanel() {
this.setBackground(new Color(0,0,0,0));
}

public void paintComponent(Graphics g) {
super.paintComponent(g);
Image pic = new ImageIcon("clouds.png").getImage();
g.drawImage(pic,0,0,1024,768,null);
 }
}

//This is an inner class that is used to detect a button press
class StartButtonListener implements ActionListener {//this is the required class definition
public void actionPerformed(ActionEvent event){
System.out.println("Starting new Game");
thisFrame.dispose();
new GameWindow();
}
}

}
