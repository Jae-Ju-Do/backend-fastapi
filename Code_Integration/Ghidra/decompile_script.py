# -*- coding: utf-8 -*-
import os
import io
import logging
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Decompile & Disassembly Script Started")

decomp = DecompInterface()
decomp.openProgram(currentProgram)

function_manager = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
functions = function_manager.getFunctions(True)

OUTPUT_DIR = r"./filedata/c_file"

base_name = currentProgram.getExecutablePath().split('/')[-1].split('.')[0]
c_output_file = os.path.join(OUTPUT_DIR, base_name + ".c")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
os.chmod(OUTPUT_DIR, 0o777)

if not os.path.exists(c_output_file):
    open(c_output_file, 'a').close()

os.chmod(c_output_file, 0o666)

with io.open(c_output_file, "w", encoding="utf-8") as f:
    for function in functions:
        decompiled = decomp.decompileFunction(function, 30, ConsoleTaskMonitor())
        if decompiled.decompileCompleted():
            c_code = decompiled.getDecompiledFunction().getC()
            f.write(u"\n/* Function: {} */\n".format(function.getName()))
            f.write(c_code)
        else:
            f.write(u"Failed to decompile function: {}\n".format(function.getName()))