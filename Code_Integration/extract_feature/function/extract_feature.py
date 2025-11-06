from .is_pefile import IsPefile
from .extract_header import ExtractHeader
from .extract_section import ExtractSection
from .extract_dir_entropy import ExtractDirEntropy
from .extract_export import ExtractExport
from .extract_import import ExtractImport
from .extract_dll import ExtractDll
from .extract_byte_entropy import ExtractByteEntropy
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from value.total_value import total_value

import os
import pandas as pd

# 파일의 특징 추출
def ExtractFeatureFile(dir, name):
    df = pd.DataFrame(columns=['Key', 'Value'])
    list_value = []
    list_value.append(name)
    file_path = os.path.join(dir, name)
    IsPefile(file_path, list_value)
    if list_value[1]:
        try:
            ExtractHeader(file_path, list_value)
        except Exception as e:
            list_value[2:60] = [0] * 58
            print(f"추출 오류(ExtractHeader): {e}")
            pass

        try:
            ExtractSection(file_path, list_value)
        except Exception as e:
            list_value[60:300] = [0] * 240 
            print(f"추출 오류(ExtractSection): {e}")
            pass

        try:
            ExtractDirEntropy(file_path, list_value)
        except Exception as e:
            list_value[300:348] = [0] * 48 
            print(f"추출 오류(ExtractDirEntropy): {e}")
            pass
        
        try:
            ExtractExport(file_path, list_value)
        except Exception as e:
            list_value[348:349] = [0] * 1
            print(f"추출 오류(ExtractExport): {e}")
            pass
            
        try:
            ExtractImport(file_path, list_value)
        except Exception as e:
            list_value[349:759] = [0] * 410
            print(f"추출 오류(ExtractImport): {e}")
            pass

        try:
            ExtractDll(file_path, list_value)
        except Exception as e:
            list_value[759:818] = [0] * 59
            print(f"추출 오류(ExtractDll): {e}")
            pass
        
        try:
            ExtractByteEntropy(file_path, list_value)
        except Exception as e:
            list_value[818:882] = [0] * 64 
            print(f"추출 오류(ExtractByteEntropy): {e}")
            pass
    else:
        list_value[2:] = [0] * (len(total_value) - 2)
        print("추출(IsPefile): pe 파일이 아닙니다.")

    data_dict = {'Key': total_value[:len(list_value)], 'Value': list_value}
    df = pd.DataFrame(data_dict)

    df = df.set_index('Key').T 
    return df