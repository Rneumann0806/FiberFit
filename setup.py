#!usr\local\bin\python3
import sys
from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\morrile2\AppData\Local\Continuum\anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\morrile2\AppData\Local\Continuum\anaconda3\tcl\tk8.6'

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "PIL", "pylab", "numpy", "pyparsing", "matplotlib", "scipy"],
    "includes": ["sip", "PyQt5", "PyQt5.QtWidgets", "matplotlib.backends.backend_qt5agg"],
    "excludes": ["tkinter", "scipy.spatial.cKDTree"],
    "include_files": [
        r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\python3.dll",
        r"src\fiberfit_model\EllipseDirectFit.py",
        "resources\images\clearButton.png",
        "resources\images\open.png",
        "resources\images\settings.png",
        "resources\images\start-icon.png",
        "resources\images\export.png",
        r"src\fiberfit_gui\settings_dialog.py",
        r"src\fiberfit_gui\fiberfit_GUI.py",
        r"src\fiberfit_model\helpers.py",
        r"src\fiberfit_control\support\img_model.py",
        r"src\fiberfit_gui\export_window.py"
    ]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="FiberFit",
      version="2.1",
      description="FiberFit",
      options={"build_exe": build_exe_options},
      executables=[Executable(r"src\fiberfit_control\fiberfit.py", base=base)])

# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\cilkrts20.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\ifdlg100.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libchkp.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libicaf.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libifcoremd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\libifcoremdd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libifcorert.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\libifcorertd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libifportmd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libimalloc.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libiomp5md.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libiompstubs5md.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libmmd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\libmmdd.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\libmpx.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\liboffload.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_avx.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_avx2.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_avx512.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\mkl_avx512_mic.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_core.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_def.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_intel_thread.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_mc.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_mc3.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_msg.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_rt.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_sequential.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_tbb_thread.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_avx.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_avx2.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_avx512.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\pkgs\mkl-2017.0.1-0\Library\bin\mkl_vml_avx512_mic.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_cmpt.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_def.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_mc.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_mc2.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\mkl_vml_mc3.dll",
# r"C:\Users\morrile2\AppData\Local\Continuum\anaconda3\Library\bin\svml_dispmd.dll",