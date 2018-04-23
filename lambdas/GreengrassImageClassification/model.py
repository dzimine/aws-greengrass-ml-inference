import mxnet as mx
import numpy as np
# import picamera
import time
import io
import cv2
import urllib2
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])


class ImagenetModel(object):

    # Loads a pre-trained model locally or from an external URL
    # and returns an MXNet graph that is ready for prediction
    def __init__(self, synset_path, network_prefix, params_url=None,
                 symbol_url=None, synset_url=None, context=mx.cpu(),
                 label_names=['prob_label'], input_shapes=[('data', (1, 3, 224, 224))]):

        # Download the symbol set and network if URLs are provided
        if params_url is not None:
            fetched_file = urllib2.urlopen(params_url)
            with open(network_prefix + "-0000.params", 'wb') as output:
                output.write(fetched_file.read())

        if symbol_url is not None:
            fetched_file = urllib2.urlopen(symbol_url)
            with open(network_prefix + "-symbol.json", 'wb') as output:
                output.write(fetched_file.read())

        if synset_url is not None:
            fetched_file = urllib2.urlopen(synset_url)
            with open(synset_path, 'wb') as output:
                output.write(fetched_file.read())

        # Load the symbols for the networks
        with open(synset_path, 'r') as f:
            self.synsets = [l.rstrip() for l in f]

        # Load the network parameters from default epoch 0
        sym, arg_params, aux_params = mx.model.load_checkpoint(network_prefix, 0)

        # Load the network into an MXNet module and bind the corresponding parameters
        self.mod = mx.mod.Module(symbol=sym, label_names=label_names, context=context)
        self.mod.bind(for_training=False, data_shapes=input_shapes)
        self.mod.set_params(arg_params, aux_params)
        self.camera = None

    def predict_from_image(self, image, reshape=(224, 224), top=5):
        top_n = []

        # Construct a numpy array from the stream
        data = np.fromstring(image, dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        cvimage = cv2.imdecode(data, 1)

        # Switch RGB to BGR format (which ImageNet networks take)
        img = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        if img is None:
            return top_n

        # Resize image to fit network input
        img = cv2.resize(img, reshape)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]

        # Run forward on the image
        self.mod.forward(Batch([mx.nd.array(img)]))
        prob = self.mod.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)

        # Extract the top N predictions from the softmax output
        a = np.argsort(prob)[::-1]
        for i in a[0:top]:
            top_n.append((prob[i], self.synsets[i]))
        return top_n

    # Captures an image from the PiCamera, then sends it for prediction
    def predict_from_cam(self, capfile='cap.jpg', reshape=(224, 224), top=5):
        if self.camera is None:
            self.camera = picamera.PiCamera()

        stream = io.BytesIO()
        self.camera.start_preview()
        time.sleep(2)
        self.camera.capture(stream, format='jpeg')
        return self.predict_from_image(stream.getvalue(), reshape, top)
