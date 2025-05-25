"""zorg/management/commands/echo.py"""

from pathlib import Path

COMMAND_DIR_ROOT = Path(__file__).resolve().parent


def echo(context, echo_type, *args):
    """
    Output styled messages to stdout using context's formatting utilities.

    Formats messages based on the specified echo type and writes them to
    context.stdout. Supports multiple style types for different message
    categories (errors, warnings, etc.).

    Parameters:
        context (object): Context object with:
            - stdout: Output stream
            - style: Style object with formatting methods (ERROR, SUCCESS, etc.)
        echo_type (str): Message style type. Valid values:
            - Error: ['e', 'error', 'err']
            - Success: ['s', 'success', 'succ']
            - Warning: ['w', 'warning', 'warn']
            - Notice: ['n', 'notice', 'notif', 'notify']
            - Plain: ['p', 'plain', 'white', 't', 'text', 'none', '', None]
        *args: Content to output, passed directly to style formatters

    Examples:
        >>> echo(context, 'error', 'Critical failure!')
        >>> echo(context, 'succ', 'Operation completed')
        >>> echo(context, None, 'Generic message')

    Notes:
        - Unrecognized echo types will default to plain text
        - Actual styling depends on context.style implementations
    """
    if echo_type in ["e", "error", "err"]:
        context.stdout.write(context.style.ERROR(*args))
    elif echo_type in ["s", "success", "succ"]:
        context.stdout.write(context.style.SUCCESS(*args))
    elif echo_type in ["w", "warning", "warn"]:
        context.stdout.write(context.style.WARNING(*args))
    elif echo_type in ["n", "notice", "notif", "notify"]:
        context.stdout.write(context.style.NOTICE(*args))
    elif echo_type in ["p", "plain", "white", "t", "text", "none", "", None]:
        context.stdout.write(*args)
    else:
        context.stdout.write(*args)


def copy_files(sources, dest_dir):
    """
    Copy files, directories (recursively), and/or glob patterns to a destination directory while preserving directory structures.

    Features
        Recursive Directory Copy:
            Directories are copied entirely, including nested subdirectories and files.
        Glob Patterns:
            Supports ** for recursive globbing (e.g., **/*.txt for all text files in subdirectories).
        Preserved Structure:
            Files retain their relative paths from the source directory or glob parent.
        Edge Cases
            Existing Files:
                Overwrites files in the destination without warning.
            Empty Directories:
                Not copied (only files are copied).
            Invalid Sources:
                Non-existent files/globs are silently skipped.

    Args:
        sources (str, Path, list, tuple): Source(s) to copy. Can be:
            - A single file path
            - A directory path (copied recursively)
            - A glob pattern (e.g., '**/*.txt' for recursive matching)
            - A list/tuple of mixed files/dirs/globs
        dest_dir (str, Path): Destination directory (must exist)

    Raises:
        ValueError: If destination directory does not exist

    Examples:
        Copy single file

            copy_files('file.txt', 'backup')

        Copy a Directory Recursively

            copy_files("source_dir", "dest_dir")

            Source Structure:

            source_dir/
            ├── notes.txt
            └── images/
                └── photo.jpg
            Destination Structure:

            dest_dir/
            ├── notes.txt
            └── images/
                └── photo.jpg

        Copy Files via Glob Pattern

            copy_files("data/**/*.csv", "data_backup")

            Files Matched:
                data/sales/2023.csv
                data/inventory.csv

            Result:

            data_backup/
            ├── sales/
            │   └── 2023.csv
            └── inventory.csv

        Mix Files, Directories, and Globs

            copy_files(["config.yaml", "docs", "src/**/*.md"], "archive")

            Result:

                config.yaml is copied to archive/config.yaml.
                The entire docs directory structure is replicated under archive/docs.
                All .md files under src are copied to archive, preserving their paths.

    Notes:
        - Destination directory must exist but subdirectories will be created as needed
        - Overwrites existing files with same names in destination
        - Preserves file content but not metadata (permissions/timestamps)
        - Empty directories are not copied
        - Invalid/non-existent sources are silently skipped
        - Use '**' in glob patterns for recursive file matching
    """
    dest_path = Path(dest_dir)

    # Validate destination directory exists
    if not dest_path.is_dir():
        raise ValueError(f"Destination directory '{dest_dir}' does not exist or is invalid.")

    # Normalize input to handle single/multiple sources
    if isinstance(sources, (str, Path)):
        sources_list = [sources]
    else:
        sources_list = sources

    for source in sources_list:
        source_path = Path(source)

        # Case 1: Source is a file
        if source_path.is_file():
            dest_file = dest_path / source_path.name
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            dest_file.write_bytes(source_path.read_bytes())

        # Case 2: Source is a directory (copy recursively)
        elif source_path.is_dir():
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    # Preserve relative path to source directory
                    relative = file_path.relative_to(source_path)
                    dest_file = dest_path / relative
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    dest_file.write_bytes(file_path.read_bytes())

        # Case 3: Treat as a glob pattern (copy matched files recursively)
        else:
            parent_dir = source_path.parent
            pattern = source_path.name
            for file_path in parent_dir.glob(pattern):
                if file_path.is_file():
                    # Preserve relative path to glob's parent directory
                    relative = file_path.relative_to(parent_dir)
                    dest_file = dest_path / relative
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    dest_file.write_bytes(file_path.read_bytes())
