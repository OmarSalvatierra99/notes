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
import shutil
import re
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = r"C:\Users\Usuario\Documents\Personal\notas"

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

# Tag to folder mapping
TAG_FOLDER_MAP = {
    '#developer': 'developer',
    '#art': 'art',
    '#ideas': 'brain',
    '#auditoria': 'auditoria',
    '#anki': 'anki',
    '#projects': 'projects'
}

# Folders to skip during organization
SKIP_FOLDERS = {'.obsidian', '.trash', '.git', 'scripts'}


def create_folders(vault_path):
    """Create necessary folders if they don't exist"""
    print("\n📁 Creating/verifying folder structure...")
    for folder in FOLDERS.values():
        folder_path = os.path.join(vault_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"  ✓ {folder}/")


def find_tags_in_file(file_path):
    """Extract tags from a markdown file, including frontmatter tags"""
    tags = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for YAML frontmatter tags
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                # Look for tags in frontmatter (tags: [tag1, tag2] or tags: tag1, tag2)
                yaml_tags = re.findall(r'tags:\s*\[([^\]]+)\]', frontmatter)
                if yaml_tags:
                    for tag_list in yaml_tags:
                        # Split by comma and clean up
                        for tag in tag_list.split(','):
                            tag = tag.strip().strip('"').strip("'")
                            if not tag.startswith('#'):
                                tag = '#' + tag
                            tags.add(tag)
                
                # Also look for inline tags in frontmatter
                yaml_inline_tags = re.findall(r'tags:\s*(.+?)(?:\n|$)', frontmatter)
                if yaml_inline_tags:
                    for tag_line in yaml_inline_tags:
                        if not '[' in tag_line:  # Skip if it's the array format we already handled
                            for tag in tag_line.split(','):
                                tag = tag.strip().strip('"').strip("'")
                                if not tag.startswith('#'):
                                    tag = '#' + tag
                                tags.add(tag)
            
            # Find all inline tags in the format #tagname
            inline_tags = re.findall(r'#[a-zA-Z0-9_-]+', content)
            tags.update(inline_tags)
            
    except Exception as e:
        print(f"  ⚠️  Warning: Could not read {file_path}: {e}")
    
    return tags


def update_internal_links(file_path, old_path, new_path, vault_path):
    """Update internal links in markdown files after moving a file"""
    try:
        # Calculate relative paths
        old_rel = os.path.relpath(old_path, vault_path)
        new_rel = os.path.relpath(new_path, vault_path)
        
        # Get filename without extension for wiki-style links
        old_name = os.path.splitext(os.path.basename(old_path))[0]
        
        # For now, we'll skip link updates as it's complex
        # This is a placeholder for future enhancement
        pass
    except Exception as e:
        print(f"  ⚠️  Warning: Could not update links: {e}")


def move_file(source, destination_folder, vault_path):
    """Move a file to the destination folder with duplicate handling"""
    dest_dir = os.path.join(vault_path, destination_folder)
    filename = os.path.basename(source)
    destination = os.path.join(dest_dir, filename)
    
    # Handle duplicate filenames
    if os.path.exists(destination):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(destination):
            new_filename = f"{base}_{counter}{ext}"
            destination = os.path.join(dest_dir, new_filename)
            counter += 1
        print(f"  ⚠️  Duplicate found, renaming to: {os.path.basename(destination)}")
    
    try:
        shutil.move(source, destination)
        return True, destination
    except PermissionError:
        print(f"  ❌ Permission denied: {source}")
        return False, None
    except Exception as e:
        print(f"  ❌ Error moving {source}: {e}")
        return False, None


def should_skip_folder(folder_path, vault_path):
    """Check if a folder should be skipped"""
    relative_path = os.path.relpath(folder_path, vault_path)
    
    # Don't skip the root vault folder itself
    if relative_path == '.':
        return False
    
    # Skip if it's a dot folder (hidden folders)
    if relative_path.startswith('.'):
        return True
    
    # Skip if it's one of our organized folders
    if relative_path in FOLDERS.values():
        return True
    
    # Skip if it's in the skip list
    for skip_folder in SKIP_FOLDERS:
        if relative_path.startswith(skip_folder):
            return True
    
    return False


