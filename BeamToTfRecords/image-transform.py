#!/usr/bin/env python

from __future__ import print_function
import os
import apache_beam as beam
import tensorflow as tf
from argparse import ArgumentParser

tf.enable_eager_execution()

class ImageSource(beam.io.filebasedsource.FileBasedSource):
    """A source fo reading image files."""
    def __init__(self, file_pattern, has_label):
        super(ImageSource, self).__init__(file_pattern)
        self._has_label = has_label

    def read_records(self, file_name, offset_range_tracker):
        with self.open_file(file_name) as file_to_read:
            image_bytes = file_to_read.read()
            img = tf.image.decode_jpeg(image_bytes, channels=3).numpy()
            
            # Get the string label from its parent folder
            label = os.path.basename(os.path.dirname(file_name)) if self._has_label else None

            yield img, label, file_name


class ReadFromImage(beam.PTransform):
    """A class for reading image files"""
    def __init__(self, file_pattern, has_label=False, **kwargs):
        super(ReadFromImage, self).__init__(**kwargs)
        self._source = ImageSource(file_pattern, has_label) 

    def expand(self, pvalue):
        return pvalue.pipeline | beam.io.Read(self._source)


class TFExampleFromImageDoFn(beam.DoFn):
    """A class for transforming images to TF Examples"""

    def __init__(self, has_label=False):
        self._has_label = has_label

    def process(self, element):
        img, label, file_name = element

        def _bytes_feature(value):
            return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

        def _int_feature(value):
            return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

        def _float_feature(value):
            return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
        
        pixels = img.tobytes()
        width, height, _ = img.shape

        feature = {
            'image/bytes': _bytes_feature(pixels),
            'image/width': _int_feature(width),
            'image/height': _int_feature(height),
            'image/filename': _bytes_feature(file_name)
        }

        if self._has_label:
            feature['label'] = _bytes_feature(label)

        example = tf.train.Example(features=tf.train.Features(feature=feature))

        yield example

def run_pipeline():
    parser = ArgumentParser(description='Create TFRecord files from directories using Apache Beam')

    parser.add_argument('--input_directory', help='Base directory for images')
    parser.add_argument('--output_directory', help='Base directory for tfrecord output')
    parser.add_argument('--dataset_name', help='Name of the dataset. Used for file naming conventions')
    parser.add_argument('--num_shards', default=2, type=int, help='Number of shards to split the dataset into')
    parser.add_argument('--has_labels', action='store_true', help='Whether the folder structure includes labels')
    args, pipeline_args = parser.parse_known_args()

    path_expression = os.path.join(args.input_directory, '**/*.jpg')
    output_path = os.path.join(args.output_directory, args.dataset_name)

    with beam.Pipeline(argv=pipeline_args) as p: 
        images = p | ReadFromImage(path_expression, args.has_labels)
        
        _ = (
            images
            | 'MakeTfExample' >> beam.ParDo(TFExampleFromImageDoFn(has_label=args.has_labels))
            | 'SaveTfRecords' >> beam.io.WriteToTFRecord(
                output_path, file_name_suffix='.tfrecord', num_shards=args.num_shards,
                shard_name_template='-SS',
                coder=beam.coders.ProtoCoder(tf.train.Example))
        )

if __name__ == '__main__':
    run_pipeline()
