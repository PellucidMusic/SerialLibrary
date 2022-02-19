import serial
import time


port = "/dev/ttyACM0"

array_a = [21,21,21]

SerialObj = serial.Serial(port) # COMxx   format on Windows
SerialObj.baudrate = 115200  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1    # Number of Stop bits = 1


def map_range(value, min_a, max_a , min_b = 0 , max_b = 255):    
    span_a = max_a - min_a
    span_b = max_b - min_b
    valueScaled = min_b + ((float(value-min_a)/ float(span_a)) *span_b)
    ret_value = int(valueScaled)
    return(ret_value)




def send_serial(data_array):
    
    start_tag = 20
    end_tag = 21
    COBS_start = 255
    COBS_end = 255
    sum_check = (sum(data_array))%256
    print(sum_check)  
   
    data_array, COBS_start = COBS(data_array, start_tag, start_tag, end_tag)
    data_array, COBS_end = COBS(data_array, end_tag, start_tag, end_tag)  
    
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
    


def COBS(in_array, search_t,start_tag,end_tag):
    
    preceding_bytes = 3  # Number of bytes before the first payload
    COBS_byte = 255
    i = 0
    j = 0 
    k = 0
    out_array = in_array
    COBS_pos = []
    
    while i < len(out_array):
        if (out_array[i] == search_t):
             COBS_pos.append(i)
        i += 1
    
    print(COBS_pos)

    if (len(COBS_pos) !=  0):
        COBS_byte = COBS_pos[0]+preceding_bytes
        if (COBS_byte == start_tag):
            COBS_byte = 0 
        if (COBS_byte == end_tag):
            COBS_byte = 1 
        
    while j < (len(COBS_pos)):                
        if (j == ((len(COBS_pos))-1)):
            out_array[(COBS_pos[j])] = 255
            j+= 1
        else: 
            out_array[(COBS_pos[j])] = COBS_pos[j+1]+preceding_bytes 
            if (out_array[(COBS_pos[j])] == start_tag):
                out_array[(COBS_pos[j])] = 0 
            if (out_array[(COBS_pos[j])] == end_tag):
                out_array[(COBS_pos[j])] = 1 
            
            j += 1

    
    return(out_array, COBS_byte)



send_serial(array_a)