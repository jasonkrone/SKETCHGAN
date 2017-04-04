from scipy.misc import imread
from random import shuffle
import time, os

import tensorflow as tf
from glob import glob
from utils import get_image, colorize
# this is based on tensorflow tutorial code
# https://github.com/tensorflow/tensorflow/blob/r0.8/tensorflow/examples/how_tos/reading_data/convert_to_records.py
# TODO: it is probably very wasteful to store these images as raw numpy
# strings, because that is not compressed at all.
# i am only doing that because it is what the tensorflow tutorial does.
# should probably figure out how to store them as JPEG.

IMSIZE = 256
NUM_CLASSES = 125

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def make_file_class_csv(data_dir):
	d = {}
	file = open("class_labels.csv", "w")
	for root, dirs, files in os.walk(data_dir):
		for i, name in enumerate(dirs):
			d[name] = i
			file.write(str(i) + ',' + name + '\n')
	file.close()
	return d

def main(argv):	
	#file_class_dict = make_file_class_csv('TODO')
    pattern = \
    "/a/h/jkrone02/Downloads/rendered_256x256/256x256/photo/tx_000100000000/*/*jpg"
    print 'input data:', pattern
    files = glob(pattern)
    print 'files:', files[:5], len(files)

    dirs = glob("/a/h/jkrone02/Downloads/rendered_256x256/256x256/photo/tx_000100000000/*")
    print 'class dirs:', dirs
    assert len(dirs) == NUM_CLASSES, len(dirs)
    dirs = [d.split('/')[-1] for d in dirs]
    dirs = sorted(dirs)
    print 'classes:', dirs
    str_to_int = dict(zip(dirs, range(len(dirs))))
    outfile = '/a/h/jkrone02/sketchy_photos' + '.tfrecords'
    writer = tf.python_io.TFRecordWriter(outfile)

    for i, f in enumerate(files):
        print i
        image = get_image(f, IMSIZE, is_crop=True, resize_w=IMSIZE)
        image = colorize(image)
        assert image.shape == (IMSIZE, IMSIZE, 3)
        #image += 1.
        #image *= (255. / 2.)
        image = image.astype('uint8')
        #print image.min(), image.max()
        # from pylearn2.utils.image import save
        # save('foo.png', (image + 1.) / 2.)
        image_raw = image.tostring()
        class_str = f.split('/')[-2]
        label = str_to_int[class_str]
        if i % 1 == 0:
            print i, '\t',label
        example = tf.train.Example(features=tf.train.Features(feature={
            'height': _int64_feature(IMSIZE),
            'width': _int64_feature(IMSIZE),
            'depth': _int64_feature(3),
            'image_raw': _bytes_feature(image_raw),
            'label': _int64_feature(label)
            }))
        writer.write(example.SerializeToString())

    writer.close()

if __name__ == "__main__":
    tf.app.run()
