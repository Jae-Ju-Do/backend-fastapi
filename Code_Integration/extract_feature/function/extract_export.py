import pefile

# export 데이터 추출
def ExtractExport(file_path, list_value):
    pe = pefile.PE(file_path)

    try:
        list_value.append(len(pe.DIRECTORY_ENTRY_EXPORT.symbols))
    except:
        list_value.append(0)
        pass