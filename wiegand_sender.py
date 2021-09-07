import RPi.GPIO as GPIO
import time

MAP = [0]*100
BITSMAP = [0]*100
k = 0

class WiegandSender:
    BIT_DELAY= 0.000075  #0.0000001  == 1 milisecond
    IDEAL_DELAY= 0.00105 
    
    def __init__(self):
        alive = True 
           
    
    
    def begin(self, D0,D1, Mode = 1):
        alive = True
        self.WD0 = D0
        self.WD1 = D1
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.WD0, GPIO.OUT)
        GPIO.setup(self.WD1, GPIO.OUT)
        GPIO.output(self.WD0, GPIO.HIGH)
        GPIO.output(self.WD1, GPIO.HIGH)
        
        MAP[0] = "0000"     
        BITSMAP[0] = 0 
        
        MAP[1] = "0001"
        BITSMAP[1] = 1   
        
        MAP[2] = "0010"     
        BITSMAP[2] = 1    
        
        MAP[3] = "0011"     
        BITSMAP[3] = 2 
        
        MAP[4] = "0100"     
        BITSMAP[4] = 1
        
        MAP[5] = "0101"     
        BITSMAP[5] = 2   
        
        MAP[6] = "0110"     
        BITSMAP[6] = 2   
        
        MAP[7] = "0111"     
        BITSMAP[7] = 3   
        
        MAP[8] = "1000"     
        BITSMAP[8] = 1    
        
        MAP[9] = "1001"     
        BITSMAP[9] = 2    
        
        MAP[10] = "1010"    
        BITSMAP[10] = 2  
        
        MAP[11] = "1011"    
        BITSMAP[11] = 3    
        
        MAP[12] = "1100"   
        BITSMAP[12] = 2 
        
        MAP[13] = "1101"   
        BITSMAP[13] = 3    
        
        MAP[14] = "1110"    
        BITSMAP[14] = 3    
        
        MAP[15] = "1111"    
        BITSMAP[15] = 4    

    
    
    
    def available(self):
        return self.available_data
        
        
    def read(self):
        return self.RECEIVED_CARD_ID
        
        
    def readD0(self):
        self.Bits[currentPoint] = 0
        self.lastTaken = time.time()
        self.currentPoint += 1
        
    def readD1(self):
        self.Bits[currentPoint] = 1
        self.lastTaken = time.time()
        self.currentPoint += 1
        
        
    def send(self, data):
        dataL = len(data)
        WiegandSender.sendStartParity( self, data )
        
        for i in range(dataL):
            #print(i)
            Extra = 0
            Deci = 0
            
            if ( (data[i] >= 'a' and data[i] <= 'f')  or (data[i] >= 'A' and data[i] <= 'F') ):
                if data[i] >= 'a' and data[i] <= 'f' :
                    Extra = 10 + ord(data[i]) - ord('a')
                else:
                    Extra = 10 + ord(data[i]) - ord('A')
                    
                   
            elif data[i] >= '0' and data[i] <= '9':
                Deci = ord(data[i]) - ord('0')
            
            else:
                WiegandSender.sendStopParity(self, data)
                print("Invalid character in ID")
                print(i)
                return
                
                
                
            for j in range(0, 4):
                if MAP[Extra + Deci] [j] == '0':
                    WiegandSender.sendZero(self,False)
            
                elif MAP[Extra + Deci] [j] == '1':
                    WiegandSender.sendOne( self,False )
                    
                    
        WiegandSender.sendStopParity( self,data ) 
        
        
        
    def sendZero(self, lastbit = False):
        GPIO.output(self.WD0, GPIO.LOW)
        time.sleep(self.BIT_DELAY)
        GPIO.output(self.WD0, GPIO.HIGH)
        time.sleep(self.IDEAL_DELAY)
        print("0", end = "")
        
        
    def sendOne( self, lastbit = False ):
        GPIO.output( self.WD1, GPIO.LOW)
        time.sleep(self.BIT_DELAY)
        GPIO.output( self.WD1, GPIO.HIGH)
        time.sleep(self.IDEAL_DELAY)
        print("1", end="")                
    

    def sendStartParity( self, data ):
        dataL = len(data)
        print(dataL)
        if dataL%2 == 0:
            FH = data[0 : int(dataL/2)]
            sum = 0
            for i in range(0, len(FH) ):
                Extra = 0
                Deci = 0
                if data[i] >= 'a' and data[i] <= 'f' or data[i] >= 'A' and data[i] <= 'F':
                    if data[i] >= 'a' and data[i] <= 'f':
                        
                        Extra = 10 + ord(FH[i]) - ord('a')
                    else:
                        Extra = 10 + ord(FH[i]) - ord('A')
                elif FH[i] >= '0' and FH[i] <= '9':
                    Deci = ord(FH[i]) - ord('0')
                else:
                    pass
                sum += BITSMAP[Extra + Deci]
                
                
                if( sum%2 == 1):
                    WiegandSender.sendOne(self, False)
                else:
                    WiegandSender.sendZero(self, False)
                    
                    
                    
                    
                    
                    
    def sendStopParity(self, data):
        dataL = len(data)
        if dataL % 2 == 0:
            FH = data[0 : int(dataL/2) ]
            sum = 0
        
            for i in range(0, len(FH) ):
                Extra = 0
                Deci = 0
                
                if data[i] >= 'a' and data[i] <='f' or data[i] >= 'A' and data[i] <= 'F':
                    if data[i] >= 'a' and data[i] <= 'f' :
                        Extra = 10 + ord(FH[i]) - ord('a')
                        
                    else:
                        Extra = 10 + ord(FH[i]) - ord('a')
                        
                elif FH[i] >= '0' and FH[i] <= '9' :
                    Deci =  ord(FH[i]) - ord('0')
                else:
                    pass
                    
                sum += BITSMAP[Extra + Deci]
                
            if sum%2 == 0:
                WiegandSender.sendOne(self, True)
            else:
                WiegandSender.sendZero(self, True)
            
    def test(self, data):
        global k, bin_list_value
        k = 0
        bin_value = bin(data)
        bin_list_value = list( bin_value )
        bin_list_value = bin_list_value[2:]
        print(bin_list_value)
        
        for i in bin_list_value:
            k += 1
        print(k)
        
        if k > 12:
            second_odd_parity_field = bin_list_value[-12:]
            print(second_odd_parity_field)
            
            
            WiegandSender.find_first_even_parity(self) 
            WiegandSender.add_parity_checker(self)
            WiegandSender.send_first_even_parity_filed(self)
            WiegandSender.send_second_odd_parity_filed(self)
            WiegandSender.find_second_odd_parity(self)
        else:
            print("short")
            bin_list_value_shadow = bin_list_value.copy()
            print( bin_list_value_shadow )
            for i in range(0, 24 - k):
                if i < k:
                    bin_list_value[i] = 0
                else:
                    bin_list_value.append(0)
            for i in range(0 , k):
                print(bin_list_value_shadow[i] )
                bin_list_value.append( bin_list_value_shadow[i] )
            print( bin_list_value )
            
            
            ##################################
            k = 0
            bin_list_value = bin_list_value[2:]
            print(bin_list_value)
            
            for i in bin_list_value:
                k += 1
            print(k)
            
            if k > 12:
                second_odd_parity_field = bin_list_value[-12:]
                print(second_odd_parity_field)
                
                
                WiegandSender.find_first_even_parity(self) 
                WiegandSender.add_parity_checker(self)
                WiegandSender.send_first_even_parity_filed(self)
                WiegandSender.send_second_odd_parity_filed(self)
                WiegandSender.find_second_odd_parity(self)
        
        
    def find_first_even_parity(self):
        global first_even_parity_field_length
        even_parity_flag = 0
        first_even_parity_field_length = 0
        for i in range(0, 12-(24-k) ):
            #print( bin_list_value[i] )
            if bin_list_value[i] == "1":
                even_parity_flag += 1
            first_even_parity_field_length += 1

        
        if even_parity_flag % 2 == 0:
            WiegandSender.sendZero(self, False)
        else:
            WiegandSender.sendOne(self, False)
            
    def add_parity_checker(self):
        for i in range(0, (12-first_even_parity_field_length) ):
            #print( bin_list_value[i] )
            WiegandSender.sendZero(self, False)
            
            
            
    def send_first_even_parity_filed(self):
        for i in range(0, 12-(24-k) ):
            #print( bin_list_value[i] )  
            if int(bin_list_value[i]) % 2 == 0:
                WiegandSender.sendZero(self, False)
            else:
                WiegandSender.sendOne(self, False)
                
                
    def send_second_odd_parity_filed(self):
        for i in range(12-(24-k), 24-(24-k) ):
            #print( bin_list_value[i] )        
            if int(bin_list_value[i]) % 2 == 0:
                WiegandSender.sendZero(self, False)
            else:
                WiegandSender.sendOne(self, False)
        
        
    def find_second_odd_parity(self):

        odd_parity_flag = 0
        first_even_parity_field_length = 0
        for i in range(12-(24-k), 24-(24-k) ):
            #print( bin_list_value[i] )
            if bin_list_value[i] == "1":
                odd_parity_flag += 1
            

        print("odd parity flag: ", odd_parity_flag)
        if odd_parity_flag % 2 != 0:
            WiegandSender.sendZero(self, False)
        else:
            WiegandSender.sendOne(self, False)
        



        

if __name__ == "__main__":
    wiegand = WiegandSender()
    #wiegand.begin(9,11,1)
    wiegand.begin(26, 19,1)
    #wiegand.send("1865602")  #1C7784 > 1865604
    
    #wiegand.send("1C7784")
    wiegand.test(1865604)
    time.sleep(1)
    wiegand.test(16777211)
    time.sleep(1)
    wiegand.test(16777011)
    time.sleep(1)
    wiegand.test(16347211)
    time.sleep(1)
    wiegand.test(1211)

















