import os
from pathlib import Path
from datetime import datetime

def generate_files(filename, count, config, **options):
    """Generate multiple files based on name/extension and options."""
    if not filename:
        return False
        
    # Determine prefix and extension
    if '.' not in filename:
        prefix = config.get('prefix', 'file')
        extension = filename
    else:
        parts = filename.rsplit('.', 1)
        prefix = parts[0]
        extension = parts[1] if len(parts) > 1 else ""

    created_in_session = set()
    
    # Check for padding and start_index in config
    padding = int(config.get('padding', 0))
    start_index = int(config.get('start_index', 1))
    
    # Overwrite with options if provided
    padding = int(options.get('padding', padding))
    start_index = int(options.get('start_index', start_index))

    for _ in range(count):
        # We need to find the next available name, considering what we've already "created" in this session
        sub_count = start_index
        output_path = Path(options.get('output_dir')) if options.get('output_dir') else Path.cwd()
        
        # Determine initial name without sequence if possible
        first_attempt = True
        
        while True:
            # Handle patterns in prefix
            current_prefix = prefix
            if "{date}" in current_prefix:
                current_prefix = current_prefix.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
            
            if first_attempt and '.' in filename and "{n}" not in filename:
                # If they provided a full name like 'test.txt' and no {n}, try it as is first
                file_name = filename
                first_attempt = False
            else:
                # Standard sequential naming
                count_str = str(sub_count).zfill(padding)
                if "{n}" in current_prefix:
                    file_name_candidate = current_prefix.replace("{n}", count_str)
                    if extension:
                        file_name = f"{file_name_candidate}.{extension}"
                    else:
                        file_name = file_name_candidate
                else:
                    if extension:
                        file_name = f"{current_prefix}{count_str}.{extension}"
                    else:
                        file_name = f"{current_prefix}{count_str}"
                sub_count += 1
            
            file_path = output_path / file_name
            if not file_path.exists() and file_path not in created_in_session:
                break
            
        created_in_session.add(file_path)
        
        create_file(
            prefix=None,
            extension=None, 
            output_dir=options.get('output_dir'),
            content=options.get('content'),
            template_path=options.get('template'),
            dry_run=options.get('dry_run', False),
            quiet=options.get('quiet', False),
            force_name=file_name
        )
    
    # Save the paths of created files for 'undo' command
    if not options.get('dry_run'):
        from . import config as cfg
        cfg.save_last_run([str(p.absolute()) for p in created_in_session])
        
    return True

def create_file(prefix, extension, output_dir=None, content=None, template_path=None, dry_run=False, quiet=False, force_name=None):
    """Create a single file with sequential naming and optional content."""
    # Set output path
    output_path = Path(output_dir) if output_dir else Path.cwd()
    
    if force_name:
        file_path = output_path / force_name
    else:
        # Fallback (should not be reached if called from generate_files)
        count = 1
        if extension:
            file_name = f"{prefix}{count}.{extension}"
        else:
            file_name = f"{prefix}{count}"
        file_path = output_path / file_name
        
        while file_path.exists():
            count += 1
            if extension:
                file_name = f"{prefix}{count}.{extension}"
            else:
                file_name = f"{prefix}{count}"
            file_path = output_path / file_name
        
    if dry_run:
        if not quiet:
            print(f"[DRY-RUN] Would create: {file_path}")
        return True

    # Ensure output directory exists
    if output_dir:
        file_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine content
    final_content = content or ""
    if template_path:
        template = Path(template_path)
        if template.exists():
            final_content = template.read_text()
        else:
            if not quiet:
                print(f"Warning: Template file '{template_path}' not found. Using empty content.")

    # Variable replacement in content
    if final_content:
        now = datetime.now()
        final_content = final_content.replace("{n}", force_name if force_name else "")
        final_content = final_content.replace("{date}", now.strftime("%Y-%m-%d"))
        final_content = final_content.replace("{time}", now.strftime("%H:%M:%S"))
        final_content = final_content.replace("{filename}", file_path.name)

    # Write file
    file_path.write_text(final_content)
    
    if not quiet:
        print(f"Created: {file_path}")
    return True
