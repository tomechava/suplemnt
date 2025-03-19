
def first_fit(memory_table, process_table, index):
    
    for i in range(len(process_table)):
        process = process_table[i]
        process_id = process[0]
        process_size = process[1]
        
        for j in range(len(memory_table)):
            memory_block = memory_table[j]
            block_pos = memory_block[0]
            block_addr = memory_block[1]
            block_size = memory_block[2]
            
            
            if block_size >= process_size:
                new_addr = block_addr 
                new_size = block_size - process_size
                memory_table[j] = [block_pos, new_addr, new_size]
                printMemory(memory_table)
                print("--->" + str(block_addr) + "," + str(process_size) + "," + str(block_pos))
                print("\n\n\n")
                
            if j == len(memory_table):
                print("No space allocation availabe for the process:" + str(process_id) + str(process_size))
                break;

def printMemory(memory_table):
    for i in range(len(memory_table)):
        print(memory_table[i])
            
        
        
        
if __name__ == '__main__':
    memory_table = [[0, 100, 260],
                    [1, 105, 500],
                    [2, 187, 720],
                    [3, 199, 100],
                    [4, 208, 450],
                    [5, 239, 200],
                    [6, 288, 450],
                    ]
    process_size = 500
    index = 2
    #first_fit(memory_table, process_size, index)
    printMemory(memory_table)