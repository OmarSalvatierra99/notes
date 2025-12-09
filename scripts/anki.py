#!/usr/bin/env python3
"""
Obsidian to Anki Exporter via AnkiConnect
Converts markdown files from the anki folder into Anki flashcards using AnkiConnect API
- Parses Front:/Back: template structure from markdown files
- Supports embedded images
- Directly syncs to Anki via AnkiConnect (no manual import needed)
"""

import os
import json
import re
import base64
import urllib.request
import hashlib
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = r"C:\Users\Usuario\Documents\Personal\notas"
ANKI_FOLDER = "anki"
MEDIA_FOLDER = "media"

# Anki deck name
DECK_NAME = "Obsidian Notes"

# AnkiConnect configuration
ANKI_CONNECT_URL = "http://localhost:8765"


def invoke_anki_connect(action, **params):
    """Send a request to AnkiConnect API"""
    request_json = json.dumps({
        'action': action,
        'version': 6,
        'params': params
    }).encode('utf-8')

    try:
        response = urllib.request.urlopen(
            urllib.request.Request(ANKI_CONNECT_URL, request_json)
        )
        response_data = json.load(response)

        if len(response_data) != 2:
            raise Exception('Response has an unexpected number of fields')
        if 'error' not in response_data:
            raise Exception('Response is missing required error field')
        if 'result' not in response_data:
            raise Exception('Response is missing required result field')
        if response_data['error'] is not None:
            raise Exception(response_data['error'])

        return response_data['result']
    except urllib.error.URLError as e:
        raise Exception(f'Failed to connect to AnkiConnect. Make sure Anki is running with AnkiConnect installed. Error: {e}')


def test_anki_connect():
    """Test if AnkiConnect is available"""
    try:
        version = invoke_anki_connect('version')
        print(f"✅ Connected to AnkiConnect (version {version})")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to AnkiConnect: {e}")
        print("\n📝 Make sure:")
        print("   1. Anki is running")
        print("   2. AnkiConnect plugin is installed")
        print("   3. AnkiConnect URL is: {ANKI_CONNECT_URL}")
        return False


def ensure_deck_exists(deck_name):
    """Create deck if it doesn't exist"""
    try:
        decks = invoke_anki_connect('deckNames')
        if deck_name not in decks:
            invoke_anki_connect('createDeck', deck=deck_name)
            print(f"📦 Created deck: {deck_name}")
        else:
            print(f"📦 Using existing deck: {deck_name}")
        return True
    except Exception as e:
        print(f"❌ Error with deck: {e}")
        return False


def store_media_file(file_path, filename):
    """Upload media file to Anki's media collection"""
    try:
        with open(file_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')

        invoke_anki_connect('storeMediaFile', filename=filename, data=data)
        return filename
    except Exception as e:
        print(f"  ⚠️  Warning: Could not upload media file {filename}: {e}")
        return None


def process_images(text, vault_path):
    """Find and upload images, replace references with Anki format"""
    images_found = []

    def replace_image(match):
        # Extract image path from either format
        if match.lastindex == 2:
            # Standard markdown: ![alt](path)
            image_path = match.group(2)
        else:
            # Obsidian wiki-style: ![[path]]
            image_path = match.group(1)

        # Handle both relative and absolute paths
        if not os.path.isabs(image_path):
            # Try media folder first
            full_path = os.path.join(vault_path, MEDIA_FOLDER, image_path)
            if not os.path.exists(full_path):
                # Try relative to vault root
                full_path = os.path.join(vault_path, image_path)
        else:
            full_path = image_path

        if os.path.exists(full_path):
            filename = os.path.basename(full_path)
            stored_filename = store_media_file(full_path, filename)
            if stored_filename:
                images_found.append(filename)
                return f'<img src="{stored_filename}">'

        print(f"  ⚠️  Warning: Image not found: {image_path}")
        return match.group(0)  # Keep original if not found

    # Pattern for Obsidian wiki-style images: ![[image.png]]
    wiki_image_pattern = r'!\[\[([^\]]+)\]\]'

    # Pattern for standard markdown images: ![alt](path)
    markdown_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    # Process wiki-style images first
    processed_text = re.sub(wiki_image_pattern, replace_image, text)

    # Then process standard markdown images
    processed_text = re.sub(markdown_image_pattern, replace_image, processed_text)

    return processed_text, images_found


def clean_markdown(text, vault_path=None):
    """Convert markdown formatting to HTML for Anki"""
    # Remove YAML frontmatter
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)

    # Process images first (before other conversions)
    images = []
    if vault_path:
        text, images = process_images(text, vault_path)

    # Convert markdown headers to bold
    text = re.sub(r'^#{1,6}\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # Convert **bold** to <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Convert *italic* to <i>italic</i> (but not if part of list marker)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', text)

    # Convert _italic_ to <i>italic</i>
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)

    # Convert `code` to <code>code</code>
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    # Convert bullet points to HTML lists
    lines = text.split('\n')
    in_list = False
    result_lines = []

    for line in lines:
        if re.match(r'^\s*[-*]\s+', line):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            item = re.sub(r'^\s*[-*]\s+', '', line)
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)

    if in_list:
        result_lines.append('</ul>')

    text = '\n'.join(result_lines)

    # Convert links [[Link]] to just Link
    text = re.sub(r'\[\[(.+?)\]\]', r'\1', text)

    # Convert [text](url) to <a href="url">text</a>
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # Remove tags
    text = re.sub(r'#[a-zA-Z0-9_-]+', '', text)

    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    # Convert newlines to <br> for Anki
    text = text.replace('\n', '<br>')

    return text, images


