import os
import subprocess
from datetime import datetime  # Импортируем для работы с датами.
from typing import List, Tuple
import argparse
from graphviz import Digraph


def get_commits(repo_path: str) -> List[Tuple[str, str, str]]:
    # Получает список коммитов из указанного репозитория Git.
    git_command = [
        "git",
        "-C",
        repo_path,
        "log",
        "--pretty=format:%H %ct %an %s",  # Формат вывода с хэшем, временной меткой, автором и сообщением
    ]

    result = subprocess.run(git_command, stdout=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise Exception(f"Ошибка при выполнении команды git: {result.stderr}")

    commits = result.stdout.splitlines()
    commit_data = []

    for c in commits:
        parts = c.split(maxsplit=3)  # Ограничиваем количество разделений на 4
        if len(parts) < 4:
            continue  # Пропускаем если недостаточно частей

        commit_hash = parts[0]
        timestamp_str = parts[1]  # Временная метка как строка
        author = parts[2]
        message = parts[3]

        try:
            timestamp = int(timestamp_str)  # Пробуем преобразовать строку в int
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            commit_data.append((commit_hash, date_str, author, message))
        except ValueError:
            print(f"Пропущен коммит из-за неправильной временной метки: {timestamp_str}")
            continue  # Пропускаем этот коммит, если произошла ошибка

    return commit_data[::-1]  # Перевернуть, чтобы получить хронологический порядок


def build_dependency_graph(commits: List[Tuple[str, str, str, str]]) -> Digraph:
    #Создаёт граф зависимостей коммитов с использованием Graphviz.
    dot = Digraph(comment="Зависимости коммитов Git")

    for i, (commit, date, author, message) in enumerate(commits):
        dot.node(str(i), f"Коммит: {commit}\nАвтор: {author}\nДата: {date}\nСообщение: {message}")
        #print(f"Коммит: {commit}\nАвтор: {author}\nДата: {date}\nСообщение: {message}")
        if i > 0:
            dot.edge(str(i - 1), str(i))  # Соединить коммиты в хронологическом порядке

    return dot


def save_graph(graph: Digraph, output_file: str) -> None:
    # Сохраняет граф в файл PNG и Удаляем временный файл
    png_file = f"{output_file}.png"
    graph.attr(fontname='Arial', fontsize='12')  # Установка шрифта для поддержки русских символов
    graph.render(output_file, format="png")
    print(f"Успех! Граф сохранён в {png_file}.")

    # Удаляем временный файл без расширения, если он существует
    try:
        os.remove(output_file)
        print(f"Временный файл '{output_file}' удалён.")
    except Exception as e:
        print(f"Ошибка при удалении временного файла '{output_file}': {e}")


def main():
    parser = argparse.ArgumentParser(description="Построение графа зависимостей коммитов.")
    parser.add_argument("--dot", required=True, help="Путь к программе для визуализации графов (Graphviz dot).")
    parser.add_argument("--repo", required=True, help="Путь к анализируемому репозиторию.")
    parser.add_argument("--output", required=True, help="Название выходного файла с изображением графа зависимостей (без формата).")

    args = parser.parse_args()

    # Установка пути к Graphviz
    os.environ["PATH"] = args.dot + os.pathsep + os.environ["PATH"]

    if not os.path.exists(args.repo):
        print(f"Ошибка: Путь к репозиторию '{args.repo}' не существует.")
        return

    commits = get_commits(args.repo)
    if not commits:
        print("Не найдено ни одного коммита.")
        return

    graph = build_dependency_graph(commits)
    save_graph(graph, args.output)


if __name__ == "__main__":
    # Основная функция для обработки аргументов командной строки и запуска программы.
    main()