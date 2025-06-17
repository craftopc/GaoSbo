# -*- coding: utf-8 -*-
# @author
# @category Decompiling
# @keybinding
# @menupath
# @toolbar

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

output_file = "decompiled_functions.txt"


def decompile_functions():
    fm = currentProgram.getFunctionManager()
    decomp = DecompInterface()
    decomp.openProgram(currentProgram)
    monitor = ConsoleTaskMonitor()

    with open(output_file, "w") as outf:
        for func in fm.getFunctions(True):
            try:
                res = decomp.decompileFunction(func, 60, monitor)
                if res.decompileCompleted():
                    outf.write(
                        "Function: %s @ %s\n" % (func.getName(), func.getEntryPoint())
                    )
                    outf.write(res.getDecompiledFunction().getC())
                    outf.write("\n" + "=" * 80 + "\n")
                else:
                    outf.write("Failed to decompile %s\n" % func.getName())
            except Exception as e:
                outf.write("Exception in %s: %s\n" % (func.getName(), str(e)))


if __name__ == "__main__":
    decompile_functions()
