chart = []

class process:
    def __init__(self, pid, AT, BT):
        self.pid = pid
        self.arrival = AT
        self.bur = BT
        self.burst = BT
        self.waittime = 0  # Initialize wait time to 0
        self.turnaroundtime = 0  # Initialize turnaround time to 0

def shiftCL(alist):
    temp = alist[0]
    for i in range(len(alist) - 1):
        alist[i] = alist[i + 1]
    alist[len(alist) - 1] = temp
    return alist

def RR(tq, plist, n):
    global chart
    queue = []
    time = 0
    ap = 0
    rp = 0
    done = 0
    q = tq
    start = 0
    while done < n:
        for i in range(ap, n):
            if time >= plist[i].arrival:
                queue.append(plist[i])
                ap += 1
                rp += 1
        if rp < 1:
            chart.append(0)
            time += 1
            continue
        if start:
            shiftCL(queue)
        if queue[0].burst > 0:
            if queue[0].burst > q:
                for g in range(time, time + q):
                    chart.append(queue[0].pid)
                time += q
                queue[0].burst -= q
            else:
                for g in range(time, time + queue[0].burst):
                    chart.append(queue[0].pid)
                time += queue[0].burst
                queue[0].burst = 0
                done += 1
                rp -= 1
                # Calculate turnaround time and waiting time for the completed process
                queue[0].turnaroundtime = time - queue[0].arrival
                queue[0].waittime = queue[0].turnaroundtime - queue[0].bur

            start = 1

plist = []
plist.append(process(0,0,5))
plist.append(process(1,1,8))
plist.append(process(2,3,6))
plist.append(process(3,5,4))
plist.append(process(4,8,8))
plist.append(process(5,16,10))

RR(3,plist,len(plist))
# Print turnaround time and waiting time for each process
for p in plist:
    print(f"Process {p.pid}: Turnaround Time = {p.turnaroundtime}, Waiting Time = {p.waittime}")

# Print the execution order of processes
print("Execution Order:")
print(chart)

