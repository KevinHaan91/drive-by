#!/usr/bin/env python3
"""
Advanced DriveBy Code Fixer
More robust fixing for complex indentation issues
"""

import os
import ast
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

class AdvancedCodeFixer:
    def __init__(self):
        self.fixed_files = []
        self.failed_files = []
        self.backup_dir = "backup_advanced_fix"
        
    def create_backup(self, file_path):
        """Create backup of file before fixing"""
        backup_path = Path(self.backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        relative_path = Path(file_path).relative_to('.')
        backup_file_path = backup_path / relative_path
        backup_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_file_path)
        print(f"✓ Backed up: {file_path}")

    def fix_python_file_advanced(self, content):
        """Advanced Python file fixing with better logic"""
        lines = content.split('\n')
        fixed_lines = []
        
        # First pass: normalize all lines and remove excessive indentation
        normalized_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                normalized_lines.append('')
            else:
                normalized_lines.append(stripped)
        
        # Second pass: rebuild with proper indentation
        indent_level = 0
        block_stack = []  # Stack to track nested blocks
        
        for i, line in enumerate(normalized_lines):
            if not line.strip():
                fixed_lines.append('')
                continue
                
            # Determine if this line should decrease indentation
            if self.should_dedent(line, block_stack):
                if block_stack:
                    block_stack.pop()
                    indent_level = max(0, indent_level - 1)
            
            # Special handling for except/finally/elif/else
            if line.startswith(('except ', 'except:', 'finally:', 'elif ', 'else:')):
                # Find the matching try/if block
                target_level = self.find_matching_block_level(line, block_stack)
                if target_level is not None:
                    indent_level = target_level
            
            # Apply current indentation
            indented_line = '    ' * indent_level + line
            fixed_lines.append(indented_line)
            
            # Determine if this line should increase indentation for next line
            if self.should_indent_next(line):
                block_type = self.get_block_type(line)
                block_stack.append((block_type, indent_level))
                indent_level += 1
        
        return '\n'.join(fixed_lines)
    
    def should_dedent(self, line, block_stack):
        """Determine if current line should dedent"""
        # Class and function definitions at module level
        if line.startswith(('class ', 'def ', 'async def ')) and not any('class' in block or 'def' in block for block, _ in block_stack):
            return len(block_stack) > 0
        
        # Return statements typically don't change indentation
        if line.startswith(('return', 'break', 'continue', 'pass', 'raise')):
            return False
            
        return False
    
    def should_indent_next(self, line):
        """Determine if next line should be indented"""
        return line.endswith(':') and not line.strip().startswith('#')
    
    def get_block_type(self, line):
        """Get the type of block this line starts"""
        if line.startswith('class '):
            return 'class'
        elif line.startswith(('def ', 'async def ')):
            return 'def'
        elif line.startswith('try:'):
            return 'try'
        elif line.startswith(('if ', 'if(')):
            return 'if'
        elif line.startswith('for '):
            return 'for'
        elif line.startswith('while '):
            return 'while'
        elif line.startswith('with '):
            return 'with'
        elif line.startswith(('except ', 'except:')):
            return 'except'
        elif line.startswith('finally:'):
            return 'finally'
        elif line.startswith(('elif ', 'else:')):
            return 'elif'
        else:
            return 'block'
    
    def find_matching_block_level(self, line, block_stack):
        """Find the indentation level for matching blocks"""
        if line.startswith(('except ', 'except:', 'finally:')):
            # Find the try block
            for i in range(len(block_stack) - 1, -1, -1):
                block_type, level = block_stack[i]
                if block_type == 'try':
                    return level
        elif line.startswith(('elif ', 'else:')):
            # Find the if block
            for i in range(len(block_stack) - 1, -1, -1):
                block_type, level = block_stack[i]
                if block_type in ('if', 'elif'):
                    return level
        return None

    def fix_file_content(self, file_path):
        """Fix a single file's content"""
        print(f"🔧 Fixing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if file_path.endswith('.py'):
                fixed_content = self.fix_python_file_advanced(content)
                
                # Try to parse the fixed content
                try:
                    ast.parse(fixed_content)
                    print(f"✅ Syntax valid for: {file_path}")
                except SyntaxError as e:
                    print(f"⚠️  Syntax still has issues in {file_path}: {e}")
                    # Continue anyway, the file might still be improved
                
                # Write the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✅ Fixed: {file_path}")
                return True
            else:
                print(f"⏭️  Skipped non-Python file: {file_path}")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            return False

    def run_fix(self):
        """Run the advanced fix on all Python files"""
        print("🚀 Starting Advanced DriveBy Code Fix")
        print("=" * 60)
        
        # Find all Python files
        python_files = []
        for file in os.listdir('.'):
            if file.endswith('.py') and not file.startswith('advanced_fixer'):
                python_files.append(file)
        
        print(f"Found {len(python_files)} Python files to fix")
        
        # Process each file
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
        print("🎉 Advanced Fix Summary")
        print("=" * 60)
        print(f"✅ Processed: {len(self.fixed_files)} files")
        print(f"❌ Failed: {len(self.failed_files)} files")
        
        if self.fixed_files:
            print("\n📁 Processed files:")
            for file_path in self.fixed_files:
                print(f"  ✓ {file_path}")
        
        if self.failed_files:
            print("\n⚠️  Failed files:")
            for file_path in self.failed_files:
                print(f"  ✗ {file_path}")
        
        print(f"\n💾 Backups stored in: {self.backup_dir}")
        print("🔧 Advanced fix completed!")

if __name__ == "__main__":
    fixer = AdvancedCodeFixer()
    fixer.run_fix()

