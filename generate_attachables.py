import json
import os
import time
from pathlib import Path

# ANSI color codes
class Colors:
    INFO = '\033[96m'      # Cyan
    SUCCESS = '\033[92m'   # Green
    WARNING = '\033[93m'   # Yellow
    ERROR = '\033[91m'     # Red
    RESET = '\033[0m'      # Reset
    BOLD = '\033[1m'       # Bold
    TITLE = '\033[95m'     # Magenta

def print_step(message, status="INFO"):
    """Print a formatted step message with colors"""
    colors = {
        "INFO": Colors.INFO,
        "SUCCESS": Colors.SUCCESS,
        "WARNING": Colors.WARNING,
        "ERROR": Colors.ERROR,
        "PROCESS": Colors.BOLD + Colors.INFO
    }
    color = colors.get(status, Colors.INFO)
    symbols = {
        "INFO": "[i]",
        "SUCCESS": "[✓]",
        "WARNING": "[!]",
        "ERROR": "[✗]",
        "PROCESS": "[►]"
    }
    symbol = symbols.get(status, "[i]")
    print(f"{color}  {symbol} {message}{Colors.RESET}")

def print_important_notice():
    """Display important notice to user"""
    print()
    print(f"{Colors.BOLD}{Colors.WARNING}{'='*64}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WARNING}  ** PLEASE READ THIS SECTION CAREFULLY **{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WARNING}{'='*64}{Colors.RESET}")
    print()
    print(f"{Colors.INFO}  Regular attachable files cannot handle items with special{Colors.RESET}")
    print(f"{Colors.INFO}  handheld display styles, which makes handheld items appear{Colors.RESET}")
    print(f"{Colors.INFO}  flat. The new version fixes this by applying unique{Colors.RESET}")
    print(f"{Colors.INFO}  animations for each handheld item.{Colors.RESET}")
    print()
    print(f"{Colors.INFO}  We currently determine handheld items through Geyser's{Colors.RESET}")
    print(f"{Colors.INFO}  mappings. If you want to add new handheld items without{Colors.RESET}")
    print(f"{Colors.INFO}  regenerating the resource pack, please visit the attachable{Colors.RESET}")
    print(f"{Colors.INFO}  file, copy it, and modify the identifier and textures under{Colors.RESET}")
    print(f"{Colors.INFO}  default and item sections.{Colors.RESET}")
    print()
    print(f"{Colors.INFO}  The new generator is based on Faithful 32X resource pack{Colors.RESET}")
    print(f"{Colors.INFO}  files. Please respect the original author's copyright:{Colors.RESET}")
    print(f"{Colors.BOLD}  https://www.faithfulpack.net/license{Colors.RESET}")
    print()
    print(f"{Colors.WARNING}  Thank you for reading.{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WARNING}{'='*64}{Colors.RESET}")
    print()
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"{Colors.WARNING}  Continuing in {i} seconds...{Colors.RESET}", end='\r')
        time.sleep(1)
    print(f"{Colors.SUCCESS}  Continuing...                    {Colors.RESET}")
    print()

def wait_for_geyser_mappings():
    """Wait for user to place Geyser mappings file"""
    print()
    print(f"{Colors.BOLD}Step 4: Geyser Mappings{Colors.RESET}")
    print("----------------------------------------------------------------")
    print()
    print(f"{Colors.INFO}  Please place the Geyser mappings file in the current folder{Colors.RESET}")
    print(f"{Colors.INFO}  and rename it to 'geyser_mappings.json' (if not already).{Colors.RESET}")
    print()
    print(f"{Colors.INFO}  Location: ./geyser_mappings.json{Colors.RESET}")
    print()
    print(f"{Colors.WARNING}  Press ENTER to continue...{Colors.RESET}")
    input()
    
    if not os.path.exists('geyser_mappings.json'):
        print_step("geyser_mappings.json not found!", "ERROR")
        return False
    
    print_step("Geyser mappings file found.", "SUCCESS")
    return True

def create_directories():
    """Create necessary output directories"""
    dirs = [
        'output/attachables',
        'output/animations',
        'output/models/entity',
        'output/render_controllers'
    ]
    
    print_step("Creating output directories...", "PROCESS")
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print_step("Output directories created successfully.", "SUCCESS")

def convert_identifier_to_filename(identifier):
    """
    Convert identifier to filename
    Example: kangelitem:item/perpol_sword -> kangelitem_item_perpol_sword.json
    """
    filename = identifier.replace(':', '_').replace('/', '_') + '.json'
    return filename

def convert_bedrock_id_to_texture_key(bedrock_identifier):
    """
    Convert bedrock_identifier to item_texture.json key
    Example: kangelitem:item/power_supply -> kangelitem.item_power_supply
    """
    # Replace : with .
    key = bedrock_identifier.replace(':', '.')
    # Replace item/ with item_
    key = key.replace('item/', 'item_')
    # Replace items/ with items_
    key = key.replace('items/', 'items_')
    return key

