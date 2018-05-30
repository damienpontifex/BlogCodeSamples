#!/usr/bin/env python

from __future__ import print_function
import os
import apache_beam as beam
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from argparse import ArgumentParser

class ImageSource(beam.io.filebasedsource.FileBasedSource):
    """A source fo reading image files."""
    def __init__(self, file_pattern, has_label):
        super(ImageSource, self).__init__(file_pattern)
        self._has_label = has_label

    def read_records(self, file_name, offset_range_tracker):
        with self.open_file(file_name) as file_to_read:
            image_bytes = file_to_read.read()
            img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            label = os.path.basename(os.path.dirname(file_name)) if self._has_label else None

            yield img, label


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
        img, label = element
        assert isinstance(img, Image.Image)

        def _bytes_feature(value):
            return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

        def _int_feature(value):
            return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

        def _float_feature(value):
            return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
        
        pixels = np.array(img).tobytes()
        width, height = img.size

        feature = {
            'image': _bytes_feature(pixels),
            'width': _int_feature(width),
            'height': _int_feature(height)
        }

        if self._has_label:
            feature['label'] = _bytes_feature(label)

        example = tf.train.Example(features=tf.train.Features(feature=feature))

        yield example

def main(args):
    path_expression = os.path.join(args.input_directory, '**/*.jpg')
    output_path = os.path.join(args.output_directory, args.dataset_name)

    pipeline_options = beam.pipeline.PipelineOptions()
    with beam.Pipeline(options=pipeline_options) as p: 
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
    parser = ArgumentParser(description='Create TFRecord files from directories using Apache Beam')

    parser.add_argument('--input_directory', help='Base directory for images')
    parser.add_argument('--output_directory', help='Base directory for tfrecord output')
    parser.add_argument('--dataset_name', help='Name of the dataset. Used for file naming conventions')
    parser.add_argument('--num_shards', default=2, type=int, help='Number of shards to split the dataset into')
    parser.add_argument('--has_labels', action='store_true', help='Whether the folder structure includes labels')
    args = parser.parse_args()

    main(args)