# import numpy as np

# import tensorflow as tf
# import tensorflow_hub as hub

import json
import PIL.Image as Image
import keras
import boto3
from keras.models import Sequential, load_model
from keras import backend as K
import numpy as np
import cv2
import os
import sys

resArr = []
colors = 3
img_cols = 128
img_rows = 128
num_classes = 2

model_paths = ['/tmp/model_0_prime.h5', '/tmp/model_1_prime.h5',
               '/tmp/model_2_prime.h5', '/tmp/model_3_prime.h5', '/tmp/model_4_prime.h5']


IMAGE_SHAPE = (img_cols, img_rows)
client = boto3.client('s3')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print("Lambda Handler 10")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print("Bucket Name: ", bucket_name, " Key: ", key)

    downloadModelFromBucket(bucket_name)
    print("Success Download")
    print("OS List Dir", os.listdir("/tmp/"))

    img = readImageFromBucket(key, bucket_name).resize(IMAGE_SHAPE)
    img = np.array(img)/255.0

    print("Read Image")

    # prediction = model.predict(img[np.newaxis, ...])
    # predicted_class = imagenet_labels[np.argmax(prediction[0], axis=-1)]

    # print('ImageName: {0}, Prediction: {1}'.format(key, predicted_class))
    for mdl in model_paths:
        print(mdl)
        # img = cv2.imread(sys.argv[1])[..., ::-1]
        # img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (128, 128))
        test_img = []
        test_img.append(img)
        test_img = np.array(test_img)
        test_img = test_img.astype('float32')
        test_img /= 255
        model = load_model(mdl)
        resArr.append(np.round(model.predict(test_img), decimals=3))

    return {
        'statusCode': 200,
        'body': json.dumps(resArr)
    }


def readImageFromBucket(key, bucket_name):
    bucket = s3.Bucket(bucket_name)
    object = bucket.Object(key)
    response = object.get()
    return Image.open(response['Body'])


def downloadModelFromBucket(bucket_name):
    client.download_file(bucket_name, 'model_0_prime.h5',
                         '/tmp/model_0_prime.h5')
    client.download_file(bucket_name, 'model_1_prime.h5',
                         '/tmp/model_1_prime.h5')
    client.download_file(bucket_name, 'model_2_prime.h5',
                         '/tmp/model_2_prime.h5')
    client.download_file(bucket_name, 'model_3_prime.h5',
                         '/tmp/model_3_prime.h5')
    client.download_file(bucket_name, 'model_4_prime.h5',
                         '/tmp/model_4_prime.h5')
