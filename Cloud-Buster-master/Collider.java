/* Collider.java
 * V 1.9
 * Sarita Sou, Jiayi Wu
 * 12/20/2018
 * An immovable hitbox that's checked against for collisions. Used by platforms.
 */

import java.awt.Rectangle;

public class Collider {
	
	Rectangle hitbox;
	
	public Collider(Rectangle hitbox) {
		this.hitbox = hitbox;
	}
}
