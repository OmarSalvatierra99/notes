#!/usr/bin/env python3
"""
Obsidian Vault Organizer Script - Enhanced Version
Organizes files in an Obsidian vault based on file type and tags:
- PDFs → pdf/ folder
- Images → media/ folder
- Files with #developer tag → developer/ folder
- Files with #art tag → art/ folder
- Files with #ideas tag → brain/ folder
- Files with #auditoria tag → auditoria-gubernamental/ folder
- Files with #anki tag → anki/ folder
"""

import os
import sys
import shutil
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, Tuple, List, Optional

# Configuration
VAULT_PATH = Path(__file__).parent.parent.resolve()
LOG_DIR = VAULT_PATH / "scripts" / "logs"

# Folder mappings
FOLDERS = {
    'pdf': 'pdf',
    'media': 'media',
    'developer': 'developer',
    'art': 'art',
    'brain': 'brain',
    'auditoria': 'auditoria-gubernamental',
    'anki': 'anki',
    'projects': 'projects'
}

# Image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico'}

# Tag to folder mapping (order matters - first match wins)
TAG_FOLDER_MAP = [
    ('#developer', 'developer'),
    ('#art', 'art'),
    ('#ideas', 'brain'),
    ('#auditoria', 'auditoria'),
    ('#anki', 'anki'),
    ('#projects', 'projects')
]

# Folders to skip during organization
SKIP_FOLDERS = {'.obsidian', '.trash', '.git', 'scripts', 'templates'}


def setup_logging(silent: bool = False) -> logging.Logger:
    """Setup logging configuration"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = LOG_DIR / f'organization_{timestamp}.log'

    logger = logging.getLogger('organizer')
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers = []

    # File handler - always logs everything
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - respects silent mode and handles Unicode properly
    if not silent:
        # Force UTF-8 encoding for console output on Windows
        import io
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    logger.info(f"Log file: {log_file}")
    return logger


def create_folders(vault_path: Path, logger: logging.Logger) -> None:
    """Create necessary folders if they don't exist"""
    logger.info("Creating/verifying folder structure...")
    for folder in FOLDERS.values():
        folder_path = vault_path / folder
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Verified folder: {folder}/")
        except Exception as e:
            logger.error(f"Failed to create folder {folder}/: {e}")
            raise


def find_tags_in_file(file_path: Path, logger: logging.Logger) -> Set[str]:
    """Extract tags from a markdown file, including frontmatter tags"""
    tags = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check for YAML frontmatter tags
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Look for tags in array format: tags: [tag1, tag2]
            yaml_array_tags = re.findall(r'tags:\s*\[([^\]]+)\]', frontmatter)
            for tag_list in yaml_array_tags:
                for tag in tag_list.split(','):
                    tag = tag.strip().strip('"').strip("'")
                    if tag:
                        tags.add(f'#{tag}' if not tag.startswith('#') else tag)

            # Look for tags in simple format: tags: tag1, tag2
            yaml_simple_tags = re.findall(r'tags:\s*([^\[\n]+)', frontmatter)
            for tag_line in yaml_simple_tags:
                if '[' not in tag_line:  # Skip array format already handled
                    for tag in tag_line.split(','):
                        tag = tag.strip().strip('"').strip("'")
                        if tag:
                            tags.add(f'#{tag}' if not tag.startswith('#') else tag)

        # Find all inline tags in the format #tagname
        inline_tags = re.findall(r'#[a-zA-Z0-9_-]+', content)
        tags.update(inline_tags)

    except Exception as e:
        logger.warning(f"Could not read {file_path.name}: {e}")

    return tags


