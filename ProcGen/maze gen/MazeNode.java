import java.util.ArrayList;
import java.util.Random;

public class MazeNode {

  public MazeNode north, east, south, west;
  public String openLinks = "";
  public boolean visited;

  private Random rnd = new Random();

  public void addLink(String link) {
    openLinks += link;
  }

  public void remLink(String link) {
    openLinks = openLinks.replace(link, "");
  }

  public boolean checkLinksVisited() {
    if (!visited) {
      return false;
    }
    if (north != null && !north.visited) {
      return false;
    }
    if (east != null && !east.visited) {
      return false;
    }
    if (south != null && !south.visited) {
      return false;
    }
    if (west != null && !west.visited) {
      return false;
    }
    return true;
  }

  public void startLinkPath() {
    visited = false;
    linkPath();
  }

  public void linkPath() {

    if (visited) {
      return;
    } else {
      visited = true;
    }

    int choiceIndex = rnd.nextInt(openLinks.length());
    String choice = "" + openLinks.charAt(choiceIndex);
    remLink(choice);

    switch (choice) {
      case "N":
      north.remLink("S");
      north.linkPath();
      break;
      case "E":
      east.remLink("W");
      east.linkPath();
      break;
      case "S":
      south.remLink("N");
      south.linkPath();
      break;
      case "W":
      west.remLink("E");
      west.linkPath();
      break;
    }
  }
}
