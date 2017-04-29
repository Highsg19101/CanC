import tensorflow as tf
from nets import inception_v3
from preprocessing import inception_preprocessing
from scipy.misc import imshow, imread

def deduction():
    slim = tf.contrib.slim
    batch_size = 3
    image_size = 299

    with tf.Graph().as_default():
        with slim.arg_scope(inception_v3.inception_v3_arg_scope()):

            imgPath = 'test4.jpg'
            testImage_string = tf.gfile.FastGFile(imgPath, 'rb').read()
            testImage = tf.image.decode_jpeg(testImage_string, channels=3)
            processed_image = inception_preprocessing.preprocess_image(testImage, image_size, image_size, is_training=False)
            processed_images = tf.expand_dims(processed_image, 0)

            logits, _ = inception_v3.inception_v3(processed_images, num_classes=2, is_training=False)
            probabilities = tf.nn.softmax(logits)
            checkpoint_path = tf.train.latest_checkpoint('/home/lee/ABO2/models/slim/CanC/train')
            init_fn = slim.assign_from_checkpoint_fn(
            checkpoint_path, slim.get_model_variables('InceptionV3'))

            with tf.Session() as sess:
                init_fn(sess)

                np_image, probabilities = sess.run([processed_images, probabilities])
                probabilities = probabilities[0, 0:]
                sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x: x[1])]
            
                names = ['mouse', 'wallet']
                for i in range(2):
                    index = sorted_inds[i]
                    print((probabilities[index], names[index]))
                    return names[sorted_inds[0]]
