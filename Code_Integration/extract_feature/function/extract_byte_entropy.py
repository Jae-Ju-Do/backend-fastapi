from .calculate_entropy import CalculateEntropy
import pefile, os, math
import numpy as np
import pandas as pd

def GetWindowBlocks(byte_data, window_size=2048, step_size=1024):
    byte = np.frombuffer(byte_data, dtype=np.uint8)
    if len(byte) < window_size:
        print("Data is too small for the specified window size.")
        return np.array([]) 
    shape = byte.shape[:-1] + (byte.shape[-1] - window_size + 1, window_size)
    strides = byte.strides + (byte.strides[-1],)
    return np.lib.stride_tricks.as_strided(byte, shape=shape, strides=strides)[::step_size, :]

def EntropyHistogramFromFile(file_path, window_size=2048, step_size=1024):
    with open(file_path, 'rb') as fp:
        byte_data = fp.read()

    output = np.zeros((8, 8), dtype=np.int32)
    blocks = GetWindowBlocks(byte_data, window_size, step_size)

    if blocks.size == 0:
        print("No blocks generated.")
        return output

    for idx, block in enumerate(blocks):
        try:
            entropy = CalculateEntropy(block)
            idx = 7 if entropy == 8.0 else int(entropy)
            c = np.bincount(block >> 5, minlength=8)
            output[idx, :] += c
        except Exception as e:
            print(f"Error at block {idx}: {e}")
            pass

    return output    

def ExtractByteEntropy(file_path, list_value):
    histogram = EntropyHistogramFromFile(file_path)
    flattened_histogram = histogram.flatten()
    feature_values = list(flattened_histogram[:64])
    list_value += feature_values
