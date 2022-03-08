import java.util.ArrayList;
import java.util.Random;

public class MazeGenerator {
  private int size = 11;
  private int mapSize; // size of charMap, set by genCharMap
  private char[][] map;
  public char[][] getCharMap() { return map; } // everything builds to this

  private MazeNode[][] nodeGrid;
  private ArrayList<MazeNode> unlinkedNodes;

  private Random rnd = new Random();

  private void genNodeGrid() {

    nodeGrid = new MazeNode[size][size];
    for (int i = 0; i < size; i++) {
      for (int j = 0; j < size; j++) {
        nodeGrid[i][j] = new MazeNode();
      }
    }

    // vert links
    for (int row = 1; row < size; row++) {
      for (int col = 0; col < size; col++) {
        nodeGrid[row][col].north = nodeGrid[row - 1][col];
        nodeGrid[row][col].addLink("N");
        nodeGrid[row - 1][col].south = nodeGrid[row][col];
        nodeGrid[row - 1][col].addLink("S");
      }
    }

    // horz links
    for (int col = 1; col < size; col++) {
      for (int row = 0; row < size; row++) {
        nodeGrid[row][col].west = nodeGrid[row][col - 1];
        nodeGrid[row][col].addLink("W");
        nodeGrid[row][col - 1].east = nodeGrid[row][col];
        nodeGrid[row][col - 1].addLink("E");
      }
    }
  }

  private void genPaths() {
    nodeGrid[0][0].startLinkPath();
    while (!checkVisited()) {
      for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++) {
          if (!nodeGrid[row][col].checkLinksVisited()) {
            nodeGrid[row][col].startLinkPath();
          }
        }
      }
    }
  }

  private boolean checkVisited() {
    for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
        if (!nodeGrid[row][col].visited) {
          return false;
        }
      }
    }
    return true;
  }

  private void buildCharNode(char c) {
    int x = rnd.nextInt(size);
    int y = rnd.nextInt(size);
    while (map[x][y] != ' ') { // dont overwrite
      x = rnd.nextInt(size);
      y = rnd.nextInt(size);
    }
    map[x * 2 + 1][y * 2 + 1] = c;
  }

  private void buildCharWall(char c) {
    int x = rnd.nextInt(mapSize);
    int y = rnd.nextInt(mapSize);
    while (map[x][y] != 'W') { // dont overwrite
      x = rnd.nextInt(mapSize);
      y = rnd.nextInt(mapSize);
    }
    map[x][y] = c;
  }

  private void buildKey() {
    int x = rnd.nextInt(size);
    int y = rnd.nextInt(size);
    while (map[x][y] != ' ') { // dont overwrite
      x = rnd.nextInt(size);
      y = rnd.nextInt(size);
    }
    int mapX = x * 2 + 1;
    int mapY = y * 2 + 1;
    map[mapX][mapY] = 'k';
    map[mapX + 1][mapY + 1] = 't'; // overwrites turrets but nobody cares
    map[mapX + 1][mapY - 1] = 't';
    map[mapX - 1][mapY + 1] = 't';
    map[mapX - 1][mapY - 1] = 't';
  }

  private void genCharMap() {
    mapSize = size * 2 + 1;
    map = new char[mapSize][mapSize];

    // central walls
    for (int row = 1; row < mapSize - 1; row++) {
      for (int col = 1; col < mapSize - 1; col++) {
        map[row][col] = 'W';
      }
    }

    // paths
    for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
        String links = nodeGrid[row][col].openLinks;
        int mapRow = row * 2 + 1;
        int mapCol = col * 2 + 1;
        map[mapRow][mapCol] = ' ';
        if (!links.contains("N")) {
          map[mapRow - 1][mapCol] = ' ';
        }
        if (!links.contains("E")) {
          map[mapRow][mapCol + 1] = ' ';
        }
        if (!links.contains("S")) {
          map[mapRow + 1][mapCol] = ' ';
        }
        if (!links.contains("W")) {
          map[mapRow][mapCol - 1] = ' ';
        }
      }
    }

    // borders (overwrites paths)
    for (int row = 0; row < mapSize; row++) {
      map[row][0] = 'W';
      map[row][mapSize - 1] = 'W';
    }
    for (int col = 0; col < mapSize; col++) {
      map[0][col] = 'W';
      map[mapSize - 1][col] = 'W';
    }

    // for (int i = 0; i < 3; i++) {
    //   buildCharNode('n'); // node
    // }
    // buildCharNode('c'); // charger
    // buildCharNode('l'); // locked
    //
    // for (int i = 0; i < 10; i++) {
    //   buildCharWall('t'); // turret
    // }

    // buildKey(); // key

    // printing
    for (int i = 0; i < mapSize; i++) {
      for (int j = 0; j < mapSize; j++) {
        System.out.print(map[i][j] + " ");
      }
      System.out.println();
    }
  }

  public MazeGenerator() {
    unlinkedNodes = new ArrayList<MazeNode>();
    genNodeGrid();
    // genPaths();
    genCharMap();
  }

  public static void main(String[] args) {
    new MazeGenerator();
  }
}
