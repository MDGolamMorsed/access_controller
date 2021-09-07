import ig100_serial_configuration
import json, time
import serial_read  #file importing
import paho.mqtt.client as mqtt
import threading
import gpio_controll, send_server_response_to_openmv



broker_address = "3.129.251.210"
pub_topic = "A840411BE7CBPUB"
sub_topic = "A840411BE7CBSUB"

door_topic = "A840411BE7CBDOOR"

led_topic = "A840411BE7CBLED"

value = ""
cmd = ""



def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+ str(rc))
  client.subscribe(sub_topic)
  client.subscribe( door_topic )
  client.subscribe( led_topic )

def on_message(client, userdata, msg): 
  cmd = msg.payload.decode()
  global shadow
  shadow = cmd
  print("on message:########")
  print( len(cmd) )
  print(cmd)
  send_server_response_to_openmv.decode_json(shadow)
  #client.disconnect()   #otherwise it will sub its own pub cmd



def parse_value_to_server():
    gpio_controll.gpio_setup()
    while 1:
        gpio_controll.rx_tx_controll_pin(0)
        serial_read.main()
        print("Publishing message to topic",pub_topic)
        client.publish(pub_topic, serial_read.json_dump ) #  str(value)

    
    
    
if __name__ == "__main__":
  
    
    client = mqtt.Client()
    client.connect(broker_address,1883,60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()   #loop_forever() will be run single.    loop_start() will run parallely with othertask
    
    t1 = threading.Thread(target=parse_value_to_server, args=())
    t1.start()
    t1.join()

  
         
      
      

  
 