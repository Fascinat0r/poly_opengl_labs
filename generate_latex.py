import os
import re
from pathlib import Path

from pathspec import PathSpec

# Настройки
allowed_extensions = {".py", ".sh", ".md", ".frag", ".vert"}  # Допустимые расширения файлов
ignore_folders = {"venv", "__pycache__", "dist"}  # Папки, которые нужно игнорировать

# Папка для сохранения .tex файлов
output_dir = Path("tex")
output_dir.mkdir(exist_ok=True)


# Функция для загрузки .gitignore и создания спецификации
def load_gitignore(base_folder):
    gitignore_path = os.path.join(base_folder, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            return PathSpec.from_lines("gitwildmatch", f)
    return None


# Проверка игнорирования файла по .gitignore
def is_gitignored(file_path, gitignore_spec):
    return gitignore_spec.match_file(file_path) if gitignore_spec else False


# Проверка, допустимо ли расширение файла
def is_allowed_file(file_name):
    _, ext = os.path.splitext(file_name)
    return ext in allowed_extensions


# Экранирование символов для LaTeX
def escape_latex(text):
    return text.replace("\\", "\\textbackslash{}").replace("_", "\\_")


# Создание XeLaTeX файла
def create_latex_file(folder, output_file, gitignore_spec):
    with open(output_file, "w", encoding="utf-8") as latex_file:
        # Заголовок LaTeX
        latex_file.write("\\documentclass{article}\n")
        latex_file.write("\\usepackage{listings}\n")
        latex_file.write("\\usepackage{xcolor}\n")
        latex_file.write("\\usepackage{polyglossia}\n")
        latex_file.write("\\setdefaultlanguage{russian}\n")
        latex_file.write("\\setotherlanguage{english}\n")
        latex_file.write("\\usepackage{standalone}\n")
        latex_file.write("\\setmainfont{Times New Roman}\n")
        latex_file.write("\\newfontfamily\\cyrillicfont{Times New Roman}\n")
        latex_file.write("\\newfontfamily\\cyrillicfonttt{Courier New}\n")
        latex_file.write("\\lstset{\n")
        latex_file.write("    language=Python,\n")
        latex_file.write("    basicstyle=\\ttfamily,\n")
        latex_file.write("    keywordstyle=\\color{blue},\n")
        latex_file.write("    stringstyle=\\color{green},\n")
        latex_file.write("    commentstyle=\\color{gray},\n")
        latex_file.write("    showstringspaces=false\n")
        latex_file.write("}\n")
        latex_file.write("\\begin{document}\n")
        latex_file.write(f"\\section*{{Листинг {escape_latex(folder.name)}}}\n")

        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, folder)

                # Пропускаем файлы по .gitignore и недопустимые расширения
                if is_gitignored(relative_file_path, gitignore_spec):
                    continue
                if not is_allowed_file(file):
                    continue

                # Добавляем листинг файла
                latex_file.write(f"\\subsection*{{{escape_latex(relative_file_path)}}}\n")
                latex_file.write("\\begin{lstlisting}\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    latex_file.write(content)
                except Exception as e:
                    latex_file.write(f"Error reading file: {e}")
                latex_file.write("\n\\end{lstlisting}\n")

        # Завершение LaTeX файла
        latex_file.write("\\end{document}\n")
    print(f"Файл создан: {output_file}")


def remove_comments(content):
    """
    Удаляет комментарии из кода, включая строки, начинающиеся с #.
    """
    # Удаление комментариев в строках
    pattern = r"(?<!\\)#.*"
    return re.sub(pattern, "", content)


# Главная функция
def main(folders):
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.is_dir():
            print(f"Пропущено: {folder} (не является директорией)")
            continue

        gitignore_spec = load_gitignore(folder_path)

        # Имя выходного LaTeX файла
        output_file = output_dir / f"{folder_path.name}.tex"

        # Создаем LaTeX файл
        create_latex_file(folder_path, output_file, gitignore_spec)


if __name__ == "__main__":
    # Пример использования: список папок
    input_folders = ["lab1", "lab2", "lab3", "lab_kr"]  # Замените на реальные пути
    main(input_folders)
