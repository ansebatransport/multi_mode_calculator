---
name: plugin-system
description: Use when creating, installing, or managing plugins that extend agent capabilities. Trigger on phrases like "plugin", "extension", "add-on", "install plugin", "create plugin", "marketplace", "bundle", "share skill", or when packaging skills for reuse.
---

# Plugin System Skill

Package, share, and install reusable agent capabilities.

## Plugin Structure

```
.opencode/plugins/
  ├── my-plugin/
  │   ├── plugin.json         # Plugin manifest
  │   ├── SKILL.md            # Skill instructions
  │   ├── scripts/            # Helper scripts
  │   ├── templates/          # Code templates
  │   └── README.md           # Usage documentation
  └── another-plugin/
      └── ...
```

## Plugin Manifest

```json
{
  "name": "my-calculator-plugin",
  "version": "1.0.0",
  "description": "Extends calculator with new capabilities",
  "author": "Mulugeta",
  "skills": ["skill-name"],
  "scripts": ["scripts/setup.sh"],
  "templates": ["templates/new-module.py"],
  "dependencies": [],
  "minVersion": "0.1.0",
  "tags": ["calculator", "math", "tools"]
}
```

## Creating a Plugin

### Step 1: Define Plugin
```bash
mkdir -p .opencode/plugins/my-plugin/{scripts,templates}
```

### Step 2: Create Manifest
```json
{
  "name": "financial-analysis",
  "version": "1.0.0",
  "description": "Advanced financial analysis tools",
  "skills": ["financial-analysis"],
  "templates": [
    "templates/financial-module.py",
    "templates/financial-test.py"
  ]
}
```

### Step 3: Create Skill
```markdown
---
name: financial-analysis
description: Use when performing advanced financial analysis...
---

# Financial Analysis Plugin

## Features
- [feature 1]
- [feature 2]

## Usage
[instructions]
```

### Step 4: Create Templates
```python
# templates/financial-module.py
"""{{ module_name }} - {{ description }}"""

from typing import Optional

def {{ function_name }}({{ params }}) -> {{ return_type }}:
    """{{ docstring }}"""
    pass
```

### Step 5: Package Plugin
```bash
# Create plugin archive
cd .opencode/plugins
tar -czf financial-analysis-1.0.0.tar.gz financial-analysis/

# Or zip
zip -r financial-analysis-1.0.0.zip financial-analysis/
```

## Installing Plugins

### From Local File
```bash
# Copy plugin to plugins directory
cp -r /path/to/plugin .opencode/plugins/

# Or from archive
tar -xzf plugin-1.0.0.tar.gz -C .opencode/plugins/
```

### From URL
```bash
# Download and install
curl -LO https://example.com/plugin-1.0.0.tar.gz
tar -xzf plugin-1.0.0.tar.gz -C .opencode/plugins/
```

### From Git
```bash
# Clone plugin repo
git clone https://github.com/user/plugin.git .opencode/plugins/plugin
```

## Plugin Manager

```bash
#!/bin/bash
# plugin-manager.sh

PLUGIN_DIR=".opencode/plugins"

list_plugins() {
    echo "Installed plugins:"
    for dir in "$PLUGIN_DIR"/*/; do
        if [ -f "$dir/plugin.json" ]; then
            name=$(python3 -c "import json; print(json.load(open('$dir/plugin.json'))['name'])")
            version=$(python3 -c "import json; print(json.load(open('$dir/plugin.json'))['version'])")
            echo "  - $name v$version"
        fi
    done
}

install_plugin() {
    local source=$1
    local name=$(basename "$source" .tar.gz)

    if [[ "$source" == http* ]]; then
        curl -LO "$source"
        tar -xzf "$(basename $source)" -C "$PLUGIN_DIR"
    elif [[ "$source" == *.tar.gz ]]; then
        tar -xzf "$source" -C "$PLUGIN_DIR"
    elif [[ "$source" == *.git ]]; then
        git clone "$source" "$PLUGIN_DIR/$name"
    else
        cp -r "$source" "$PLUGIN_DIR/"
    fi

    echo "Installed: $name"
}

remove_plugin() {
    local name=$1
    rm -rf "$PLUGIN_DIR/$name"
    echo "Removed: $name"
}

case "$1" in
    list)    list_plugins ;;
    install) install_plugin "$2" ;;
    remove)  remove_plugin "$2" ;;
    *)       echo "Usage: $0 {list|install|remove}" ;;
esac
```

## Sharing Plugins

### To GitHub
```bash
# Create plugin repo
git init my-plugin
cd my-plugin
# Add plugin files...
git add -A
git commit -m "Initial plugin"
git remote add origin git@github.com:user/my-plugin.git
git push -u origin main
```

### To Marketplace
```bash
# Package for distribution
./plugin-manager.sh package my-plugin

# Upload to marketplace (when available)
# curl -X POST https://marketplace.example.com/plugins \
#   -F "plugin=@my-plugin-1.0.0.tar.gz"
```

## Plugin Templates

### New Module Template
```python
# templates/new-module.py
"""{{ module_name }} - {{ description }}

{{ long_description }}
"""

from typing import Optional, List
from dataclasses import dataclass


@dataclass
class {{ class_name }}:
    """{{ class_description }}"""

    {{ field }}: {{ type }}

    def {{ method }}(self) -> {{ return_type }}:
        """{{ method_description }}"""
        pass


def {{ function }}({{ params }}) -> {{ return_type }}:
    """{{ function_description }}"""
    pass
```

### New Test Template
```python
# templates/new-test.py
"""Tests for {{ module_name }}"""

import pytest
from core.{{ module_name }} import {{ class_name }}


class Test{{ class_name }}:
    """Test suite for {{ class_name }}"""

    def test_{{ method }}_basic(self):
        """Test {{ method }} with basic input"""
        pass

    def test_{{ method }}_edge_case(self):
        """Test {{ method }} with edge case"""
        pass

    def test_{{ method }}_error(self):
        """Test {{ method }} error handling"""
        pass
```

## Rules

- Each plugin must have a manifest (plugin.json)
- Plugins must be self-contained
- Don't modify core files through plugins
- Test plugins before sharing
- Version plugins semantically
- Document plugin usage in README.md
