import java.util.ArrayList;
import java.util.Scanner;

public class LRU_FreeBSD_Algorithm {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        // Get the capacity of Main Memory from the user
        System.out.print("Enter the capacity of Main Memory: ");
        int capacity = scanner.nextInt();
        // Get the number of process references from the user
        System.out.print("Enter the number of process references: ");
        int numberOfReferences = scanner.nextInt();
        // List to store user-provided page references
        int[] processList = new int[numberOfReferences];
        // Get the process references from the user
        System.out.println("Enter the process references:");
        for (int i = 0; i < numberOfReferences; i++) {
            processList[i] = scanner.nextInt();
        }
        // List of current pages in Main Memory
        ArrayList<Integer> s = new ArrayList<>();
        int pageFaults = 0;
        for (int i : processList) {
            // If i is not present in currentPages list
            if (!s.contains(i)) {
                // Check if the list can hold equal pages
                if (s.size() == capacity) {
                    s.remove(0);
                    s.add(i);
                    // Increment Page faults
                    pageFaults++;
                } else {
                    s.add(i);
                }

                // Display the pattern after each page fault
                System.out.println("Current Number to Enter Memory: " + i + "\nResult: " + s);
            }
        }
        System.out.println("\nTotal Page Faults: " + pageFaults);
        // Close the scanner to prevent resource leaks
        scanner.close();
    }
}
