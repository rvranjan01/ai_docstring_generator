public class MathUtils {

    // add two numbers
    public static int add(int a, int b) {
        return a + b;
    }

    // subtract second number from first
    public static int subtract(int a, int b) {
        return a - b;
    }

    // multiply two numbers
    public static int multiply(int a, int b) {
        return a * b;
    }

    // small demo
    public static void main(String[] args) {
        int x = 10;
        int y = 3;

        System.out.println("Add: " + add(x, y));        
        System.out.println("Subtract: " + subtract(x, y)); 
        System.out.println("Multiply: " + multiply(x, y)); 
    }
}
