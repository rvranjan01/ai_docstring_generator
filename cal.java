// Class 1: Addition
class Addition {
    int add(int a, int b) {
        return a + b;
    }
}

// Class 2: Subtraction
class Subtraction {
    int subtract(int a, int b) {
        return a - b;
    }
}

// Class 3: Multiplication
class Multiplication {
    int multiply(int a, int b) {
        return a * b;
    }
}

// Class 4: Main Class
public class CalculatorApp {
    public static void main(String[] args) {
        int x = 10;
        int y = 3;

        // Creating objects
        Addition addObj = new Addition();
        Subtraction subObj = new Subtraction();
        Multiplication mulObj = new Multiplication();

        // Calling methods
        System.out.println("Addition: " + addObj.add(x, y));
        System.out.println("Subtraction: " + subObj.subtract(x, y));
        System.out.println("Multiplication: " + mulObj.multiply(x, y));
    }
}