# -*- coding: utf-8 -*-
import os
import io
import logging
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Decompile & Disassembly Script Started")

# --- 환경 변수에서 C파일 저장 경로 읽기 ---
c_output_file = os.environ.get('C_OUTPUT_PATH')

if not c_output_file:
    logger.error("환경 변수 'C_OUTPUT_PATH'가 설정되지 않았습니다. 스크립트를 종료합니다.")
    exit(1) # 오류와 함께 종료

# 출력 디렉토리 생성
output_dir = os.path.dirname(c_output_file)
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logger.error("출력 디렉토리 생성 실패: {} - {}".format(output_dir, e))
        exit(1)

decomp = DecompInterface()
decomp.openProgram(currentProgram)

function_manager = currentProgram.getFunctionManager()
functions = function_manager.getFunctions(True)

# 불필요한 chmod 및 파일 생성 로직 제거
logger.info("C파일을 저장할 경로: {}".format(c_output_file))

with io.open(c_output_file, "w", encoding="utf-8") as f:
    for function in functions:
        try:
            decompiled = decomp.decompileFunction(function, 30, ConsoleTaskMonitor())
            if decompiled.decompileCompleted():
                c_code = decompiled.getDecompiledFunction().getC()
                f.write(u"\n/* Function: {} */\n".format(function.getName()))
                f.write(c_code)
            else:
                f.write(u"\n/* Failed to decompile function: {} */\n".format(function.getName()))
        except Exception as e:
             f.write(u"\n/* Exception during decompile function: {} - {} */\n".format(function.getName(), e))

logger.info("디컴파일 완료: {}".format(c_output_file))