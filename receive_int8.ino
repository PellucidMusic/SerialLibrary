// Example 6 - Receiving binary data

const byte numBytes = 64;
byte receivedBytes[numBytes];
byte numReceived = 0;
int received_data[64];
int decoded_data[64];
int COBS_start = 255;
int COBS_end = 255;

boolean newData = false;

void setup() {
    Serial1.begin(9600);
    Serial.begin(115200);
    Serial1.println("<Arduino is ready>");
    received_data[0] = 255;
    received_data[1] = 255;
}

void loop() {
    recvBytesWithStartEndMarkers();
    showNewData();
}

void recvBytesWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    byte startMarker = 0x14;
    byte endMarker = 0x15;
    byte rb;
   

    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();

        if (recvInProgress == true) {
            if (rb != endMarker) {
                receivedBytes[ndx] = rb;
                ndx++;
                if (ndx >= numBytes) {
                    ndx = numBytes - 1;
                }
            }
            else {
                receivedBytes[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                numReceived = ndx;  // save the number for use when printing
                ndx = 0;
                newData = true;
            }
        }

        else if (rb == startMarker) {
            recvInProgress = true;
        }
    }

    for (int i = 0; i < numReceived; i++) {
        received_data[i] = receivedBytes[i];      
    }

    COBS_decode();
    
   
}

void showNewData() {
    if (newData == true) {
        Serial1.print("This just in (HEX values)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial1.print(decoded_data[n]);
            Serial1.print(' ');
        }
        Serial1.println();
        newData = false;
    }
}


void COBS_decode() {
    
    int len_rec = sizeof(received_data)/sizeof(received_data[0]);    
    uint8_t sum_check_rec = received_data[2];
    uint8_t sum_check_calc = 0;
    int start_tag = 20;
    int end_tag = 21;

        
    int COBS_start = received_data[0];
    int COBS_end = received_data[1];
    
    for (int i = 3; i < len_rec; i++) {
      
      int current = received_data[i];              
      
      if (i == COBS_start) {
        decoded_data[i-3] = start_tag;
        COBS_start = current;
      } 
      
      else if (i == COBS_end) {
        decoded_data[i-3] = end_tag;
        COBS_end = current;
      }

      else {

        decoded_data[i-3] = current;
        
      }
     }

      int len_dec = sizeof(decoded_data)/sizeof(decoded_data[0]);
      
      for (int i = 0; i < len_dec; i++) {
        sum_check_calc += decoded_data[i];
      }
    
      if (numReceived == 60 && (sum_check_rec != sum_check_calc)) {
        Serial1.println("SUM CHECK ERROR");
        Serial1.println(sum_check_calc);
        Serial1.println(sum_check_rec);

    
    }

  
}
