import pandas as pd
import sys, os, pefile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from value.header_value import header_value

# header 데이터 추출 후 list에 저장
def ExtractHeaderToList(pe, field_path, list_value):
    try:
        header_name, field_name = field_path.split('/')
        header_obj = getattr(pe, header_name, None)
        
        if header_obj and hasattr(header_obj, field_name):
            value = getattr(header_obj, field_name)
            if isinstance(value, bytes): 
                value = ' '.join([f'{byte:02x}' for byte in value])
            elif isinstance(value, int):
                value = hex(value)
        else:
            value = None
    except:
        value = None  
        pass

    list_value.append(value)

# header 데이터 추출
def ExtractHeader(file_path, list_value):
    pe = pefile.PE(file_path)

    for field_path in header_value:
        ExtractHeaderToList(pe, field_path, list_value)
