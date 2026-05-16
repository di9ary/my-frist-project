import os
from collections import defaultdict


def list_files(path="."):
    print(f"\n[{os.path.abspath(path)}]\n")
    try:
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        print("Error: Permission denied.")
        return

    for entry in entries:
        if entry.is_dir():
            print(f"  [DIR]  {entry.name}")
        else:
            size_kb = entry.stat().st_size / 1024
            print(f"  {size_kb:8.2f} KB  {entry.name}")

    print()


def count_by_type(path="."):
    counts = defaultdict(int)
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                ext = os.path.splitext(entry.name)[1].lower() or "(no extension)"
                counts[ext] += 1
    except PermissionError:
        print("Error: Permission denied.")
        return

    if not counts:
        print("\nNo files found.\n")
        return

    print("\nFile type counts:\n")
    for ext, count in sorted(counts.items()):
        print(f"  {ext:<20} {count}")
    print()


def search_files(keyword, path="."):
    keyword = keyword.lower()
    results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if keyword in name.lower():
                full_path = os.path.join(root, name)
                size_kb = os.path.getsize(full_path) / 1024
                results.append((full_path, size_kb))

    if not results:
        print(f'\nNo files matching "{keyword}" found.\n')
        return

    print(f'\nSearch results for "{keyword}":\n')
    for full_path, size_kb in results:
        print(f"  {size_kb:8.2f} KB  {full_path}")
    print()


def main():
    target_path = "."
    while True:
        print("=" * 40)
        print("       Python File Manager")
        print("=" * 40)
        print(f"  Current path: {os.path.abspath(target_path)}")
        print()
        print("  1. List files and folders")
        print("  2. Count files by type")
        print("  3. Search by filename")
        print("  4. Change directory")
        print("  0. Exit")
        print()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_files(target_path)
        elif choice == "2":
            count_by_type(target_path)
        elif choice == "3":
            keyword = input("Enter search keyword: ").strip()
            if keyword:
                search_files(keyword, target_path)
            else:
                print("Keyword cannot be empty.\n")
        elif choice == "4":
            new_path = input("Enter new path: ").strip()
            if os.path.isdir(new_path):
                target_path = new_path
            else:
                print("Invalid path.\n")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.\n")


if __name__ == "__main__":
    main()