def organize_vault(vault_path, dry_run=False, debug=False):
    """Organize files in the Obsidian vault"""
    if not os.path.exists(vault_path):
        print(f"❌ Error: Vault path does not exist: {vault_path}")
        return
    
    print(f"\n{'🔍 DRY RUN - ' if dry_run else '🚀 '}Starting organization of: {vault_path}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if debug:
        print("🐛 DEBUG MODE: ON")
    print()
    
    # Create folders
    if not dry_run:
        create_folders(vault_path)
    else:
        print("\n📁 Folders that would be created:")
        for folder in FOLDERS.values():
            print(f"  • {folder}/")
    
    stats = {
        'pdf_moved': 0,
        'images_moved': 0,
        'tagged_moved': 0,
        'errors': 0,
        'skipped': 0
    }
    
    processed_files = []
    
    # Walk through vault
    print("\n📂 Scanning vault...\n")
    for root, dirs, files in os.walk(vault_path):
        # Skip folders we don't want to organize
        if should_skip_folder(root, vault_path):
            if debug:
                print(f"⏭️  Skipping folder: {os.path.relpath(root, vault_path)}")
            continue
        
        if debug:
            print(f"📁 Scanning folder: {os.path.relpath(root, vault_path)}")
        
        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                stats['skipped'] += 1
                continue
            
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            moved = False
            
            # Check if it's a PDF
            if file_ext == '.pdf':
                print(f"📄 PDF: {file}")
                if not dry_run:
                    success, new_path = move_file(file_path, FOLDERS['pdf'], vault_path)
                    if success:
                        print(f"  ✓ Moved to: {FOLDERS['pdf']}/")
                        stats['pdf_moved'] += 1
                        processed_files.append((file, FOLDERS['pdf']))
                        moved = True
                    else:
                        stats['errors'] += 1
                else:
                    print(f"  → Would move to: {FOLDERS['pdf']}/")
                    stats['pdf_moved'] += 1
                    moved = True
            
            # Check if it's an image
            elif file_ext in IMAGE_EXTENSIONS:
                print(f"🖼️  Image: {file}")
                if not dry_run:
                    success, new_path = move_file(file_path, FOLDERS['media'], vault_path)
                    if success:
                        print(f"  ✓ Moved to: {FOLDERS['media']}/")
                        stats['images_moved'] += 1
                        processed_files.append((file, FOLDERS['media']))
                        moved = True
                    else:
                        stats['errors'] += 1
                else:
                    print(f"  → Would move to: {FOLDERS['media']}/")
                    stats['images_moved'] += 1
                    moved = True
            
            # Check markdown files for tags
            elif file_ext == '.md':
                tags = find_tags_in_file(file_path)
                
                if debug and tags:
                    print(f"📝 Markdown: {file} - Tags: {tags}")
                
                if tags:
                    # Check each tag mapping
                    for tag, folder in TAG_FOLDER_MAP.items():
                        if tag in tags:
                            all_tags = ', '.join(sorted(tags))
                            print(f"🏷️  Tagged file: {file}")
                            print(f"  📌 Tags found: {all_tags}")
                            print(f"  🎯 Matching tag: {tag}")
                            
                            if not dry_run:
                                success, new_path = move_file(file_path, FOLDERS[folder], vault_path)
                                if success:
                                    print(f"  ✓ Moved to: {FOLDERS[folder]}/")
                                    stats['tagged_moved'] += 1
                                    processed_files.append((file, FOLDERS[folder]))
                                    moved = True
                                else:
                                    stats['errors'] += 1
                            else:
                                print(f"  → Would move to: {FOLDERS[folder]}/")
                                stats['tagged_moved'] += 1
                                moved = True
                            break  # Only move to first matching tag folder
                    
                    if debug and not moved and tags:
                        print(f"⚠️  Markdown file with unmatched tags: {file} - Tags: {tags}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ORGANIZATION SUMMARY")
    print("="*60)
    print(f"📄 PDFs organized: {stats['pdf_moved']}")
    print(f"🖼️  Images organized: {stats['images_moved']}")
    print(f"🏷️  Tagged files organized: {stats['tagged_moved']}")
    print(f"⏭️  Files skipped: {stats['skipped']}")
    print(f"❌ Errors encountered: {stats['errors']}")
    print("-"*60)
    total = stats['pdf_moved'] + stats['images_moved'] + stats['tagged_moved']
    print(f"✅ Total files organized: {total}")
    print("="*60)
    
    if not dry_run and processed_files:
        print("\n📝 Files moved:")
        for filename, folder in processed_files[:20]:  # Show first 20
            print(f"  • {filename} → {folder}/")
        if len(processed_files) > 20:
            print(f"  ... and {len(processed_files) - 20} more files")
    
    return stats


def create_backup_log(vault_path):
    """Create a log file with organization details"""
    log_dir = os.path.join(vault_path, 'scripts')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'organization_log_{timestamp}.txt')
    
    return log_file


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("🗂️  OBSIDIAN VAULT ORGANIZER")
    print("="*60)
    
    # Check if vault path exists
    if not os.path.exists(VAULT_PATH):
        print(f"\n❌ ERROR: Vault path does not exist!")
        print(f"Path: {VAULT_PATH}")
        print("\nPlease update VAULT_PATH in the script.")
        sys.exit(1)
    
    # Display configuration
    print(f"\n📍 Vault path: {VAULT_PATH}")
    print("\n📋 Organization rules:")
    print("  • PDFs → pdf/")
    print("  • Images (jpg, png, gif, etc.) → media/")
    print("  • #developer → developer/")
    print("  • #art → art/")
    print("  • #ideas → brain/")
    print("  • #auditoria → auditoria-gubernamental/")
    print("  • #anki → anki/")
    
    # Ask for debug mode
    print("\n" + "-"*60)
    debug_response = input("🐛 Enable DEBUG mode? (shows detailed scanning info) [y/N]: ")
    debug_mode = debug_response.lower() == 'y'
    
    # Ask for dry run
    print("-"*60)
    response = input("\n🔍 Run in DRY RUN mode first? (recommended) [Y/n]: ")
    
    if response.lower() != 'n':
        print("\n" + "="*60)
        print("🔍 DRY RUN MODE - No files will be moved")
        print("="*60)
        organize_vault(VAULT_PATH, dry_run=True, debug=debug_mode)
        
        print("\n" + "="*60)
        response = input("\n✅ Proceed with actual organization? [y/N]: ")
        if response.lower() == 'y':
            print("\n⚠️  FINAL WARNING: Files will be moved!")
            final = input("Type 'yes' to confirm: ")
            if final.lower() == 'yes':
                organize_vault(VAULT_PATH, dry_run=False, debug=debug_mode)
                print("\n✅ Organization complete!")
            else:
                print("\n❌ Organization cancelled.")
        else:
            print("\n❌ Organization cancelled.")
    else:
        print("\n⚠️  WARNING: Skipping dry run!")
        response = input("Are you sure you want to proceed? [y/N]: ")
        if response.lower() == 'y':
            print("\n⚠️  FINAL WARNING: Files will be moved!")
            final = input("Type 'yes' to confirm: ")
            if final.lower() == 'yes':
                organize_vault(VAULT_PATH, dry_run=False, debug=debug_mode)
                print("\n✅ Organization complete!")
            else:
                print("\n❌ Organization cancelled.")
        else:
            print("\n❌ Organization cancelled.")
    
    print("\n" + "="*60)
    print("👋 Thank you for using Obsidian Vault Organizer!")
    print("="*60)