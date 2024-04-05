import os
import subprocess


# def find_git_repo_path(current_path):
#     while True:
#         git_dir = os.path.join(current_path, '.git')
#         if os.path.exists(git_dir) and os.path.isdir(git_dir):
#             return current_path
#         # 親ディレクトリに移動
#         current_path = os.path.dirname(current_path)
#         if current_path == os.path.dirname(current_path):
#             break  # ルートディレクトリに達した場合は終了

#     return None  # Gitリポジトリが見つからなかった場合


def generate_git_tree(repo_path, output_file, max_depth=3):
    git_ls_tree = subprocess.Popen(
        ["git", "ls-tree", "--name-only", "-r", "HEAD"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    git_ls_tree_out, _ = git_ls_tree.communicate()

    tree_structure = {}  # フォルダ構造を表す辞書

    for line in git_ls_tree_out.splitlines():
        path_parts = line.split('/')
        current_dict = tree_structure

        for part in path_parts:
            current_dict = current_dict.setdefault(part, {})

    with open(output_file, 'w', encoding="utf-8") as f:
        def print_tree_structure(tree, indent="", current_path="", depth=0):
            sorted_tree = sorted(tree.items())
            for i, (key, value) in enumerate(sorted_tree):
                full_path = os.path.join(current_path, key)
                is_last = i == len(sorted_tree) - 1
                f.write(f"{indent}{'└─' if is_last else '├─'}{key}\n")
                if depth < max_depth and isinstance(value, dict):
                    print_tree_structure(
                        value, indent + ("    " if is_last else "│   "), full_path, depth + 1)

        print_tree_structure(tree_structure, "", repo_path)


if __name__ == "__main__":
    current_path = os.getcwd()  # 現在のディレクトリを取得
    # repo_path = find_git_repo_path(current_path)
    search_path = current_path

    # なんかgitリポジトリなくてもいけるっぽい？
    # if repo_path:
    output_file = "tree.txt"  # 出力ファイルの名前を指定
    generate_git_tree(search_path, output_file, max_depth=float('inf'))
    print(f"Gitリポジトリのツリーを {output_file} に出力しました。")
    # else:
    #     print("Gitリポジトリが見つかりませんでした。")
