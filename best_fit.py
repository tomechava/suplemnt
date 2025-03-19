
def best_fit(memory_table, process_table):
    rejected_processes = []
    
    for i in range(len(process_table)): #Cycle between processes
        process = process_table[i]
        process_id = process[0]
        process_size = process[1]
        
        best_pos = -1
        print("Proceso No." + str(i))
        printMemory(memory_table, -1)
        for j in range(len(memory_table)):  #Cicle between memory blocs
            memory_block = memory_table[j]
            block_pos = memory_block[0]
            block_addr = memory_block[1]
            block_size = memory_block[2]
            
            if block_size == process_size:  #If exactly same size
                best_pos = j
                break;
            else:
                if block_size > process_size:   #Process size fits in the blocks size?
                    if best_pos == -1:          #First available position?
                        best_pos = j
                    elif memory_table[j][2] < memory_table[best_pos][2]: #Block size smaller than past size?
                        best_pos = j
        
        if best_pos != -1:  #If best allocation found...
            best_block = memory_table[best_pos]
            best_block_id = best_block[0]
            best_block_addr = best_block[1]
            best_block_size = best_block[2]
            new_addr = best_block_addr + process_size 
            new_size = best_block_size - process_size
            
            memory_table[best_pos] = [best_block_id, new_addr, new_size]
            print("Best position found: " + str(best_pos))
            printMemory(memory_table, best_pos)
            print("--->" + str(best_block_addr) + "," + str(process_size) + "," + str(best_block_id))
            print("\n\n")
            if new_size == 0:
                del memory_table[best_pos]
            
        if best_pos == -1:
            print(f"No space available for process {process_id} (size {process_size})")
            print("\n\n")
            rejected_processes.append((process_id, process_size))
            continue
            
    print("Final Memory:")
    printMemory(memory_table, -1)
    printRejected(rejected_processes)

def printMemory(memory_table, best_pos):
    for i in range(len(memory_table)):
        if best_pos == i:
            print(str(memory_table[i]) + "<---")
        else:
            print(str(memory_table[i]))
            
def printRejected(rejected_processes):
    print("\nResumen de procesos rechazados:")
    for pid, size in rejected_processes:
        print(f"Proceso {pid} - tamaño {size}")
            
        
if __name__ == '__main__':
    memory_table = [[0, 100, 260],
                    [1, 105, 500],
                    [2, 187, 720],
                    [3, 199, 100],
                    [4, 208, 450],
                    [5, 239, 200],
                    [6, 288, 450],
                    ]
    
    process_table = [[0, 500], 
                    [1, 100], 
                    [2, 340], 
                    [3, 900], 
                    [4, 250],
                    ]
    
    best_fit(memory_table, process_table)