import os
import zipfile

def export_to_pdsprj(name, generated_file, export_dir, build_dir):
    os.makedirs(export_dir, exist_ok=True)
    zip_path = f"{export_dir}/{name}.zip"

    with zipfile.ZipFile(zip_path, 'w') as zip_f:
        # Add generated file
        zip_f.write(generated_file, arcname=os.path.basename(generated_file))

        # Add build files
        for file in os.listdir(build_dir):
            zip_f.write(os.path.join(build_dir, file), arcname=file)

    # Rename to .pdsprj
    pdsprj_path = f"{export_dir}/{name}.pdsprj"
    os.rename(zip_path, pdsprj_path)
