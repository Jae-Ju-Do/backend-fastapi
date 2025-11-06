import sys, os, pefile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from value.api_value import dll_list

# dll 데이터 추출
def ExtractDll(file_path, list_value):
    pe = pefile.PE(file_path)
    
    value = [0] * len(dll_list)

    try:
        for import_entry in pe.DIRECTORY_ENTRY_IMPORT:
            if import_entry.dll.decode() in dll_list:
                index = dll_list.index(import_entry.dll.decode())
                value[index] += 1
    except:
        pass
    finally:
        list_value += value