import os
import subprocess

def compile_code(name, extension, build_dir):
    os.makedirs(build_dir, exist_ok=True)
    generated_file = f"generated/{name}.{extension}"

    if extension == 'vhdl':
        # Compile with GHDL
        subprocess.check_call(['ghdl', '-a', '-fsynopsys', '--workdir=' + build_dir, generated_file])
        subprocess.check_call(['ghdl', '-e', '--workdir=' + build_dir, name])
        # Optionally run: subprocess.check_call(['ghdl', '-r', '--workdir=' + build_dir, name])
    elif extension == 'v':
        # Compile with Icarus Verilog
        out_file = os.path.join(build_dir, f"{name}.out")
        subprocess.check_call(['iverilog', '-o', out_file, generated_file])
    else:
        raise ValueError("Unsupported language extension")
