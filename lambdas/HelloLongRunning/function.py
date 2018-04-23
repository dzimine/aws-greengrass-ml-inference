import os
import sys
from threading import Timer

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import greengrasssdk


# Creating a greengrass core sdk client
# client = greengrasssdk.client('iot-data')

INTERVAL = int(os.environ.get('INTERVAL', '5'))


def run():
    print "Executing run..."
    # client.publish(topic='hello/world', payload='Hello from Greengrass Core.')

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(INTERVAL, run).start()

# Start executing the function above
run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def handler(event=None, context=None):
    return
