#! /usr/env/bin python3

import argparse
import os
import sys
import glob
import pickle
import tensorflow as tf
import numpy as np
from PIL import Image

def _int64_feature(value):
    """Create a Int64List Feature
    
    Args:
        value: The value to store in the feature
    
    Returns:
        The FeatureEntry
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    """Create a BytesList Feature
    
    Args:
        value: The value to store in the feature
    
    Returns:
        The FeatureEntry
    """
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def convert_to_tfrecord(dataset_name, data_directory, class_map, segments=1, directories_as_labels=True, files='**/*.jpg'):
    """Convert the dataset into TFRecords on disk
    
    Args:
        dataset_name:   The name/folder of the dataset
        data_directory: The directory where records will be stored
        class_map:      Dictionary mapping dictory label name to integer label
        segments:       The number of files on disk to separate records into
        directories_as_labels: Whether the directory name should be used as it's label (used for test directory)
        files:          Which files to find in the data directory
    """
    
    # Create a dataset of file path and class tuples for each file
    filenames = glob.glob(os.path.join(data_directory, files))
    classes = (os.path.basename(os.path.dirname(name)) for name in filenames) if directories_as_labels else [None] * len(filenames)
    dataset = list(zip(filenames, classes))
    
    # If sharding the dataset, find how many records per file
    num_examples = len(filenames)
    samples_per_segment = num_examples // segments
    
    print(f"Have {samples_per_segment} per record file")
    
    for segment_index in range(segments):
        start_index = segment_index * samples_per_segment
        end_index = (segment_index + 1) * samples_per_segment
        
        sub_dataset = dataset[start_index:end_index]
        record_filename = os.path.join(data_directory, f"{dataset_name}-{segment_index}.tfrecords")

        with tf.python_io.TFRecordWriter(record_filename) as writer:
            print(f"Writing {record_filename}")

            for index, sample in enumerate(sub_dataset):
                sys.stdout.write(f"\rProcessing sample {start_index+index+1} of {num_examples}")
                sys.stdout.flush()

                file_path, label = sample
                image = Image.open(file_path)
                image = image.resize((224, 224))
                image_raw = np.array(image).tostring()
                
                features = {
                    'label': _int64_feature(class_map[label]),
                    'text_label': _bytes_feature(label),
                    'image': _bytes_feature(image_raw)
                }
                example = tf.train.Example(features=tf.train.Features(feature=features))
                writer.write(example.SerializeToString())   

def process_directory(data_directory:str):
    """Process the directory to convert images to TFRecords"""

    data_dir = os.path.expanduser(data_directory)
    train_data_dir = os.path.join(data_dir, 'train')

    class_names = os.listdir(train_data_dir) # Get names of classes
    class_name2id = { label: index for index, label in enumerate(class_names) } # Map class names to integer labels

    # Persist this mapping so it can be loaded when training for decoding
    with open(os.path.join(data_directory, 'class_name2id.p'), 'wb') as p:
        pickle.dump(class_name2id, p, protocol=pickle.HIGHEST_PROTOCOL)
    
    convert_to_tfrecord('train', data_dir, class_name2id, segments=4)
    convert_to_tfrecord('validation', data_dir, class_name2id)
    convert_to_tfrecord('test', data_dir, class_name2id, directories_as_labels=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--data-directory', 
        default='~/data/mnist',
        help='Directory where TFRecords will be stored')

    args = parser.parse_args()
    process_directory(args.data_directory)