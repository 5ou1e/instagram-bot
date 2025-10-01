import os
import subprocess
import tokenize
from io import BytesIO
from pathlib import Path

import click


@click.group(help="Инструменты")
def tools():
    pass


@tools.command(name="cloc")
@click.argument(
    "directory",
    required=False,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
)
@click.option(
    "--count-comments",
    is_flag=True,
    default=False,
    help="Считать строки с комментариями",
)
@click.option(
    "--count-empty", is_flag=True, default=False, help="Считать пустые строки"
)
@click.option(
    "--count-words", is_flag=True, default=False, help="Также считать количество лексем"
)
def count_lines_of_code(directory, count_comments, count_empty, count_words):
    """
    Посчитать строки и (опционально) лексемы Python-кода в файлах.
    """

    path = Path(directory)
    total_lines = 0
    total_words = 0
    max_lines = 0
    max_file = ""

    files = [path] if path.is_file() else list(path.rglob("*.py"))

    for f in files:
        if not f.is_file() or not f.exists():
            continue

        local_count = 0
        local_words = 0
        try:
            try:
                content = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = f.read_text(encoding="cp1251")

            lines = content.splitlines()

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    if count_empty:
                        local_count += 1
                    continue
                # if stripped.startswith(("#", '"', "'")):
                #     if count_comments:
                #         local_count += 1
                #     continue
                local_count += 1

            if count_words:
                tokens = list(
                    tokenize.tokenize(BytesIO(content.encode("utf-8")).readline)
                )
                for t in tokens:
                    if t.type == tokenize.NAME:
                        local_words += 1
                    elif t.type in (tokenize.OP, tokenize.STRING, tokenize.NUMBER):
                        local_words += 1

            print(f"{f} - {local_count} строк", end="")
            if count_words:
                print(f", {local_words} лексем")
            else:
                print()

            total_lines += local_count
            total_words += local_words

            if local_count > max_lines:
                max_lines = local_count
                max_file = str(f)

        except Exception as e:
            print(f"Ошибка чтения файла {f}: {e}")

    print("=" * 40)
    print(f"Максимум строк в файле: {max_file} - {max_lines} строк")
    print(f"Всего строк (с учетом опций) - {total_lines}")
    if count_words:
        print(f"Всего лексем (слов) - {total_words}")


# ===== Команда генерации структуры проекта =====


class FolderStructureGenerator:
    def __init__(
        self,
        excluded_dirs: set[str] = None,
        excluded_files: set[str] = None,
    ):
        self.excluded_dirs = excluded_dirs or {
            "__pycache__",
            ".mypy_cache",
            ".git",
            ".venv",
            "venv",
            ".idea",
            ".pytest_cache",
            "migrations",
            "nginx",
            "tests",
            "__init__.py",
        }
        self.excluded_files = excluded_files or {".DS_Store", ".gitignore"}

    def generate(
        self, directory: str, prefix: str = "", only_dirs: bool = False
    ) -> list[str]:
        tree_lines = []

        try:
            entries = sorted(os.listdir(directory))
        except Exception as e:
            return [f"{prefix}Ошибка при чтении {directory}: {e}"]

        filtered = []
        for e in entries:
            if e in self.excluded_dirs or e in self.excluded_files:
                continue
            full_path = os.path.join(directory, e)
            if only_dirs and not os.path.isdir(full_path):
                continue
            filtered.append(e)

        for i, entry in enumerate(filtered):
            path = os.path.join(directory, entry)
            connector = "└── " if i == len(filtered) - 1 else "├── "
            tree_lines.append(prefix + connector + entry)

            if os.path.isdir(path):
                tree_lines.extend(
                    self.generate(
                        path,
                        prefix + ("    " if i == len(filtered) - 1 else "│   "),
                        only_dirs=only_dirs,
                    )
                )

        return tree_lines


@tools.command(
    name="show_tree",
    help="Показать структуру проекта (по умолчанию из текущей директории)",
)
@click.argument(
    "directory",
    required=False,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
)
@click.option(
    "--only-dirs", is_flag=True, default=False, help="Показывать только папки"
)
def show_tree(directory, only_dirs):
    """
    Выводит дерево проекта, исключая стандартные папки и файлы.
    """
    generator = FolderStructureGenerator()
    tree_output = generator.generate(directory, only_dirs=only_dirs)
    print(f"Структура директории {directory}")
    print("\n".join(tree_output))


@tools.command(name="lint", help="Запустить линтеры и автоформатирование.")
@click.argument("path", required=False, default="src/")
def lint(path):
    """Прогон линтеров и автоформатирование."""

    # Убираем возможные кавычки из начала и конца пути (если вдруг попали)
    path = path.strip("\"'")

    commands = [
        [
            "autoflake",
            "--remove-all-unused-imports",
            "--in-place",
            "--recursive",
            path,
        ],
        ["isort", path],
        ["black", path],
    ]

    for cmd in commands:
        click.echo(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            click.secho(f"Command failed: {' '.join(cmd)}", fg="red")
            exit(result.returncode)

    click.secho("✅ Всё чисто!", fg="green")
