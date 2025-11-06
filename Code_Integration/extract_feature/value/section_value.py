# 추출할 섹션 리스트 정보
section_list = [
    ".text",       # 프로그램 실행 코드 (기계어, import address table 정보 포함)
    ".data",       # 초기화된 데이터 (전역 변수 및 static 변수, 읽기/쓰기 가능)
    ".rdata",      # 읽기 전용 데이터 (문자열, 상수 등)
    ".bss",        # 초기화되지 않은 전역 변수 및 static 변수를 위한 섹션
    ".rsrc",       # 리소스 관련 데이터 (아이콘, 커서, UI 리소스 등)
    ".idata",      # Import된 DLL 및 API와 관련된 데이터.
    ".edata",      # Export된 API와 관련된 데이터
    ".reloc",      # 재배치 정보 (메모리 주소 변경 시 사용하는 정보)
    ".debug",      # 디버그 정보 (디버깅에 필요한 심볼, 소스 파일 정보 등)
    ".pdata",      # 예외 처리 및 함수의 unwind 데이터
    ".tls",        # 스레드 지역 저장소 데이터 (Thread-Local Storage)
    ".manifest",   # 응용 프로그램 매니페스트 데이터 (OS와의 호환성 정보 등)
    ".crt",        # C 런타임 초기화와 관련된 데이터
    ".xdata",      # 추가적인 예외 처리 및 디버깅 정보
    ".init",       # 프로그램 초기화 루틴 (프로그램 시작 전 실행되는 코드)
    ".fini",       # 프로그램 종료 루틴 (프로그램 종료 시 실행되는 코드)
    ".plt",        # Procedure Linkage Table (동적 링킹을 위한 코드)
    ".got",        # Global Offset Table (전역 데이터 주소 관리)
    ".eh_frame",   # 예외 처리와 관련된 프레임 정보
    ".exidx"       # ARM 예외 처리 테이블 (ARM 플랫폼에서 사용)
]

# 섹션에서 추출할 데이터 리스트 정보
section_object = [
    'Misc', 
    'Misc_PhysicalAddress', 
    'Misc_VirtualSize', 
    'VirtualAddress', 
    'SizeOfRawData', 
    'PointerToRawData', 
    'PointerToRelocations', 
    'PointerToLinenumbers', 
    'NumberOfRelocations', 
    'NumberOfLinenumbers', 
    'Characteristics'
]