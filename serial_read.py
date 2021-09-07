import serial, time, os, json, base64
import codecs
import json_parser
import ig100_serial_configuration

from PIL import Image

from io import BytesIO

i = 0


json_read_flag = 0
port = "/dev/serial0"                 #ttyS0   ttyACM1  serial0   ttyAMAO
hex_value = ""
img = ""
flag = False
image_length = 0


 
def main():
    print("hi")
    #while True:
    try:
        print("Keyboard Interrupt2")
        json_read_from_openmv()
        camera_value_read_from_openmv()    
        #convert_camera_value_to_image()      #for ensure image is not truncated
            
                
            
                
    except AssertionError as e:
        print("Keyboard Interrupt")
        print(e)
            #break
            
            
            

def json_read_from_openmv():
    global  json_string, json_read_flag, image_length 
    while True:
        if ig100_serial_configuration.ser.inWaiting() > 0 and json_read_flag == 0:
            value = ig100_serial_configuration.ser.readline() #str(response_json).strip("'<>() ").replace('\'', '\"')
            
            #print( bytes(value) )
            try: 
                print(value)
                print("json_read_from_openmv")
                value = value.decode().rstrip().replace('\x00', '')
                print(value)
                json_read_flag = 1
                json_string = json.loads((value) )
                image_length = json_string['ImageLength']
                print(image_length)
                print("\n\n\n")
                #camera_value_read_from_openmv()
                break
            except ValueError as e:
                print('Response content is not in the json format')
                print(e)
                print('Response content is not in the json format')
                #break
            





def camera_value_read_from_openmv():
    global hex_value, i, json_read_flag, image_length
    #ig100_serial_configuration.ser.flushInput()
    while True:
        #print("json_read_flag: ")
        #print(json_read_flag)
        #time.sleep(1)
        if ig100_serial_configuration.ser.inWaiting() > 0 and json_read_flag == 1:
            value = ig100_serial_configuration.ser.read()
            #print(type(value))
            # print(type(hex))
            #print(value)
            #print(value.hex())
            #print("\n\n\n")
            # hex.append( value.hex() )
            hex_value += str(value.hex())
            #img += str(value)
            # flag = True
            i+=1
            #print(i)
            
        if i >= image_length:  # 153600   4140   307200  24624  2120
            ig100_serial_configuration.ser.flushInput()
            json_payload()
            i = 0
            json_read_flag = 0
            break



def json_payload():   
    global b64, hex_value, json_dump
    #print("####################################################### HEX OUTPUT ########################################################################################")
    # print( len(hex) )
    #print(hex_value)

    b64 = codecs.encode(codecs.decode(hex_value, 'hex'), 'base64').decode()

    #print("############################################################################### BASE64 OUTPUT ################################################################")
    #print(b64)
    # print( len(b64) )
    # print(  "############################################################################### BASE64 OUTPUT ################################################################")

    
    flag = False

    #json_value = json_parser.json_payload
    json_string["Camera"] = b64.replace('\n', '')

    json_dump = json.dumps(json_string)


    print((json_dump))
    print(len(json_dump))
    hex_value = ""
    img = ""


def convert_camera_value_to_image():        #for ensure image is not truncated
    
    im = Image.open(BytesIO(base64.b64decode(b64)))
    im.show()
    im.save('image.jpg')
    print("saved")
    print("\n\n\n")









if __name__ == "__main__":
    main()
    
    


    
       
