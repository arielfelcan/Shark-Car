import sensor
import time
import math
import time
from mqtt import MQTTClient
import network
import time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Tufts_Robot", "")
while wlan.ifconfig()[0] == '0.0.0.0':
    print('.', end=' ')
    time.sleep(1)
# We should have a valid IP now via DHCP
print(wlan.ifconfig())
mqtt_broker = 'broker.hivemq.com'
port = 1883
topic_pub = 'ME35-24/ari'
client = MQTTClient('repl1', mqtt_broker , port, keepalive=60)
client.connect()
print('Connected to %s MQTT broker' % (mqtt_broker))
# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.
# Please use the TAG36H11 tag family for this script - it's the recommended tag family to use.
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()
while True:
    # clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():
        img.draw_rectangle(tag.rect, color=(255, 0, 0))
        img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))
        print_args = (tag.name, tag.id, (180 * tag.rotation) / math.pi)
#        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
        msg = str((180 * tag.rotation) / math.pi)
        print(msg)
        try:
            # client.publish(topic_pub.encode(), msg.encode())
            client.publish(topic_pub, msg)
            print(f"Published message: {msg}")
        except Exception as e:
            print(f"Failed to publish message: {e}")
#    print(clock.fps())
    time.sleep(0.1)
