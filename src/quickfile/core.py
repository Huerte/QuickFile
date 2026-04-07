import os
from pathlib import Path

def create_file(prefix, extension):
    count = 1
    file_name = Path(f"{prefix}{count}.{extension}" if extension else f"{prefix}{count}")
    
    while file_name.exists():
        count += 1
        file_name = Path(f"{prefix}{count}.{extension}" if extension else f"{prefix}{count}")
        
    file_name.touch(exist_ok=True)
    print(f"Created: {file_name}")
    return True

def generate_files(filename, count, config):
    if not filename:
        return False
        
    if '.' not in filename:
        prefix = config.get('prefix', 'file')
        extension = filename
    else:
        # If multiple dots exist, split only on the first or last depending on need.
        # But for simple extensions:
        parts = filename.split('.', 1)
        prefix = parts[0]
        extension = parts[1] if len(parts) > 1 else ""

    for _ in range(count):
        create_file(prefix, extension)
        
    return True