def extract_note_id(content, file_path):
    """Extract or generate a unique ID for the note"""
    # Try to extract ID from YAML frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # Look for id field in YAML
        id_match = re.search(r'^\s*id:\s*(.+)$', frontmatter, re.MULTILINE)
        if id_match:
            note_id = id_match.group(1).strip().strip('"').strip("'")
            return note_id

    # If no ID in frontmatter, generate one based on file path
    # This ensures the same file always gets the same ID
    relative_path = os.path.relpath(file_path)
    note_id = hashlib.md5(relative_path.encode('utf-8')).hexdigest()
    return note_id


def parse_card_from_template(file_path, vault_path):
    """Parse Front:/Back: template structure from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Error reading {file_path}: {e}")
        return None, None, [], None

    # Extract unique ID for this note
    note_id = extract_note_id(content, file_path)

    # Remove YAML frontmatter for processing
    content_no_yaml = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Try to parse Front:/Back: format
    front_match = re.search(r'^Front:\s*\n(.*?)(?=^Back:|\Z)', content_no_yaml, re.MULTILINE | re.DOTALL)
    back_match = re.search(r'^Back:\s*\n(.*?)$', content_no_yaml, re.MULTILINE | re.DOTALL)

    if front_match and back_match:
        front = front_match.group(1).strip()
        back = back_match.group(1).strip()

        # If either is empty, skip
        if not front or not back:
            return None, None, [], None

        # Clean and convert markdown to HTML
        front_html, front_images = clean_markdown(front, vault_path)
        back_html, back_images = clean_markdown(back, vault_path)

        all_images = front_images + back_images

        return front_html, back_html, all_images, note_id
    else:
        # No template found
        return None, None, [], None


def find_note_by_id(note_id):
    """Find an Anki note by our custom ID stored in tags"""
    # Search for notes with our ID tag
    query = f'"tag:obsidian-id-{note_id}"'
    try:
        note_ids = invoke_anki_connect('findNotes', query=query)
        if note_ids and len(note_ids) > 0:
            return note_ids[0]  # Return first match
        return None
    except Exception as e:
        print(f"  ⚠️  Warning: Could not search for note: {e}")
        return None


def update_note_in_anki(anki_note_id, front, back, tags=None):
    """Update an existing note in Anki"""
    if tags is None:
        tags = []

    note = {
        "id": anki_note_id,
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": tags
    }

    try:
        invoke_anki_connect('updateNoteFields', note=note)
        # Also update tags
        invoke_anki_connect('clearUnusedTags')
        return True
    except Exception as e:
        print(f"  ⚠️  Warning: Could not update note: {e}")
        return False


def add_note_to_anki(front, back, deck_name, note_id, tags=None):
    """Add a single note to Anki via AnkiConnect"""
    if tags is None:
        tags = []

    # Add our unique ID as a tag for tracking
    id_tag = f"obsidian-id-{note_id}"
    if id_tag not in tags:
        tags.append(id_tag)

    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": tags,
        "options": {
            "allowDuplicate": True  # We handle duplicates ourselves
        }
    }

    try:
        result = invoke_anki_connect('addNote', note=note)
        return result  # Returns note ID if successful
    except Exception as e:
        raise e


def sync_or_update_note(front, back, deck_name, note_id, tags=None):
    """Check if note exists and update it, or create new one"""
    if tags is None:
        tags = ['obsidian']

    # Add our unique ID as a tag
    id_tag = f"obsidian-id-{note_id}"
    if id_tag not in tags:
        tags.append(id_tag)

    # Check if note already exists
    existing_note_id = find_note_by_id(note_id)

    if existing_note_id:
        # Update existing note
        if update_note_in_anki(existing_note_id, front, back, tags):
            return 'updated', existing_note_id
        else:
            return 'error', None
    else:
        # Create new note
        try:
            new_note_id = add_note_to_anki(front, back, deck_name, note_id, tags)
            return 'created', new_note_id
        except Exception as e:
            return 'error', str(e)


def sync_to_anki(vault_path, deck_name):
    """Sync notes from anki folder to Anki via AnkiConnect"""
    anki_folder_path = os.path.join(vault_path, ANKI_FOLDER)

    if not os.path.exists(anki_folder_path):
        print(f"❌ Error: Anki folder does not exist: {anki_folder_path}")
        print(f"Please make sure the '{ANKI_FOLDER}' folder exists in your vault.")
        return

    print(f"📂 Scanning folder: {anki_folder_path}\n")

    cards_created = 0
    cards_updated = 0
    skipped = []
    errors = 0

    # Walk through anki folder
    for root, _, files in os.walk(anki_folder_path):
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                file_path = os.path.join(root, file)

                front, back, images, note_id = parse_card_from_template(file_path, vault_path)

                if front and back and note_id:
                    try:
                        print(f"📝 {file}")
                        print(f"   🔑 ID: {note_id[:16]}...")
                        if images:
                            print(f"   🖼️  Images: {', '.join(images)}")
                        print(f"   Front: {front[:50].replace('<br>', ' ')}...")
                        print(f"   Back: {back[:50].replace('<br>', ' ')}...")

                        status, result = sync_or_update_note(front, back, deck_name, note_id)

                        if status == 'created':
                            print(f"   ✅ Created new card (Anki ID: {result})")
                            cards_created += 1
                        elif status == 'updated':
                            print(f"   🔄 Updated existing card (Anki ID: {result})")
                            cards_updated += 1
                        elif status == 'error':
                            print(f"   ❌ Error: {result}")
                            errors += 1
                        print()
                    except Exception as e:
                        print(f"   ❌ Error: {e}\n")
                        errors += 1
                else:
                    skipped.append(file)
                    if not front and not back:
                        print(f"⏭️  Skipped (no Front:/Back: template found): {file}\n")
                    else:
                        print(f"⏭️  Skipped (could not generate ID): {file}\n")

    # Summary
    print("="*60)
    print("📊 SYNC SUMMARY")
    print("="*60)
    print(f"✅ Cards created: {cards_created}")
    print(f"🔄 Cards updated: {cards_updated}")
    print(f"⏭️  Files skipped: {len(skipped)}")
    print(f"❌ Errors: {errors}")
    print("="*60)

    total_synced = cards_created + cards_updated

    if total_synced > 0:
        print(f"\n✅ Successfully synced {total_synced} cards to Anki!")
        print(f"   • {cards_created} new cards created")
        print(f"   • {cards_updated} existing cards updated")
        print(f"📦 Deck: {deck_name}")
    else:
        print(f"\n⚠️  No cards were synced")

    return total_synced


if __name__ == "__main__":
    print("="*60)
    print("📇 OBSIDIAN TO ANKI SYNC via AnkiConnect")
    print("="*60)

    # Check if vault exists
    if not os.path.exists(VAULT_PATH):
        print(f"\n❌ ERROR: Vault path does not exist!")
        print(f"Path: {VAULT_PATH}")
        print("\nPlease update VAULT_PATH in the script.")
        exit(1)

    print(f"\n📍 Vault path: {VAULT_PATH}")
    print(f"📂 Anki folder: {ANKI_FOLDER}/")
    print(f"📦 Deck name: {DECK_NAME}")
    print(f"🔌 AnkiConnect URL: {ANKI_CONNECT_URL}")

    # Test AnkiConnect connection
    print("\n" + "-"*60)
    print("Testing AnkiConnect connection...")
    print("-"*60)

    if not test_anki_connect():
        print("\n❌ Cannot proceed without AnkiConnect connection.")
        print("\n📝 Setup instructions:")
        print("   1. Install AnkiConnect add-on in Anki")
        print("      Tools > Add-ons > Get Add-ons > Code: 2055492159")
        print("   2. Restart Anki")
        print("   3. Make sure Anki is running")
        exit(1)

    # Ensure deck exists
    print("\n" + "-"*60)
    if not ensure_deck_exists(DECK_NAME):
        exit(1)

    # Confirm sync
    print("\n" + "-"*60)
    print("📋 Template format expected in markdown files:")
    print("   Front:")
    print("   [your question or front content]")
    print("   Back:")
    print("   [your answer or back content]")
    print("-"*60)

    response = input("\n🚀 Start syncing notes to Anki? [Y/n]: ").strip()

    if response.lower() != 'n':
        print("\n" + "="*60)
        print("🚀 Starting sync...")
        print("="*60 + "\n")

        sync_to_anki(VAULT_PATH, DECK_NAME)

        print("\n" + "="*60)
        print("✅ Sync complete!")
        print("="*60)
        print("\n💡 Tip: Open Anki to review your new cards!")
    else:
        print("\n❌ Sync cancelled.")
        exit(0)