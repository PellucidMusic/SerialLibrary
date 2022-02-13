import serial
import time
import struct

port = "/dev/ttyACM0"

array_a = [3,2,8,21,8,25,33,77,21,37,3,2,218,4,8,155,33,77,24,37,32,2,20,4,25,155,33,77,20,37,3,2,28,4,8,155,33,77,25,37,3,2,8,4,8,155,33,77,24,37,3,2,8,4,8,155,33,77,24]


SerialObj = serial.Serial(port) # COMxx   format on Windows
SerialObj.baudrate = 115200  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1    # Number of Stop bits = 1



def send_serial(data_array):
    
    start_tag = 20
    end_tag = 21
    COBS_start = 255
    COBS_end = 255
    sum_check = (sum(data_array))%256
    print(sum_check)
    
    data_array, COBS_start = COBS(data_array, start_tag)
    data_array, COBS_end = COBS(data_array, end_tag)  
    print(COBS_start)
    print(COBS_end)

    data_array.insert(0,start_tag)
    data_array.insert(1,COBS_start)
    data_array.insert(2,COBS_end)
    data_array.insert(3,sum_check)
    data_array.append(end_tag)
    

    arr_bytes = []
    for a in array_a:
        arr_bytes.append((a).to_bytes(1, byteorder = "little"))
    
    
    for b in arr_bytes:
        SerialObj.write(b)
    


def COBS(in_array, search_t):
    
    preceding_bytes = 3  # Number of bytes before the first payload
    COBS_byte = 255
    i = 0
    j = 0 
    out_array = in_array
    COBS_pos = []
    
    while i < len(out_array):
        if (out_array[i] == search_t):
             COBS_pos.append(i)
        i += 1
    
    print(COBS_pos)

    if (len(COBS_pos) !=  0):
        COBS_byte = COBS_pos[0]+preceding_bytes
    
        
    while j < (len(COBS_pos)):         
        
        if (j == ((len(COBS_pos))-1)):
            out_array[(COBS_pos[j])] = 255
            j+= 1
        else: 
            out_array[(COBS_pos[j])] = COBS_pos[j+1]+preceding_bytes 
            j += 1
        

    return(out_array, COBS_byte)



send_serial(array_a)