def move_file(source: Path, destination_folder: str, vault_path: Path, logger: logging.Logger) -> Tuple[bool, Optional[Path]]:
    """Move a file to the destination folder with duplicate handling"""
    dest_dir = vault_path / destination_folder
    filename = source.name
    destination = dest_dir / filename

    # Handle duplicate filenames
    if destination.exists():
        base = source.stem
        ext = source.suffix
        counter = 1
        while destination.exists():
            new_filename = f"{base}_{counter}{ext}"
            destination = dest_dir / new_filename
            counter += 1
        logger.warning(f"Duplicate found, renaming to: {destination.name}")

    try:
        shutil.move(str(source), str(destination))
        logger.debug(f"Moved: {source.name} → {destination_folder}/")
        return True, destination
    except PermissionError as e:
        logger.error(f"Permission denied moving {source.name}: {e}")
        return False, None
    except Exception as e:
        logger.error(f"Error moving {source.name}: {e}")
        return False, None


def should_skip_folder(folder_path: Path, vault_path: Path) -> bool:
    """Check if a folder should be skipped"""
    try:
        relative_path = folder_path.relative_to(vault_path)
        relative_str = str(relative_path)

        # Don't skip the root vault folder itself
        if relative_str == '.':
            return False

        # Skip hidden folders
        if any(part.startswith('.') for part in relative_path.parts):
            return True

        # Skip if it's one of our organized folders
        if relative_str in FOLDERS.values():
            return True

        # Skip if it's in the skip list
        for skip_folder in SKIP_FOLDERS:
            if relative_str == skip_folder or relative_str.startswith(skip_folder + os.sep):
                return True

        return False
    except ValueError:
        # Path is not relative to vault_path
        return True


def organize_vault(vault_path: Path, dry_run: bool = False, silent: bool = False) -> Dict[str, int]:
    """Organize files in the Obsidian vault"""
    logger = setup_logging(silent)

    if not vault_path.exists():
        logger.error(f"Vault path does not exist: {vault_path}")
        sys.exit(1)

    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Starting organization of: {vault_path}")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Create folders
    if not dry_run:
        try:
            create_folders(vault_path, logger)
        except Exception as e:
            logger.error(f"Failed to create folders: {e}")
            sys.exit(1)

    stats = {
        'pdf_moved': 0,
        'images_moved': 0,
        'tagged_moved': 0,
        'errors': 0,
        'skipped': 0
    }

    processed_files: List[Tuple[str, str]] = []

    # Walk through vault
    logger.info("Scanning vault...")

    try:
        for root, dirs, files in os.walk(vault_path):
            root_path = Path(root)

            # Skip folders we don't want to organize
            if should_skip_folder(root_path, vault_path):
                logger.debug(f"Skipping folder: {root_path.relative_to(vault_path)}")
                dirs[:] = []  # Don't recurse into skipped directories
                continue

            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    stats['skipped'] += 1
                    continue

                file_path = root_path / file
                file_ext = file_path.suffix.lower()

                try:
                    # Check if it's a PDF
                    if file_ext == '.pdf':
                        logger.info(f"📄 PDF: {file}")
                        if not dry_run:
                            success, _ = move_file(file_path, FOLDERS['pdf'], vault_path, logger)
                            if success:
                                stats['pdf_moved'] += 1
                                processed_files.append((file, FOLDERS['pdf']))
                            else:
                                stats['errors'] += 1
                        else:
                            logger.info(f"  → Would move to: {FOLDERS['pdf']}/")
                            stats['pdf_moved'] += 1

                    # Check if it's an image
                    elif file_ext in IMAGE_EXTENSIONS:
                        logger.info(f"🖼️  Image: {file}")
                        if not dry_run:
                            success, _ = move_file(file_path, FOLDERS['media'], vault_path, logger)
                            if success:
                                stats['images_moved'] += 1
                                processed_files.append((file, FOLDERS['media']))
                            else:
                                stats['errors'] += 1
                        else:
                            logger.info(f"  → Would move to: {FOLDERS['media']}/")
                            stats['images_moved'] += 1

                    # Check markdown files for tags
                    elif file_ext == '.md':
                        tags = find_tags_in_file(file_path, logger)

                        if tags:
                            # Check each tag mapping in priority order
                            for tag, folder in TAG_FOLDER_MAP:
                                if tag in tags:
                                    all_tags = ', '.join(sorted(tags))
                                    logger.info(f"🏷️  Tagged file: {file}")
                                    logger.debug(f"  Tags found: {all_tags}")
                                    logger.debug(f"  Matching tag: {tag}")

                                    if not dry_run:
                                        success, _ = move_file(file_path, FOLDERS[folder], vault_path, logger)
                                        if success:
                                            stats['tagged_moved'] += 1
                                            processed_files.append((file, FOLDERS[folder]))
                                        else:
                                            stats['errors'] += 1
                                    else:
                                        logger.info(f"  → Would move to: {FOLDERS[folder]}/")
                                        stats['tagged_moved'] += 1
                                    break  # Only move to first matching tag folder

                except Exception as e:
                    logger.error(f"Error processing {file}: {e}")
                    stats['errors'] += 1

    except Exception as e:
        logger.error(f"Fatal error during vault scan: {e}")
        sys.exit(1)

    # Print summary
    logger.info("=" * 60)
    logger.info("📊 ORGANIZATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📄 PDFs organized: {stats['pdf_moved']}")
    logger.info(f"🖼️  Images organized: {stats['images_moved']}")
    logger.info(f"🏷️  Tagged files organized: {stats['tagged_moved']}")
    logger.info(f"⏭️  Files skipped: {stats['skipped']}")
    logger.info(f"❌ Errors encountered: {stats['errors']}")
    logger.info("-" * 60)
    total = stats['pdf_moved'] + stats['images_moved'] + stats['tagged_moved']
    logger.info(f"✅ Total files organized: {total}")
    logger.info("=" * 60)

    if not dry_run and processed_files:
        logger.debug("Files moved:")
        for filename, folder in processed_files[:50]:
            logger.debug(f"  • {filename} → {folder}/")
        if len(processed_files) > 50:
            logger.debug(f"  ... and {len(processed_files) - 50} more files")

    return stats


