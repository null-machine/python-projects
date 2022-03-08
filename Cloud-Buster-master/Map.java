/* Map.java
 * V 1.9
 * Jiayi Wu, Sarita Sou
 * 12/20/2018
 * The environment and background.
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.Scanner;
import java.awt.image.*;
import javax.imageio.*;

class Map {
	private int tileWidth, tileHeight;
	private int[][] map;
	private Tile[][] worldMap;
	private int visibleH, visibleW;
	Point pos; //make getter later
	private BufferedImage[] tileImages, backgrounds;

	public Map(int xResolution,int yResolution) {
		BufferedImage sheet;

		tileWidth=85; //The size of each square
		tileHeight=85;//it would be best to choose a res that has a common divisor
		tileImages = new BufferedImage[3];
		backgrounds = new BufferedImage[1];
		pos = new Point(-1100,-1300);
	
		try{
			createIntMap();
			tileImages[0] = ImageIO.read(new File("tile0.png"));
			sheet = ImageIO.read(new File("lever.png"));
			for (int i=0; i<2; i++) {
				tileImages[i+1] = sheet.getSubimage(i * 15,0,15,25);
			}
			backgrounds[0] = ImageIO.read(new File("stone.png"));
		} catch (Exception e){
			System.out.println("error loading map");
		}

		createWorldMap();
	}

	public Tile[][] getTileMap(){
		return worldMap;
	}

	// reads a text file and turns into int array to show tile position
	public void createIntMap() throws Exception {
		Scanner input = new Scanner(new File("map.txt"));
		String content = "";
		int cols;
		int rows;

		while (input.hasNext()) {
			content += input.nextLine();
		}
		input.close();

		cols = Integer.parseInt(content.substring(0,content.indexOf(" ")));
		content = content.substring(content.indexOf(" ")+1);

		rows = Integer.parseInt(content.substring(0,content.indexOf(" ")));
		content = content.substring(content.indexOf(" ")+1);

		map = new int[cols][rows];

		for (int i=0;i<map.length;i++) {
			for (int j=0;j<map[0].length;j++) {
				map[i][j] = (int)content.charAt(0)-48;
				content = content.substring(1);
			}
		}
	}

	//Creates a 2D array of tiles from the int array
	public void createWorldMap() {
		worldMap = new Tile[map.length][map[1].length];
		for (int j=0;j<worldMap.length;j++){
			for (int i=0;i<worldMap[1].length;i++) {
				if (map[j][i] == 1){
					worldMap[j][i]=new Platform(Color.RED,i*tileWidth, j*tileHeight,85,85, tileImages[0]);
				} else if (map[j][i] == 4) {
					worldMap[j][i]=new DeathBlock(Color.RED,i*tileWidth, j*tileHeight,85,85, tileImages[1]);
				} else if (map[j][i] == 8) {
					worldMap[j][i]=new Lever(Color.RED,i*tileWidth, j*tileHeight,85,85, tileImages[1]);
				}
			}
		}
	}

	public void update(int dx, int dy,boolean left, boolean right, boolean up, boolean down){
		if (left && (pos.getX()<-5)){
			this.pos.translate(dx,0);
		}else if (right && (pos.getX()>-1130)){
			this.pos.translate(-(dx),0);
		}
		if (up && (pos.getY()<-5)){
			this.pos.translate(dy,0);
		}else if (down && (pos.getY()>-1130)){
			this.pos.translate(-(dy),0);
		}
	}

	//draws the 2D array of tiles
	public void draw(Graphics g) {
		g.drawImage(backgrounds[0],(int)pos.getX()%2048+35,((int)pos.getY())%1536,2048,1536,null);
		g.drawImage(backgrounds[0],(int)pos.getX()%2048+35,((int)pos.getY())%1536-1536,2048,1536,null);
		g.drawImage(backgrounds[0],(int)pos.getX()%2048+35,((int)pos.getY())%1536+1536,2048,1536,null);

		for (int j=0;j<map.length;j++){
			for (int i=0;i<map[1].length;i++){
				if (map[j][i]==1) {
					//System.out.println((int)pos.getX()+i+" "+((int)pos.getY())+j);
					worldMap[j][i].setPos(((int)pos.getX())+i,((int)pos.getY())+j);
					worldMap[j][i].draw(g,i,j);
				} else if (map[j][i]==8) {
					worldMap[j][i].setPos(((int)pos.getX())+i,((int)pos.getY())+j);
					worldMap[j][i].draw(g,i,j);
				}
			}
		}
	}
}
