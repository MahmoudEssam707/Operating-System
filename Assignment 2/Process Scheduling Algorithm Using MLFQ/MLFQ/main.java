import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        List<List<Process>> queues = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            queues.add(new ArrayList<>());
        }

        MLFQ mlfq = new MLFQ(queues);

        try (Scanner scanner = new Scanner(System.in)) {
            System.out.println("Enter the number of processes:");
            int numProcesses = scanner.nextInt();

            List<Process> processes = new ArrayList<>();
            for (int i = 0; i < numProcesses; i++) {
                System.out.println("Enter burst time for process " + (i + 1) + ":");
                int burstTime = scanner.nextInt();
                processes.add(new Process("P" + (i + 1), i, burstTime));
            }

            // Add all processes to the highest priority queue at the start
            queues.get(0).addAll(processes);

            mlfq.schedule(processes);
        }
    }
}