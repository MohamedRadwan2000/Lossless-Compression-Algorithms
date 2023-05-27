package newpackage;

public class Node implements Comparable<Node> {

    private int key;
    private String val;
    public Node left, right;

    public Node() {

    }

    public Node(int key, String value) {
        this.key = key;
        this.val = value;
    }

    public Node(Node left, Node right) {
        this.key = left.key + right.key;
        this.left = left;
        this.right = right;
    }

    public boolean isLeaf() {
        return left == null && right == null;
    }

    public String getValue() {
        return val;
    }

    public void setVal(String value) {
        this.val = value;
    }

    @Override
    public int compareTo(Node o) {
        return Integer.compare(this.key, o.key);
    }
}
