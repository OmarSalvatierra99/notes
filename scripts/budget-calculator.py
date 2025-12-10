#!/usr/bin/env python3
"""
Budget Calculator for Obsidian Budget.md
Automatically calculates and updates totals in budget sections.
"""

import re
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(__file__).parent.parent.resolve()
BUDGET_FILE = VAULT_PATH / "Budget.md"


def extract_amount(line):
    """Extract numeric amount from a line like '- Item: $1,234.56 MXM'"""
    # Match patterns like: $1,234.56 or $1234.56 or $1,234 or $1234
    pattern = r'\$\s*([0-9,]+\.?[0-9]*)'
    match = re.search(pattern, line)
    if match:
        # Remove commas and convert to float
        amount_str = match.group(1).replace(',', '')
        try:
            return float(amount_str)
        except ValueError:
            return 0.0
    return 0.0


def format_amount(amount):
    """Format amount as $X,XXX.XX"""
    return f"${amount:,.2f}"


def calculate_budget_totals(content):
    """
    Parse Budget.md content and calculate totals for each section.
    Returns updated content with corrected totals.
    """
    lines = content.split('\n')
    result_lines = []

    current_section = None
    section_total = 0.0
    section_items = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect section headers (## Header)
        if line.startswith('## '):
            # If we were in a section, we've moved to a new one
            if current_section is not None:
                # Add accumulated items
                result_lines.extend(section_items)
                # Add blank line before total
                if section_items and not section_items[-1].strip():
                    pass  # Already has blank line
                else:
                    result_lines.append('')
                # Add calculated total
                result_lines.append(f"- **Total: {format_amount(section_total)} MXM**")
                result_lines.append('')

            # Start new section
            current_section = line.strip()
            section_total = 0.0
            section_items = []
            result_lines.append(line)

        # Detect bullet points with amounts
        elif line.strip().startswith('- ') and not line.strip().startswith('- **Total:'):
            # This is an item line
            amount = extract_amount(line)
            section_total += amount
            section_items.append(line)

        # Detect existing total lines (skip them, we'll regenerate)
        elif line.strip().startswith('- **Total:'):
            # Skip this line, we'll add our own calculated total
            pass

        # Blank lines or other content
        else:
            if current_section is not None:
                # We're inside a section, accumulate
                section_items.append(line)
            else:
                # We're before any section
                result_lines.append(line)

        i += 1

    # Handle last section if exists
    if current_section is not None and section_items:
        result_lines.extend(section_items)
        # Add blank line before total
        if section_items and not section_items[-1].strip():
            pass  # Already has blank line
        else:
            result_lines.append('')
        # Add calculated total
        result_lines.append(f"- **Total: {format_amount(section_total)} MXM**")
        result_lines.append('')

    return '\n'.join(result_lines)


def main():
    """Main entry point"""
    # Force UTF-8 encoding for console output on Windows
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("💰 BUDGET CALCULATOR")
    print("=" * 60)

    if not BUDGET_FILE.exists():
        print(f"\n❌ Error: Budget.md not found at: {BUDGET_FILE}")
        return 1

    print(f"\n📄 Reading: {BUDGET_FILE.name}")

    # Read current content
    try:
        with open(BUDGET_FILE, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 1

    # Calculate new totals
    updated_content = calculate_budget_totals(original_content)

    # Check if anything changed
    if original_content == updated_content:
        print("✅ Totals are already correct - no changes needed")
        return 0

    # Write updated content
    try:
        with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Budget totals updated successfully!")
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return 1

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    # Show what changed
    original_lines = original_content.split('\n')
    updated_lines = updated_content.split('\n')

    for i, (orig, upd) in enumerate(zip(original_lines, updated_lines)):
        if orig != upd and '**Total:' in upd:
            print(f"Updated: {upd.strip()}")

    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
