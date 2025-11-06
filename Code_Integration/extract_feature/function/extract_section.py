from .calculate_entropy import CalculateEntropy
import sys, os, pefile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from value.section_value import section_list, section_object

# selection 데이터 추출 후 list에 저장
def ExtractSectionToList(section_save, section_check, list_value):
    value = []
    if section_check:
        for key in section_object:
            if hasattr(section_save, key):
                value.append(hex(getattr(section_save, key)))
            else:
                value.append(None)
        section_data = section_save.get_data()
        entropy = CalculateEntropy(section_data)
        value.append(entropy)
    else:
        for key in section_object:
            value.append(None)
        value.append(None)
    list_value += value

# selection 데이터 추출
def ExtractSection(file_path, list_value):
    pe = pefile.PE(file_path)

    for section_name in section_list:
        section_check = False
        section_save = None
        for section in pe.sections:
            if section.Name.decode().rstrip('\x00') == section_name:
                section_check = True
                section_save = section
        ExtractSectionToList(section_save, section_check, list_value)
