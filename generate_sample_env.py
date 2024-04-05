import os
from dotenv import dotenv_values


def mask_key(key):
    return "*****"  # キーをマスクする場合の置き換え関数


def copy_and_mask_env(env_file_path, dest_path):
    # .envファイルの内容を読み取る
    env_values = dotenv_values(env_file_path)

    # キーをマスクする
    masked_env_values = {key: mask_key(value)
                         for key, value in env_values.items()}

    # sample.envファイルに書き込む
    with open(dest_path, 'w') as f:
        for key, value in masked_env_values.items():
            f.write(f"{key}={value}\n")


def find_and_copy_env(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == '.env':
                env_file_path = os.path.join(root, file)
                sample_env_file_path = os.path.join(root, 'sample.env')
                copy_and_mask_env(env_file_path, sample_env_file_path)


if __name__ == "__main__":
    # 現在のディレクトリを取得
    current_directory = os.getcwd()

    # 現在のディレクトリから再帰的に.envファイルをコピーしてキーをマスクする
    find_and_copy_env(current_directory)
