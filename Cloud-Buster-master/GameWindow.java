/* GameWindow.java
 * V 1.9
 * Jiayi Wu, Sarita Sou
 * 12/20/2018
 * Displays all game elements during play.
 */

//Graphics &GUI imports
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.awt.image.*;
import javax.imageio.*;

//Keyboard imports
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

//This class represents the game window
class GameWindow extends JFrame {
Map map;
Player player;
//Clock clock;
static GamePanel gamePanel;
private int screenH,screenW;
private boolean paused, resumeSelected;

//Constructor
public GameWindow() {
super("Cloud Buster");
screenH = 768;
screenW = 1024;
this.setSize(screenW,screenH);
setResizable(false);// set my window to allow the user to resize it
this.setLocationRelativeTo(null);
this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);// set the window up to end the program when closed

//Set up the game panel (where we put our graphics)
gamePanel = new GamePanel();
this.add(new GamePanel());

// KeyListener
MyKeyListener keyListener = new MyKeyListener();
this.addKeyListener(keyListener);

this.requestFocusInWindow(); //make sure the frame has focus
this.setVisible(true);

paused = false;
resumeSelected = true;

//Start the game loop in a separate thread
Thread t = new Thread(new Runnable() { public void run() { animate(); }}); //start the gameLoop
t.start();
}

//The main Game Loop
public void animate() {
while(true){
try{ Thread.sleep(20);} catch (Exception exc){}//delay
player.checkCollision();
player.update();
map.update(player.getDx(),player.getDx(),player.getMapLeft(),player.getMapRight(),player.getMapUp(),player.getMapDown());
this.repaint();
}
}

//An inner class representing the panel on which the game takes place
private class GamePanel extends JPanel {
Font font;
BufferedImage pauseBackground;

//constructor
public GamePanel() {
setPreferredSize(new Dimension(1024,768));
map = new Map(screenW,screenH);
player = new Player(map.getTileMap());
//clock = new Clock();
try {
pauseBackground = ImageIO.read(new File("pause.png"));
font = Font.createFont(Font.TRUETYPE_FONT, new File("8bitoperator_jve.ttf")).deriveFont(64f);
} catch (Exception e) {
System.out.println("error loading files");
}

setFont(font);
}

public void paintComponent(Graphics g) {
super.paintComponent(g); //required to ensure the panel si correctly redrawn
map.draw(g);
player.draw(g,player.getDirection());
if (paused) {
g.drawImage(pauseBackground,0,0,1024,768,null);
if (resumeSelected) {
g.setColor(Color.WHITE);
g.drawString("RESUME",420,290);
g.setColor(Color.GRAY);
g.drawString("QUIT",450,450);
} else {
g.setColor(Color.GRAY);
g.drawString("RESUME",420,290);
g.setColor(Color.WHITE);
g.drawString("QUIT",450,450);
}
}
}

}//End of the GamePanel class

private class MyKeyListener implements KeyListener {

public void keyTyped(KeyEvent e) {
}


public void keyPressed(KeyEvent e) {
//System.out.println("keyPressed="+KeyEvent.getKeyText(e.getKeyCode()));
if (!paused) {
if (e.getKeyCode() == 37 && player.getKeyRight() == false) {//If ArrowLeft is pressed
player.setMovingLeft(true);
player.setKeyLeft(true);
player.setDirection("left");
}else if (e.getKeyCode() == 39 && player.getKeyLeft() == false){//If ArrowRight is pressed
player.setMovingRight(true);
player.setKeyRight(true);
player.setDirection("right");
}else if (e.getKeyCode() == 38){ //If ArrowUp is pressed
player.setDirection("up");
map.pos.translate(0,-100);
}else if (e.getKeyCode() == 40){ //If ArrowDown is pressed
player.setDirection("down");
map.pos.translate(0,100);
}else if (e.getKeyCode() == 32){ //If space is pressed
if (player.getCanJump()) {
player.setJump(true);
}
}else if (e.getKeyCode() == 67){ //If "c" is pressed
player.setAttack(true);
}else if (e.getKeyCode() == 88){ //If "x" is pressed
player.setSpecialAttack(true);
player.setDirection("down");
}else if (e.getKeyCode() == 90){ //If "z" is pressed
System.out.println("Z");
}else if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {//If ESC is pressed
paused = true;
}
} else {
if (e.getKeyCode() == 67){ //If "c" is pressed
if (resumeSelected) {
paused = false;
} else {
System.exit(0);
}
} else if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {//If ESC is pressed
paused = false;
}else if (e.getKeyCode() == 38){ //If ArrowUp is pressed
resumeSelected = true;
}else if (e.getKeyCode() == 40){ //If ArrowDown is pressed
resumeSelected = false;
}
}
}

public void keyReleased(KeyEvent e) {
if (e.getKeyCode() == 37) {//If ArrowLeft is released
player.setMovingLeft(false);
player.setKeyLeft(false);
}else if (e.getKeyCode() == 39){//If ArrowRight is released
player.setMovingRight(false);
player.setKeyRight(false);
}else if (e.getKeyCode() == 40){//If ArrowDown is released

}
}
} //end of keyboard listener


}//End of the GameWindow class