def main():
    """Main entry point with CLI argument parsing"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Organize Obsidian vault files by type and tags',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without moving files'
    )
    parser.add_argument(
        '--silent',
        action='store_true',
        help='Silent mode - only log to file, no console output'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode with prompts (legacy behavior)'
    )

    args = parser.parse_args()

    if args.interactive:
        # Legacy interactive mode
        print("=" * 60)
        print("🗂️  OBSIDIAN VAULT ORGANIZER")
        print("=" * 60)
        print(f"\n📍 Vault path: {VAULT_PATH}")
        print("\n📋 Organization rules:")
        print("  • PDFs → pdf/")
        print("  • Images (jpg, png, gif, etc.) → media/")
        print("  • #developer → developer/")
        print("  • #art → art/")
        print("  • #ideas → brain/")
        print("  • #auditoria → auditoria-gubernamental/")
        print("  • #anki → anki/")

        response = input("\n🔍 Run in DRY RUN mode first? (recommended) [Y/n]: ")

        if response.lower() != 'n':
            print("\n🔍 DRY RUN MODE - No files will be moved\n")
            organize_vault(VAULT_PATH, dry_run=True, silent=False)

            response = input("\n✅ Proceed with actual organization? [y/N]: ")
            if response.lower() == 'y':
                organize_vault(VAULT_PATH, dry_run=False, silent=False)
                print("\n✅ Organization complete!")
            else:
                print("\n❌ Organization cancelled.")
        else:
            response = input("⚠️  Skip dry run and proceed? [y/N]: ")
            if response.lower() == 'y':
                organize_vault(VAULT_PATH, dry_run=False, silent=False)
                print("\n✅ Organization complete!")
            else:
                print("\n❌ Organization cancelled.")
    else:
        # Non-interactive mode (for Shell Commands plugin)
        try:
            stats = organize_vault(VAULT_PATH, dry_run=args.dry_run, silent=args.silent)

            # Exit code based on errors
            if stats['errors'] > 0:
                sys.exit(1)
            else:
                sys.exit(0)
        except Exception as e:
            print(f"Fatal error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
