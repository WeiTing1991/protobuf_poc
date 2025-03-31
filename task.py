import os
import platform
from glob import glob
import invoke

HERE = os.path.abspath(os.path.dirname(__file__))


def generate_path_to_compiler():
	if platform.system() == "Windows":
		return os.path.join(HERE, "bin", "win64", "protoc.exe")
	elif platform.system() == "Linux":
		return os.path.join(HERE, "bin", "linux64", "protoc")
	elif platform.system() == "Darwin":
		return os.path.join(HERE, "bin", "osx", "protoc")


@invoke.task(help={"idl_dir": "Directory containing the IDL files"})
def generate_classes(ctx, idl_dir: str, target_language: str = "python"):
	idl_dir = os.path.abspath(idl_dir)
	path_to_compiler = generate_path_to_compiler()
	for idl_file in glob(os.path.join(idl_dir, "*.proto")):
		cmd = f"{path_to_compiler} --{target_language} {idl_file}"
		print(cmd)
		print(f"compiling {idl_file}")
		ctx.run(f"{path_to_compiler} --{target_language} {idl_file}")
