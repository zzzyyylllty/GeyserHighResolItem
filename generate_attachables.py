import json
import os
from pathlib import Path

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*64}")
    print(f"  {title}")
    print(f"{'='*64}\n")

def print_step(message, status="INFO"):
    """Print a formatted step message"""
    symbols = {
        "INFO": "[→]",
        "OK": "[✓]",
        "ERROR": "[✗]",
        "PROCESS": "[►]"
    }
    symbol = symbols.get(status, "[i]")
    print(f"  {symbol} {message}")

def create_directories():
    """Create necessary output directories"""
    dirs = [
        'output/attachables',
        'output/animations',
        'output/models/entity',
        'output/render_controllers'
    ]
    
    print_step("Creating output directories...", "INFO")
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print_step("Output directories created successfully.", "OK")

def convert_identifier(identifier):
    """
    Convert identifier format
    Example: kangelitem.item_power_supply -> kangelitem:item/power_supply
             namespace.items_diamond -> namespace:items/diamond
    """
    # Split by first dot to separate namespace and item
    parts = identifier.split('.', 1)
    if len(parts) != 2:
        return identifier
    
    namespace = parts[0]
    item_part = parts[1]
    
    # Replace item_ or items_ with item/ or items/
    if item_part.startswith('item_'):
        item_part = 'item/' + item_part[5:]
    elif item_part.startswith('items_'):
        item_part = 'items/' + item_part[6:]
    
    # Combine with colon
    return f"{namespace}:{item_part}"

def read_item_texture_json():
    """Read and parse item_texture.json"""
    json_path = 'input/textures/item_texture.json'
    
    print_step("Reading item_texture.json...", "PROCESS")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        resource_pack_name = data.get('resource_pack_name', 'Unknown')
        print_step(f"Resource pack: {resource_pack_name}", "INFO")
        
        texture_data = data.get('texture_data', {})
        items = []
        
        for identifier, item_data in texture_data.items():
            texture_path = item_data.get('textures', '')
            if texture_path:
                converted_id = convert_identifier(identifier)
                items.append((identifier, converted_id, texture_path))
        
        print_step(f"Found {len(items)} items to process.", "OK")
        return items
    
    except FileNotFoundError:
        print_step("input/textures/item_texture.json not found!", "ERROR")
        return []
    except json.JSONDecodeError as e:
        print_step(f"Failed to parse JSON: {e}", "ERROR")
        return []

def create_attachable(original_identifier, converted_identifier, texture_path):
    """Create attachable JSON file for an item"""
    filename = original_identifier.replace('.', '_') + '.json'
    filepath = f'output/attachables/{filename}'
    
    attachable_data = {
        "format_version": "1.10.0",
        "minecraft:attachable": {
            "description": {
                "identifier": converted_identifier,
                "materials": {
                    "default": "entity_alphatest",
                    "enchanted": "entity_alphatest_glint"
                },
                "textures": {
                    "default": texture_path,
                    "enchanted": "textures/misc/enchanted_item_glint"
                },
                "geometry": {
                    "default": "geometry.large_item"
                },
                "animations": {
                    "hold": "animation.large_item.hold"
                },
                "scripts": {
                    "animate": ["hold"]
                },
                "render_controllers": ["controller.render.large_item"]
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(attachable_data, f, indent=4, ensure_ascii=False)

def create_animation_file():
    """Create animation JSON file"""
    filepath = 'output/animations/large_item.animation.json'
    
    animation_data = {
        "format_version": "1.10.0",
        "animations": {
            "animation.large_item.hold": {
                "loop": True,
                "bones": {
                    "rightitem": {
                        "position": [
                            "c.is_first_person ? -6 : 1",
                            "c.is_first_person ? 0 : -1",
                            "c.is_first_person ? -1 : -6"
                        ],
                        "rotation": [
                            "c.is_first_person ? 45 : 15",
                            "c.is_first_person ? -15 : 0",
                            "c.is_first_person ? 30 : -165"
                        ],
                        "scale": [
                            "c.is_first_person ? 1 : 0.5",
                            "c.is_first_person ? 1 : 0.5",
                            "c.is_first_person ? 1 : 0.5"
                        ]
                    }
                }
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(animation_data, f, indent=4, ensure_ascii=False)
    
    print_step("Animation file created.", "OK")

def create_geometry_file():
    """Create geometry JSON file"""
    filepath = 'output/models/entity/large_item.geo.json'
    
    geometry_data = {
        "format_version": "1.16.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.large_item",
                    "texture_width": 16,
                    "texture_height": 16,
                    "visible_bounds_width": 2,
                    "visible_bounds_height": 1.5,
                    "visible_bounds_offset": [0, 0.25, 0]
                },
                "bones": [
                    {
                        "name": "rightitem",
                        "pivot": [0, 0, 0],
                        "texture_meshes": [
                            {
                                "texture": "default",
                                "position": [0, 0, 0],
                                "local_pivot": [8, 0, 8]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(geometry_data, f, indent=4, ensure_ascii=False)
    
    print_step("Geometry file created.", "OK")

def create_render_controller_file():
    """Create render controller JSON file"""
    filepath = 'output/render_controllers/large_item.render_controllers.json'
    
    render_controller_data = {
        "format_version": "1.8.0",
        "render_controllers": {
            "controller.render.large_item": {
                "geometry": "Geometry.default",
                "materials": [{"*": "variable.is_enchanted ? Material.enchanted : Material.default"}],
                "textures": ["Texture.default", "Texture.enchanted"]
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(render_controller_data, f, indent=4, ensure_ascii=False)
    
    print_step("Render controller file created.", "OK")

def main():
    print_section("Bedrock Large Item Generator")
    
    # Create directories
    create_directories()
    
    # Read item texture data
    print("\n")
    items = read_item_texture_json()
    
    if not items:
        print_step("No items found to process!", "ERROR")
        return 1
    
    # Create attachable files
    print("\n")
    print_step("Generating attachable files...", "PROCESS")
    print()
    
    for original_id, converted_id, texture_path in items:
        create_attachable(original_id, converted_id, texture_path)
        filename = original_id.replace('.', '_') + '.json'
        print(f"    • {filename}")
        print(f"      └─ ID: {original_id} → {converted_id}")
    
    print()
    print_step(f"Generated {len(items)} attachable files.", "OK")
    
    # Create shared files
    print("\n")
    print_step("Generating shared resource files...", "PROCESS")
    print()
    create_animation_file()
    create_geometry_file()
    create_render_controller_file()
    
    print("\n")
    print_step("All files generated successfully!", "OK")
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except Exception as e:
        print_step(f"Unexpected error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        exit(1)
