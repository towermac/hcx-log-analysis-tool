import os
import zipfile
import tarfile

def extract_log(archive_path, extract_to=None):
    """
    Extract log archive (supports zip and tar.gz formats).

    :param archive_path: Path to the archive file
    :param extract_to: Directory to extract to (default: same as archive name)
    :return: List of extracted file paths
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

    return extracted_files

if __name__ == "__main__":
    archive = "your_log.zip"  # or "your_log.tar.gz"
    output_dir = "logs"
    files = extract_log(archive, output_dir)
    print("Extracted files:")
    for f in files:
        print(f)