def read_item_texture_json():
    """Read and parse item_texture.json"""
    json_path = 'input/textures/item_texture.json'
    
    try:
        print_step("Reading item_texture.json...", "PROCESS")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        resource_pack_name = data.get('resource_pack_name', 'Unknown')
        print_step(f"Resource pack: {resource_pack_name}", "INFO")
        
        texture_data = data.get('texture_data', {})
        
        # Create a mapping dictionary
        texture_map = {}
        for identifier, item_data in texture_data.items():
            texture_path = item_data.get('textures', '')
            if texture_path:
                texture_map[identifier] = texture_path
        
        print_step(f"Loaded {len(texture_map)} texture mappings.", "SUCCESS")
        return texture_map
    
    except FileNotFoundError:
        print_step("input/textures/item_texture.json not found!", "ERROR")
        return {}
    except json.JSONDecodeError as e:
        print_step(f"Failed to parse JSON: {e}", "ERROR")
        return {}

def read_geyser_mappings():
    """Read and parse Geyser mappings file"""
    try:
        print_step("Reading geyser_mappings.json...", "PROCESS")
        
        with open('geyser_mappings.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        format_version = data.get('format_version', 'Unknown')
        print_step(f"Format version: {format_version}", "INFO")
        
        items_data = data.get('items', {})
        item_configs = []
        
        # Extract all item configurations
        for minecraft_item, configs in items_data.items():
            if isinstance(configs, list):
                for config in configs:
                    if config.get('type') == 'definition':
                        bedrock_id = config.get('bedrock_identifier', '')
                        bedrock_options = config.get('bedrock_options', {})
                        is_handheld = bedrock_options.get('display_handheld', False)
                        
                        if bedrock_id:
                            item_configs.append({
                                'bedrock_identifier': bedrock_id,
                                'is_handheld': is_handheld
                            })
        
        print_step(f"Found {len(item_configs)} item configurations.", "SUCCESS")
        return item_configs
    
    except FileNotFoundError:
        print_step("geyser_mappings.json not found!", "ERROR")
        return []
    except json.JSONDecodeError as e:
        print_step(f"Failed to parse JSON: {e}", "ERROR")
        return []

def create_attachable(bedrock_identifier, is_handheld, texture_path):
    """Create attachable JSON file for an item"""
    filename = convert_identifier_to_filename(bedrock_identifier)
    filepath = f'output/attachables/{filename}'
    
    # Determine animations based on handheld status
    if is_handheld:
        first_person_anim = "animation.player_item_held.first_person_hold_held"
        third_person_anim = "animation.player_item_held.third_person_hold_held"
    else:
        first_person_anim = "animation.player_item.first_person_hold"
        third_person_anim = "animation.player_item.third_person_hold"
    
    attachable_data = {
        "format_version": "1.10.0",
        "minecraft:attachable": {
            "description": {
                "identifier": bedrock_identifier,
                "render_controllers": ["controller.render.item_default"],
                "materials": {
                    "default": "entity_alphatest",
                    "enchanted": "entity_alphatest_glint"
                },
                "textures": {
                    "default": texture_path,
                    "enchanted": "textures/misc/enchanted_item_glint",
                    "item": texture_path
                },
                "geometry": {
                    "default": "geometry.item_size"
                },
                "animations": {
                    "first_person_hold": first_person_anim,
                    "third_person_hold": third_person_anim
                },
                "scripts": {
                    "animate": [
                        {
                            "first_person_hold": "c.is_first_person"
                        },
                        {
                            "third_person_hold": "!c.is_first_person"
                        }
                    ]
                }
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(attachable_data, f, indent=2, ensure_ascii=False)

def create_render_controller():
    """Create render controller JSON file"""
    filepath = 'output/render_controllers/item_size.render_controllers.json'
    
    render_controller_data = {
        "format_version": "1.8.0",
        "render_controllers": {
            "controller.render.item_size.animate": {
                "geometry": "Geometry.default",
                "materials": [{"*": "Material.default"}],
                "textures": ["texture.item"]
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(render_controller_data, f, indent=2, ensure_ascii=False)
    
    print_step("Render controller file created.", "SUCCESS")

def create_geometry():
    """Create geometry JSON file"""
    filepath = 'output/models/entity/item_size.geo.json'
    
    geometry_data = {
        "format_version": "1.16.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.item_size",
                    "texture_width": 16,
                    "texture_height": 16,
                    "visible_bounds_width": 1,
                    "visible_bounds_height": 1,
                    "visible_bounds_offset": [0, 0, 0]
                },
                "bones": [
                    {
                        "name": "root_item",
                        "pivot": [0, 0, 0],
                        "rotation": [0, 87.5, 0],
                        "binding": "q.item_slot_to_bone_name(context.item_slot)",
                        "texture_meshes": [
                            {
                                "texture": "default",
                                "position": [-8, -7, 3],
                                "rotation": [0, 90, -90],
                                "local_pivot": [9, -2, 9],
                                "scale": [1, 2, 1]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(geometry_data, f, indent=2, ensure_ascii=False)
    
    print_step("Geometry file created.", "SUCCESS")

def create_player_item_animation():
    """Create player_item animation JSON file"""
    filepath = 'output/animations/player_item.json'
    
    animation_data = {
        "format_version": "1.8.0",
        "animations": {
            "animation.player_item.third_person_hold": {
                "loop": True,
                "animation_length": 10,
                "bones": {
                    "root_item": {
                        "rotation": [283.00481, -107.53494, -439.9079],
                        "position": [1.29869, 28.09352, -7.93738],
                        "scale": 0.55
                    }
                }
            },
            "animation.player_item.first_person_hold": {
                "loop": True,
                "animation_length": 10,
                "bones": {
                    "root_item": {
                        "rotation": [271.13165, -26.19883, -69.62689],
                        "position": [-5.02343, 13.98217, -3.72306],
                        "scale": [1.4, 1.4, 1.4]
                    }
                }
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(animation_data, f, indent=2, ensure_ascii=False)
    
    print_step("Player item animation file created.", "SUCCESS")

def create_player_item_held_animation():
    """Create player_item_held animation JSON file"""
    filepath = 'output/animations/player_item_held.json'
    
    animation_data = {
        "format_version": "1.8.0",
        "animations": {
            "animation.player_item_held.third_person_hold_held": {
                "loop": True,
                "animation_length": 10,
                "bones": {
                    "root_item": {
                        "rotation": [-36.67548, -86.85374, -179.50132],
                        "position": [-3.36827, 26.60414, -14.20191],
                        "scale": [0.75, 1, 1]
                    }
                }
            },
            "animation.player_item_held.first_person_hold_held": {
                "loop": True,
                "animation_length": 10,
                "bones": {
                    "root_item": {
                        "rotation": [304.15889, -147.41223, -238.55658],
                        "position": [2.10302, -3.83105, 10.43465],
                        "scale": 1.4
                    }
                }
            }
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(animation_data, f, indent=2, ensure_ascii=False)
    
    print_step("Player item held animation file created.", "SUCCESS")

def main():
    print()
    print(f"{Colors.BOLD}Step 3: Important Information{Colors.RESET}")
    print("----------------------------------------------------------------")
    
    # Display important notice
    print_important_notice()
    
    # Wait for Geyser mappings
    if not wait_for_geyser_mappings():
        return 1
    
    print()
    print(f"{Colors.BOLD}Step 5: File Generation{Colors.RESET}")
    print("----------------------------------------------------------------")
    print()
    
    # Create directories
    create_directories()
    
    # Read item_texture.json
    print()
    texture_map = read_item_texture_json()
    
    if not texture_map:
        print_step("Failed to load texture mappings!", "ERROR")
        return 1
    
    # Read Geyser mappings
    print()
    item_configs = read_geyser_mappings()
    
    if not item_configs:
        print_step("No item configurations found!", "ERROR")
        return 1
    
    # Create attachable files
    print()
    print_step("Generating attachable files...", "PROCESS")
    print()
    
    handheld_count = 0
    regular_count = 0
    matched_count = 0
    missing_count = 0
    
    for config in item_configs:
        bedrock_id = config['bedrock_identifier']
        is_handheld = config['is_handheld']
        
        # Convert bedrock_identifier to texture key
        texture_key = convert_bedrock_id_to_texture_key(bedrock_id)
        
        # Look up texture path
        texture_path = texture_map.get(texture_key)
        
        if texture_path:
            create_attachable(bedrock_id, is_handheld, texture_path)
            
            filename = convert_identifier_to_filename(bedrock_id)
            item_type = f"{Colors.WARNING}[HANDHELD]{Colors.RESET}" if is_handheld else f"{Colors.INFO}[REGULAR]{Colors.RESET}"
            print(f"  {item_type} {filename}")
            print(f"    └─ Key: {texture_key}")
            print(f"    └─ Texture: {texture_path}")
            
            matched_count += 1
            if is_handheld:
                handheld_count += 1
            else:
                regular_count += 1
        else:
            print(f"  {Colors.ERROR}[MISSING]{Colors.RESET} {bedrock_id}")
            print(f"    └─ Key not found: {texture_key}")
            missing_count += 1
    
    print()
    print_step(f"Generated {matched_count} attachable files.", "SUCCESS")
    print_step(f"  - Handheld items: {handheld_count}", "INFO")
    print_step(f"  - Regular items: {regular_count}", "INFO")
    
    if missing_count > 0:
        print_step(f"  - Missing textures: {missing_count}", "WARNING")
    
    # Create shared files
    print()
    print_step("Generating shared resource files...", "PROCESS")
    print()
    create_render_controller()
    create_geometry()
    create_player_item_animation()
    create_player_item_held_animation()
    
    print()
    print_step("All files generated successfully!", "SUCCESS")
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print()
        print_step("Operation cancelled by user.", "WARNING")
        exit(1)
    except Exception as e:
        print_step(f"Unexpected error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        exit(1)
