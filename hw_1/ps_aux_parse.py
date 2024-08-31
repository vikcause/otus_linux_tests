"""
module for parse 'ps uax' command output
"""

import json
import subprocess
import datetime


def parse_ps_aux():
    """method to parse 'ps uax' command"""
    # Run command 'ps aux'
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("Error while running: 'ps aux'.")
        return None

    lines = result.stdout.split('\n')
    lines = lines[1:-1]

    # Analize command
    users = set()
    processes_count = {}
    memory_usage = 0
    cpu_usage = 0
    max_memory_process = {}
    max_cpu_process = {}

    for line in lines:
        if line.startswith('USER'):
            continue
        # Parsing strings 'ps aux'
        fields = line.split()
        if len(fields) < 4:
            continue

        user = fields[0]
        cpu_percent = float(fields[2])
        mem_kb = float(fields[3])
        process_name = fields[10]

        users.add(user)
        processes_count[user] = processes_count.get(user, 0) + 1

#        refresh cpu & mem usage
        memory_usage += mem_kb
        cpu_usage += cpu_percent

        if process_name in max_memory_process:
            max_memory_process[process_name] += mem_kb
        else:
            max_memory_process[process_name] = mem_kb

        if process_name in max_cpu_process:
            max_cpu_process[process_name] += cpu_percent
        else:
            max_cpu_process[process_name] = cpu_percent

#    find max cpu & memory usage processes
    max_memory_process = max(max_memory_process, key=max_memory_process.get)
    max_cpu_process = max(max_cpu_process, key=max_cpu_process.get)

    return {
        'users': sorted(list(users)),
        'total_processes': sum(processes_count.values()),
        'processes_per_user': processes_count,
        'memory_usage': f"{memory_usage:.1f}%",
        'cpu_usage': f"{cpu_usage:.1f}%",
        'max_memory_process': max_memory_process,
        'max_cpu_process': max_cpu_process
    }


# Printing results
results = parse_ps_aux()
if results is not None:
    print("Users:", ', '.join(results['users']))
    print(f"Total amount of processes: {results['total_processes']}")
    print("Amount of processes per user:")
    for user, count in sorted(results['processes_per_user'].items(),
                              key=lambda x: x[1], reverse=True):
        print(f"{count} processes for: {user}")
    print(f"Total Memory usage: {results['memory_usage']}")
    print(f"Total CPU usage : {results['cpu_usage']}")
    print(
        f"Highest usable memory process: {results['max_memory_process'][:20]}")
    print(
        f"Highest usable CPU process: {results['max_cpu_process'][:20]}")
else:
    print("Error while running. There is no results")

# add date & time
current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"{current_date}_scan.txt"

# write results to file
with open(file_name, 'w') as file:
    json_data = json.dumps(results, indent=4)
    file.write(json_data)

print(f"Results saved to: {file_name}")
