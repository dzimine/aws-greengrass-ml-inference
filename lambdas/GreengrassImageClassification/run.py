import sys
import glob
import time
import os
import model

WATCH_PATTERN = os.environ.get('WATCH_PATTERN', './input/*.jpeg')
MODEL_PATH = os.environ.get('MODEL_PATH', './squeezenet/')

global_model = model.ImagenetModel(MODEL_PATH + 'synset.txt', MODEL_PATH + 'squeezenet_v1.1')


def run_image_classification():
    while True:
        for fn in glob.glob(WATCH_PATTERN):

            try:
                with open(fn, 'r') as f:
                    image = f.read()
                prediction = global_model.predict_from_image(image)
                print prediction
            except:
                e = sys.exc_info()[0]
                print("Exception occured during prediction: %s" % e)
            os.remove(fn)

            time.sleep(2)


# When run as Lambda, this will be invoked
run_image_classification()


# Dummy function handler, not invoked for long-running lambda
def handler(event, context):
    return
