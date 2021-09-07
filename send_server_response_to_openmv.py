import json, time 
import gpio_controll, ig100_serial_configuration, door_controll_timer, wiegand_sender

def decode_json(payload):
    json_string = json.loads( payload )
    status_code = json_string['AccessStatus']
    rfid_value = json_string['RFID']

    if status_code == 1:
        gpio_controll.door_open( json_string["DoorID"] )
        
        wiegand = wiegand_sender.WiegandSender()
        wiegand.begin(26, 19,1)
        if len(rfid_value) > 0:
            wiegand.test(int(rfid_value))  #1C7784 > 1865604
        
  
        door_controll_timer.set_door_timer( json_string["DoorID"] )
        #time.sleep(2)
        print("cmd send to mega on message1")
        gpio_controll.rx_tx_controll_pin(1)
        #time.sleep(1)
        ig100_serial_configuration.ser.write( "success".encode() )
        time.sleep(.5)
        gpio_controll.rx_tx_controll_pin(0)
    elif status_code == 0:
        
        print("cmd send to mega on message0")
        gpio_controll.rx_tx_controll_pin(1)
        #time.sleep(1)
        ig100_serial_configuration.ser.write( "unsuccess".encode() )
        time.sleep(.5)
        gpio_controll.rx_tx_controll_pin(0)