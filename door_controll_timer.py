import threading, time
import gpio_controll


timer = 10



def door_timer_start(door_id):
    previous_time = time.time()
    while True:
        present_time = time.time()
        if present_time - previous_time > 5:
            gpio_controll.door_close( door_id )
            break
      





def set_door_timer(door_id):
    t2 = threading.Thread(target=door_timer_start, args=( door_id, ))
    t2.start()
    #t2.join() 
    


if __name__ == "__main__":
    gpio_controll.gpio_setup()
    set_door_timer(1)
    set_door_timer(2)
    set_door_timer(3)
    print("i")