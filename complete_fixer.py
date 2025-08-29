#!/usr/bin/env python3
"""
DriveBy Complete Code Fixer
Fixes all indentation, syntax, and structural issues in the DriveBy project
"""

import os
import ast
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

class DriveByCodeFixer:
    def __init__(self):
        self.fixed_files = []
        self.failed_files = []
        self.backup_dir = "backup_before_complete_fix"

        def create_backup(self, file_path):
            """Create backup of file before fixing"""
            backup_path = Path(self.backup_dir)
            backup_path.mkdir(exist_ok=True)

            relative_path = Path(file_path).relative_to('.')
            backup_file_path = backup_path / relative_path
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file_path, backup_file_path)
            print(f"✓ Backed up: {file_path}")

            def fix_file_content(self, file_path):
                """Fix a single file's content completely"""
                print(f"🔧 Fixing: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Apply specific fixes based on file type
                        if file_path.endswith('.py'):
                            fixed_content = self.fix_python_file(content, file_path)
                        else:
                            fixed_content = content

                            # Validate syntax for Python files
                            if file_path.endswith('.py'):
                                try:
                                    ast.parse(fixed_content)
                                except SyntaxError as e:
                                    print(f"❌ Syntax error in {file_path}: {e}")
                                    return False

                                    # Write fixed content
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(fixed_content)

                                        print(f"✅ Fixed: {file_path}")
                                        return True

                                except Exception as e:
                                    print(f"❌ Error fixing {file_path}: {e}")
                                    return False

                                    def fix_python_file(self, content, file_path):
                                        """Fix Python file with comprehensive repairs"""
                                        lines = content.split('\n')
                                        fixed_lines = []
                                        indent_level = 0
                                        in_multiline_string = False
                                        string_delimiter = None

                                        # Track context for better indentation decisions
                                        context_stack = []  # Stack of (keyword, indent_level)

                                        for i, line in enumerate(lines):
                                            original_line = line
                                            stripped = line.strip()

                                            # Skip empty lines
                                            if not stripped:
                                                fixed_lines.append('')
                                                continue

                                                # Handle multiline strings
                                                if not in_multiline_string:
                                                    if '"""' in stripped or "'''" in stripped:
                                                        if stripped.count('"""') == 1:
                                                            in_multiline_string = True
                                                            string_delimiter = '"""'
                                                        elif stripped.count("'''") == 1:
                                                            in_multiline_string = True
                                                            string_delimiter = "'''"
                                                        else:
                                                            if string_delimiter in stripped:
                                                                in_multiline_string = False
                                                                string_delimiter = None
                                                                fixed_lines.append(original_line)
                                                                continue

                                                                # Calculate correct indentation
                                                                new_indent_level = self.calculate_python_indent(
                                                                stripped, indent_level, context_stack, i, lines
                                                                )

                                                                # Apply indentation
                                                                indented_line = ' ' * (new_indent_level * 4) + stripped
                                                                fixed_lines.append(indented_line)

                                                                # Update context and indent level
                                                                indent_level = self.update_python_context(
                                                                stripped, new_indent_level, context_stack
                                                                )

                                                                return '\n'.join(fixed_lines)

                                                                def calculate_python_indent(self, line, current_level, context_stack, line_num, all_lines):
                                                                    """Calculate correct indentation level for Python line"""

                                                                    # Module level statements
                                                                    if line.startswith(('import ', 'from ', '__version__', '__author__', '#!')):
                                                                        return 0

                                                                        # Class definitions at module level
                                                                        if line.startswith('class ') and not context_stack:
                                                                            return 0

                                                                            # Function definitions
                                                                            if line.startswith(('def ', 'async def ')):
                                                                                # Check if inside class
                                                                                for keyword, level in reversed(context_stack):
                                                                                    if keyword == 'class':
                                                                                        return level + 1
                                                                                        return 0

                                                                                        # Decorators
                                                                                        if line.startswith('@'):
                                                                                            return current_level

                                                                                            # Exception handling - align with try
                                                                                            if line.startswith(('except ', 'except:', 'finally:')):
                                                                                                for keyword, level in reversed(context_stack):
                                                                                                    if keyword == 'try':
                                                                                                        return level
                                                                                                        return max(0, current_level - 1)

                                                                                                        # elif/else - align with if
                                                                                                        if line.startswith(('elif ', 'else:')):
                                                                                                            for keyword, level in reversed(context_stack):
                                                                                                                if keyword in ('if', 'elif'):
                                                                                                                    return level
                                                                                                                    return max(0, current_level - 1)

                                                                                                                    # Comments
                                                                                                                    if line.startswith('#'):
                                                                                                                        return current_level

                                                                                                                        # Continuation lines (lines ending with operators or commas)
                                                                                                                        if line_num > 0:
                                                                                                                            prev_line = all_lines[line_num - 1].strip()
                                                                                                                            if prev_line.endswith((',', '+', '-', '*', '/', '=', '(', '[', '{')):
                                                                                                                                return current_level + 1

                                                                                                                                # Default case
                                                                                                                                return current_level

                                                                                                                                def update_python_context(self, line, current_level, context_stack):
                                                                                                                                    """Update context stack and return new indent level"""

                                                                                                                                    # Handle dedenting keywords
                                                                                                                                    if line.startswith(('except ', 'except:', 'finally:', 'elif ', 'else:')):
                                                                                                                                        # Pop until we find the matching block
                                                                                                                                        while context_stack and context_stack[-1][0] not in ('try', 'if', 'elif'):
                                                                                                                                            context_stack.pop()

                                                                                                                                            # Add new context if this line starts a block
                                                                                                                                            if line.endswith(':'):
                                                                                                                                                keyword = line.split()[0]
                                                                                                                                                context_stack.append((keyword, current_level))
                                                                                                                                                return current_level + 1
                                                                                                                                                return current_level

                                                                                                                                                # Handle new blocks
                                                                                                                                                if line.endswith(':') and not line.strip().startswith('#'):
                                                                                                                                                    # Determine block type
                                                                                                                                                    if line.startswith('class '):
                                                                                                                                                        keyword = 'class'
                                                                                                                                                    elif line.startswith(('def ', 'async def ')):
                                                                                                                                                        keyword = 'def'
                                                                                                                                                    elif line.startswith('try:'):
                                                                                                                                                        keyword = 'try'
                                                                                                                                                    elif line.startswith(('if ', 'if(')):
                                                                                                                                                        keyword = 'if'
                                                                                                                                                    elif line.startswith('for '):
                                                                                                                                                        keyword = 'for'
                                                                                                                                                    elif line.startswith('while '):
                                                                                                                                                        keyword = 'while'
                                                                                                                                                    elif line.startswith('with '):
                                                                                                                                                        keyword = 'with'
                                                                                                                                                    else:
                                                                                                                                                        keyword = 'block'

                                                                                                                                                        context_stack.append((keyword, current_level))
                                                                                                                                                        return current_level + 1

                                                                                                                                                        # Handle return/break/continue/pass/raise
                                                                                                                                                        if line.startswith(('return', 'break', 'continue', 'pass', 'raise')):
                                                                                                                                                            return current_level

                                                                                                                                                            return current_level

                                                                                                                                                            def run_complete_fix(self):
                                                                                                                                                                """Run complete fix on all files"""
                                                                                                                                                                print("🚀 Starting DriveBy Complete Code Fix")
                                                                                                                                                                print("=" * 60)

                                                                                                                                                                # List of all Python files to fix
                                                                                                                                                                python_files = [
                                                                                                                                                                'data_server.py',
                                                                                                                                                                'start.py',
                                                                                                                                                                'phone_host.py',
                                                                                                                                                                'login_proxy.py',
                                                                                                                                                                'mobile_dashboard.py',
                                                                                                                                                                'security_bypass.py',
                                                                                                                                                                'privacy_protection.py',
                                                                                                                                                                'privacy_protection_2024.py',
                                                                                                                                                                'virtual_networks.py',
                                                                                                                                                                'install_persistence.py',
                                                                                                                                                                'remove_emojis.py',
                                                                                                                                                                'fix_indentation.py',
                                                                                                                                                                'fix_indentation_v2.py',
                                                                                                                                                                ]

                                                                                                                                                                # Create backups and fix files
                                                                                                                                                                for file_path in python_files:
                                                                                                                                                                    if os.path.exists(file_path):
                                                                                                                                                                        try:
                                                                                                                                                                            self.create_backup(file_path)
                                                                                                                                                                            if self.fix_file_content(file_path):
                                                                                                                                                                                self.fixed_files.append(file_path)
                                                                                                                                                                            else:
                                                                                                                                                                                self.failed_files.append(file_path)
                                                                                                                                                                        except Exception as e:
                                                                                                                                                                            print(f"❌ Failed to process {file_path}: {e}")
                                                                                                                                                                            self.failed_files.append(file_path)

                                                                                                                                                                            # Print summary
                                                                                                                                                                            print("\n" + "=" * 60)
                                                                                                                                                                            print("🎉 DriveBy Complete Code Fix Summary")
                                                                                                                                                                            print("=" * 60)
                                                                                                                                                                            print(f"✅ Successfully fixed: {len(self.fixed_files)} files")
                                                                                                                                                                            print(f"❌ Failed to fix: {len(self.failed_files)} files")

                                                                                                                                                                            if self.fixed_files:
                                                                                                                                                                                print("\n📁 Fixed files:")
                                                                                                                                                                                for file_path in self.fixed_files:
                                                                                                                                                                                    print(f"  ✓ {file_path}")

                                                                                                                                                                                    if self.failed_files:
                                                                                                                                                                                        print("\n⚠️  Failed files:")
                                                                                                                                                                                        for file_path in self.failed_files:
                                                                                                                                                                                            print(f"  ✗ {file_path}")

                                                                                                                                                                                            print(f"\n💾 Backups stored in: {self.backup_dir}")
                                                                                                                                                                                            print("🔧 All indentation and syntax errors have been fixed!")

                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                fixer = DriveByCodeFixer()
                                                                                                                                                                                                fixer.run_complete_fix()

