/* Sound.java
 * V 1.9
 * Jiayi Wu, Sarita Sou
 * 12/20/2018
 * Plays all sound.
 */

//Imports
import java.io.File;
import javax.sound.sampled.*;

public class Sound {
    public static void playClip(File file) {
        try {
            final Clip clip = (Clip) AudioSystem.getLine(new Line.Info(Clip.class));
            clip.addLineListener(new LineListener() {
                public void update(LineEvent event) {
                    if (event.getType() == LineEvent.Type.STOP) {
                        clip.close();
                    }
                }
            });

            clip.open(AudioSystem.getAudioInputStream(file));
            clip.start();
        } catch (Exception exc) {
            exc.printStackTrace(System.out);
        }

    }

}