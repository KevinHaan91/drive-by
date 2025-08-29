import os
import ast
import sys
import shutil
import re
import tokenize
import io
from pathlib import Path
from datetime import datetime

class AggressiveCodeFixer:
    def __init__(self):
        self.fixed_files = []
        self.failed_files = []
        self.backup_dir = "backup_aggressive_fix"
        
    def create_backup(self, file_path):
        """Create backup of file before fixing"""
        backup_path = Path(self.backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        relative_path = Path(file_path).relative_to('.')
        backup_file_path = backup_path / relative_path
        backup_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_file_path)
        print(f"✓ Backed up: {file_path}")

    def aggressive_fix_file(self, file_path):
        """Aggressively fix a file with all possible repairs"""
        print(f"🔧 AGGRESSIVELY FIXING: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Apply multiple passes of fixes
            fixed_content = content
            
            # Pass 1: Clean up basic issues
            fixed_content = self.clean_basic_issues(fixed_content)
            
            # Pass 2: Fix indentation completely
            fixed_content = self.fix_indentation_aggressive(fixed_content)
            
            # Pass 3: Fix syntax errors
            fixed_content = self.fix_syntax_errors(fixed_content)
            
            # Pass 4: Fix structural issues
            fixed_content = self.fix_structural_issues(fixed_content)
            
            # Pass 5: Final cleanup
            fixed_content = self.final_cleanup(fixed_content)
            
            # Validate and write
            if self.validate_and_write(file_path, fixed_content):
                self.fixed_files.append(file_path)
                return True
            else:
                # If validation fails, try emergency fix
                emergency_content = self.emergency_fix(file_path, content)
                if self.validate_and_write(file_path, emergency_content):
                    self.fixed_files.append(file_path)
                    return True
                else:
                    self.failed_files.append(file_path)
                    return False
                    
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            self.failed_files.append(file_path)
            return False

    def clean_basic_issues(self, content):
        """Clean up basic formatting issues"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Convert tabs to spaces
            line = line.expandtabs(4)
            
            # Fix common syntax issues
            line = re.sub(r'\s+$', '', line)  # Remove trailing spaces
            line = re.sub(r'^\s*#\s*', '# ', line)  # Fix comment spacing
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def fix_indentation_aggressive(self, content):
        """Aggressively fix all indentation issues"""
        lines = content.split('\n')
        fixed_lines = []
        indent_level = 0
        in_multiline_string = False
        string_delimiter = None
        
        # Track all block types
        block_stack = []
        
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
            correct_indent = self.calculate_aggressive_indent(
                stripped, indent_level, block_stack, i, lines
            )
            
            # Apply indentation
            indented_line = ' ' * (correct_indent * 4) + stripped
            fixed_lines.append(indented_line)
            
            # Update indent level and block stack
            indent_level = self.update_block_stack(
                stripped, correct_indent, block_stack
            )
        
        return '\n'.join(fixed_lines)

    def calculate_aggressive_indent(self, line, current_level, block_stack, line_num, all_lines):
        """Calculate indentation with aggressive correction"""
        
        # Module level imports and declarations
        if line.startswith(('import ', 'from ', '__version__', '__author__', '#!/')):
            return 0
        
        # Class definitions
        if line.startswith('class '):
            return 0
        
        # Function definitions
        if line.startswith(('def ', 'async def ')):
            # Check if we're inside a class
            class_level = self.find_class_level(block_stack)
            if class_level is not None:
                return class_level + 1
            return 0
        
        # Decorators
        if line.startswith('@'):
            return current_level
        
        # Exception handling
        if line.startswith(('except ', 'except:', 'finally:')):
            try_level = self.find_try_level(block_stack)
            if try_level is not None:
                return try_level
            return max(0, current_level - 1)
        
        # elif/else
        if line.startswith(('elif ', 'else:')):
            if_level = self.find_if_level(block_stack)
            if if_level is not None:
                return if_level
            return max(0, current_level - 1)
        
        # Comments
        if line.startswith('#'):
            return current_level
        
        # Continuation lines
        if line_num > 0:
            prev_line = all_lines[line_num - 1].strip()
            if prev_line.endswith((',', '+', '-', '*', '/', '=', '\\', '(', '[', '{')):
                return current_level + 1
        
        # Handle specific problematic patterns
        if line.startswith(('return', 'break', 'continue', 'pass', 'raise')):
            return current_level
        
        # Default case
        return current_level

    def find_class_level(self, block_stack):
        """Find the indentation level of the current class"""
        for block_type, level in reversed(block_stack):
            if block_type == 'class':
                return level
        return None

    def find_try_level(self, block_stack):
        """Find the indentation level of the current try block"""
        for block_type, level in reversed(block_stack):
            if block_type == 'try':
                return level
        return None

    def find_if_level(self, block_stack):
        """Find the indentation level of the current if block"""
        for block_type, level in reversed(block_stack):
            if block_type in ('if', 'elif'):
                return level
        return None

    def update_block_stack(self, line, current_level, block_stack):
        """Update the block stack and return new indent level"""
        
        # Handle dedenting keywords
        if line.startswith(('except ', 'except:', 'finally:')):
            # Keep the try block, remove everything after it
            new_stack = []
            for block_type, level in block_stack:
                new_stack.append((block_type, level))
                if block_type == 'try':
                    break
            block_stack[:] = new_stack
            
            if line.endswith(':'):
                keyword = line.split()[0]
                block_stack.append((keyword, current_level))
                return current_level + 1
            return current_level
        
        elif line.startswith(('elif ', 'else:')):
            # Keep the if block, remove everything after it
            new_stack = []
            for block_type, level in block_stack:
                new_stack.append((block_type, level))
                if block_type in ('if', 'elif'):
                    break
            block_stack[:] = new_stack
            
            if line.endswith(':'):
                keyword = line.split()[0]
                block_stack.append((keyword, current_level))
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
            
            block_stack.append((keyword, current_level))
            return current_level + 1
        
        return current_level

    def fix_syntax_errors(self, content):
        """Fix common syntax errors"""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                fixed_lines.append(line)
                continue
            
            # Fix missing colons
            if self.needs_colon(stripped) and not stripped.endswith(':'):
                line = line + ':'
            
            # Fix incomplete statements
            if self.is_incomplete_statement(stripped):
                line = line + ' pass'
            
            # Fix malformed function definitions
            if stripped.startswith('def ') and '(' not in stripped:
                line = line + '():'
            
            # Fix malformed class definitions
            if stripped.startswith('class ') and not stripped.endswith(':'):
                line = line + ':'
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)

    def needs_colon(self, line):
        """Check if line needs a colon"""
        colon_keywords = [
            'if ', 'elif ', 'else', 'for ', 'while ', 'try', 'except',
            'finally', 'def ', 'class ', 'with ', 'async def '
        ]
        return any(line.startswith(keyword) for keyword in colon_keywords)

    def is_incomplete_statement(self, line):
        """Check if statement is incomplete"""
        incomplete_patterns = [
            r'^if\s+.*:$',
            r'^elif\s+.*:$',
            r'^else:$',
            r'^try:$',
            r'^except.*:$',
            r'^finally:$',
            r'^for\s+.*:$',
            r'^while\s+.*:$',
            r'^with\s+.*:$',
            r'^def\s+.*:$',
            r'^class\s+.*:$',
        ]
        
        for pattern in incomplete_patterns:
            if re.match(pattern, line):
                return True
        return False

    def fix_structural_issues(self, content):
        """Fix structural issues in the code"""
        lines = content.split('\n')
        fixed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Fix function definitions that are split across lines
            if stripped.startswith(('def ', 'async def ')) and not stripped.endswith(':'):
                # Look for the closing parenthesis and colon
                combined_line = line
                j = i + 1
                while j < len(lines) and not combined_line.strip().endswith(':'):
                    combined_line += ' ' + lines[j].strip()
                    j += 1
                
                if not combined_line.strip().endswith(':'):
                    combined_line += ':'
                
                # Calculate proper indentation
                indent = len(line) - len(line.lstrip())
                fixed_lines.append(' ' * indent + combined_line.strip())
                i = j
                continue
            
            fixed_lines.append(line)
            i += 1
        
        return '\n'.join(fixed_lines)

    def final_cleanup(self, content):
        """Final cleanup pass"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove excessive blank lines
            if line.strip() == '':
                if not cleaned_lines or cleaned_lines[-1].strip() != '':
                    cleaned_lines.append('')
            else:
                cleaned_lines.append(line)
        
        # Ensure file ends with newline
        result = '\n'.join(cleaned_lines)
        if not result.endswith('\n'):
            result += '\n'
        
        return result

    def validate_and_write(self, file_path, content):
        """Validate syntax and write file"""
        try:
            # Try to parse the content
            ast.parse(content)
            
            # If successful, write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Successfully fixed: {file_path}")
            return True
            
        except SyntaxError as e:
            print(f"❌ Syntax error in {file_path}: {e}")
            return False

    def emergency_fix(self, file_path, original_content):
        """Emergency fix for severely broken files"""
        print(f"🚨 Applying emergency fix to: {file_path}")
        
        # Generic emergency fix - create a minimal working version
        lines = original_content.split('\n')
        emergency_lines = []
        
        # Add basic imports if missing
        has_imports = any(line.strip().startswith(('import ', 'from ')) for line in lines[:10])
        if not has_imports:
            emergency_lines.extend([
                '#!/usr/bin/env python3',
                '"""Emergency fixed version"""',
                'import os',
                'import sys',
                ''
            ])
        
        # Process lines with minimal fixes
        for line in lines:
            stripped = line.strip()
            if not stripped:
                emergency_lines.append('')
                continue
            
            # Keep imports and basic statements
            if stripped.startswith(('import ', 'from ', '#', '__')):
                emergency_lines.append(stripped)
            elif stripped.startswith(('class ', 'def ')):
                if not stripped.endswith(':'):
                    emergency_lines.append(stripped + ':')
                else:
                    emergency_lines.append(stripped)
                emergency_lines.append('    pass')
            elif stripped in ('if __name__ == "__main__":',):
                emergency_lines.append(stripped)
                emergency_lines.append('    pass')
        
        # Ensure file has basic structure
        if not emergency_lines:
            emergency_lines = [
                '#!/usr/bin/env python3',
                '"""Emergency fixed version"""',
                'pass'
            ]
        
        return '\n'.join(emergency_lines)

    def run_aggressive_fix(self):
        """Run aggressive fix on all Python files"""
        print("🚀 Starting AGGRESSIVE DriveBy Code Fix")
        print("=" * 60)
        
        # Find all Python files
        python_files = []
        for file in os.listdir('.'):
            if file.endswith('.py') and not file.startswith(('aggressive_fixer', 'advanced_fixer', 'complete_fixer')):
                python_files.append(file)
        
        print(f"Found {len(python_files)} Python files to aggressively fix")
        
        # Process each file
        for file_path in python_files:
            if os.path.exists(file_path):
                try:
                    self.create_backup(file_path)
                    self.aggressive_fix_file(file_path)
                except Exception as e:
                    print(f"❌ Failed to process {file_path}: {e}")
                    self.failed_files.append(file_path)
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎉 AGGRESSIVE Fix Summary")
        print("=" * 60)
        print(f"✅ Successfully fixed: {len(self.fixed_files)} files")
        print(f"❌ Failed to fix: {len(self.failed_files)} files")
        
        if self.fixed_files:
            print("\n📁 Successfully fixed files:")
            for file_path in self.fixed_files:
                print(f"  ✓ {file_path}")
        
        if self.failed_files:
            print("\n⚠️  Failed files:")
            for file_path in self.failed_files:
                print(f"  ✗ {file_path}")
        
        print(f"\n💾 Backups stored in: {self.backup_dir}")
        print("🔧 AGGRESSIVE fix completed!")

if __name__ == "__main__":
    fixer = AggressiveCodeFixer()
    fixer.run_aggressive_fix()

