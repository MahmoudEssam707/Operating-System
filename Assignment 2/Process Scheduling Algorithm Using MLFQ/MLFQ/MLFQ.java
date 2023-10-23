import java.util.List;
public class MLFQ {
    private List<List<Process>> queues;
    private int[] timeSlices = {8, 15, Integer.MAX_VALUE}; // Time slice for each queue

    public MLFQ(List<List<Process>> queues) {
        this.queues = queues;
    }

    public void schedule(List<Process> processes) {
        int sumWaitingTimes=0;
        int[] waitingTimes = new int[processes.size()];
        int[] arrivalTimes = new int[processes.size()];
        for (int i = 0; i < processes.size(); i++) {
            waitingTimes[i] = 0;
            arrivalTimes[i] = processes.get(i).getArrivalTime();
        }

        int currentQueue = 0;
        int currentTime = 0;

        while (true) {
            if (!queues.get(currentQueue).isEmpty()) {
                Process process = queues.get(currentQueue).get(0);
                System.out.println("Running process: " + process.getName() + " from Queue " + currentQueue +
                        " with burst time: " + process.getBurstTime());

                int timeSlice = timeSlices[currentQueue]; // Dynamic time slice based on queue priority
                if (process.getBurstTime() <= timeSlice) {
                    waitingTimes[processes.indexOf(process)] += currentTime - arrivalTimes[processes.indexOf(process)];
                    currentTime += process.getBurstTime();
                    process.setBurstTime(0);
                } else {
                    process.setBurstTime(process.getBurstTime() - timeSlice);
                    currentTime += timeSlice;
                    // Update arrival time when process is moved to a lower-priority queue
                    arrivalTimes[processes.indexOf(process)] += timeSlice;
                }

                if (process.getBurstTime() > 0) {
                    if (currentQueue + 1 < queues.size()) {
                        queues.get(currentQueue + 1).add(process);
                    } else {
                        queues.get(currentQueue).add(process);
                    }
                } else {
                    System.out.println("Process " + process.getName() + " completed.");
                }

                queues.get(currentQueue).remove(0);
            }

            if (allQueuesEmpty()) {
                break;
            }
            if (queues.get(currentQueue).isEmpty()) {
                currentQueue = (currentQueue + 1) % queues.size();
            }
        }

        for (int i = 0; i < processes.size(); i++) {
            System.out.println("Waiting time for " + processes.get(i).getName() + ": " + waitingTimes[i]);
        }
        for (int i=0;i<processes.size();i++){
            sumWaitingTimes+=waitingTimes[i];
        }
        System.out.println("And the Avg Waiting Time = " + sumWaitingTimes/processes.size());
    }

    private boolean allQueuesEmpty() {
        for (List<Process> queue : queues) {
            if (!queue.isEmpty()) {
                return false;
            }
        }
        return true;
    }
}