import os
import zipfile
import tarfile
import gzip
import shutil

def extract_gz_files(directory):
    """递归解压所有 .gz 文件（不包括 .tar.gz）"""
    extracted = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.gz') and not (file.endswith('.tar.gz') or file.endswith('.tgz')):
                gz_path = os.path.join(root, file)
                out_path = os.path.splitext(gz_path)[0]
                with gzip.open(gz_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                extracted.append(out_path)
                # 如果需要删除原 .gz 文件，取消下一行注释
                # os.remove(gz_path)
    return extracted

def extract_log(archive_path, extract_to=None):
    """
    Extract log archive (supports zip and tar.gz formats).
    Also auto-extract .gz files found after initial extraction.
    """
    if not extract_to:
        extract_to = os.path.splitext(os.path.abspath(archive_path))[0]

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    extracted_files = []

    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(extract_to)
            extracted_files = [os.path.join(extract_to, name) for name in zf.namelist()]
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
        with tarfile.open(archive_path, 'r:gz') as tf:
            tf.extractall(extract_to)
            extracted_files = [os.path.join(extract_to, name) for name in tf.getnames()]
    else:
        raise ValueError("Unsupported archive format. Only zip and tar.gz are supported.")

    # 递归解压 .gz 文件
    gz_extracted = extract_gz_files(extract_to)
    extracted_files.extend(gz_extracted)

    return extracted_files

if __name__ == "__main__":
    archive = "your_log.zip"  # or "your_log.tar.gz"
    output_dir = "logs"
    files = extract_log(archive, output_dir)
    print("Extracted files:")
    for f in files:
        print(f)