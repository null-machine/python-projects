/* Player.java
 * V 1.9
 * Jiayi Wu, Sarita Sou
 * 12/20/2018
 * Manages player animations and input.
 */

import java.awt.image.BufferedImage;



class Player extends MobileCollider {
/*
private Point pos;
private int height, width, health;
private int attackWidth, attackHeight, gravity, jumpHeight, maxJumpHeight, dy, dx;
private int jumpCounter;

private boolean jump, canJump, attack, falling, specialAttack, keyLeft, keyRight;
private boolean collisionLeft,collisionRight,collisionTop,collisionBottom;
private boolean mapLeft,mapRight,mapUp,mapDown;
private boolean movingRight, movingLeft;
private Rectangle boundingBoxPlayer,boundingBoxBottom, boundingBoxAttack; //rectangles that are used for collision detection

private Tile[][] map;
*/

	// animations
	private BufferedImage[] sprites;
	private int currentSprite, currentStep, spriteIndex;
	private BufferedImage[] sprites;
	
	// player specific movement
	private String direction;
	

	public Player() {
		super(new Rectangle(500,))
pos = new Point(500,480);
width=50;
height=90;
maxJumpHeight = 300;
dy = 5;
dx = 5;
//maxDy = 768-height;

boundingBoxPlayer = new Rectangle((int)pos.getX(), (int)pos.getY(), width, height);
boundingBoxBottom = new Rectangle((int)pos.getX(), (int)pos.getY()+height-10, width, 10);

movingRight = false;
movingLeft = false;

mapRight = false;
mapLeft = false;
mapUp = false;
mapDown = false;

keyLeft = false;
keyRight = false;

jump = false;
canJump = false;
attack = false;
specialAttack = false;
falling = false;

collisionLeft = false;
collisionRight = false;
collisionTop = false;
collisionBottom = false;

direction = "right";

loadSprites();
spriteIndex=0;
currentStep=0;
}

public void animate() {

if (currentStep>3) {
currentStep = 0;
if (attack){
if (currentSprite==0) {
Sound.playClip(new File("Swoosh.wav"));
}

if (direction.equals("down")){
if ((spriteIndex>20)&&(spriteIndex<25)) {
spriteIndex++;
currentSprite++;
} else if (spriteIndex == 25) {
attack = false;
} else {
spriteIndex=21;
currentSprite = 0;
}
} else if (direction.equals("up")){
if ((spriteIndex>16)&&(spriteIndex<21)) {
spriteIndex++;
currentSprite++;
} else if (spriteIndex == 21) {
attack = false;
} else {
spriteIndex=17;
currentSprite = 0;
}
} else {
if ((spriteIndex>13)&&(spriteIndex<17)) {
spriteIndex++;
currentSprite++;
} else if (spriteIndex == 17) {
attack = false;
} else {
spriteIndex=14;
currentSprite = 0;
}
}
} else if (specialAttack) {
if ((spriteIndex>24)&&(spriteIndex<31)) {
spriteIndex++;
currentSprite++;
} else if (spriteIndex == 31) {
specialAttack = false;
} else {
spriteIndex=25;
currentSprite = 0;
}
} else if (((movingLeft)&&(pos.getX() > 5)) || ((movingRight)&&(pos.getX() < 1019))){
if ((spriteIndex>7)&&(spriteIndex<13)) {
spriteIndex++;
} else {
spriteIndex = 8;
}
} else {
spriteIndex = 32;
}
}
currentStep++;
}

public void update(){

animate();

if (movingLeft && pos.getX() > dx && (!collisionRight)){
//System.out.println("movingLeft");
mapLeft = true;
pos.translate(-dx,0);
}else if (movingRight && pos.getX() < 1024-dx && (!collisionLeft)){
//System.out.println("movingRight");
mapRight = true;
pos.translate(dx,0);
}

}

public void loadSprites() {
BufferedImage sheet;

try{
sheet = ImageIO.read(new File("aster.png"));
int cols = 36;
sprites = new BufferedImage[cols];

for (int i = 0; i < cols; i++) {
sprites[i] = sheet.getSubimage(i * 90,0,90,100);
}
}catch(Exception e) { System.out.println("error loading sheet");};
}

public void draw(Graphics g,String direction) {
int drawRatio = 3;

//g.setColor(Color.GRAY); //There are many graphics commands that Java can use

//g.fillRect((int)pos.getX(), (int)pos.getY(), width, height); //notice the y is a variable that we control from our animate method

if (direction.equals("left")) {
g.drawImage(sprites[spriteIndex],(int)(pos.getX()+150),(int)(pos.getY()-100),-270,300,null);
} else {
g.drawImage(sprites[spriteIndex],(int)(pos.getX()-100),(int)(pos.getY()-100),270,300,null);
}
}

}
