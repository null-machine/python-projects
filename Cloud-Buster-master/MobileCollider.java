/* MobileCollider.java
 * V 1.9
 * Sarita Sou, Jiayi Wu
 * 12/20/2018
 * A mobile hitbox affected by acceleration, velocity and gravity. Used by player and enemies.
 */

import java.awt.Rectangle;
import java.awt.Point;

public class MobileCollider {
	
	Rectangle hitbox; // stores position and size data
	
	// movement
	// can change float to double without problems if necessary
	Point velocity; // changes hitbox position per frame
	int acceleration; // changes velocity per frame
	int moveSpeed; // max velocity
	float moveSmooth; // inverse of frames until moveSpeed is reached, should be a value between 0 and 1
							 // e.g. a moveSmooth of 1/6 takes six frames to go from stationary to max velocity
	
	// jumping
	int jumpSpeed; // initial jump speed, should be negative to go up
	int gravity;
	boolean falling;
	
	public MobileCollider(Rectangle hitbox, float moveSpeed, float moveSmooth, float jumpSpeed, float gravity) {
		super(hitbox);
		this.moveSpeed = moveSpeed;
		this.moveSmooth = moveSmooth;
		this.jumpSpeed = jumpSpeed;
		this.gravity = gravity;
		this.velocity = 0;
		this.acceleration = 0;
	}
	
	// update method would go here, but because java collisions need to check against every single active rectangle in scene, 
	// best to register each collider in a list in main and have main do the checks and updates
	
	public void update() {
		
		// movement
		velocity.translate(acceleration * moveSmooth, 0);
		if(velocity.x > moveSpeed) {
			velocity.x = moveSpeed; // can't use Math.min to avoid if statement because velocity needs to update too
		}
		if(hitbox.intersects(other)) { // java can't check against all other rects, sigh
			hitbox.translate(-Math.min(velocity, moveSpeed), 0);
			velocity.x = 0;
		}
		
		// falling
		if(falling) {
			velocity.y += gravity;
		} else {
			velocity.y = 0;
		}
		
		// jumping and movement direction is handled by child classes, 
		// jump sets velocity.y immediately to jumpSpeed, movement sets acceleration to +- moveSpeed
		
		// apply velocity to position
		hitbox.translate(velocity.x, 0);
	}
	
}
