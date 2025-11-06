import numpy as np
import os, sys, pefile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from value.dir_entropy import directory_names

# dir 엔트로피 추출 
def ExtractDirEntropy(file_path, list_value):
    pe = pefile.PE(file_path)
    
    for directory_name in directory_names:
        full_directory_name = f"IMAGE_DIRECTORY_ENTRY_{directory_name}"

        directory_found = False
        for directory in pe.OPTIONAL_HEADER.DATA_DIRECTORY:
            if directory.name == full_directory_name:
                directory_found = True
                list_value.append(True)
                list_value.append(hex(directory.VirtualAddress))
                list_value.append(directory.Size)
                break
        
        if not directory_found:
            list_value.append(False) 
            list_value.append(hex(0))   
            list_value.append(0)   
            print(f"Directory {full_directory_name} not found.")