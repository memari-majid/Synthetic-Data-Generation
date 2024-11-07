# Installation Guide

## System Requirements

### Hardware Requirements
- CPU: Multi-core processor (recommended: 4+ cores)
- RAM: 16GB minimum
- GPU: NVIDIA/AMD GPU with 4GB+ VRAM
- Storage: 50GB+ free space

### Software Requirements
1. **Blender**
   - Version 2.80 or higher (3.0+ recommended)
   - [Download Blender](https://www.blender.org/download/)

2. **Python**
   - Included with Blender
   - No separate installation needed

## Setup Steps

### 1. Install Blender
1. Download Blender from the official website
2. Run the installer
3. Launch Blender to verify installation

### 2. Enable Rigify Add-on
1. Open Blender
2. Go to Edit > Preferences
3. Select Add-ons tab
4. Search for "Rigify"
5. Enable the add-on
6. Save Preferences

### 3. Setup Mixamo Account
1. Visit [Mixamo](https://www.mixamo.com/)
2. Create a free account
3. Verify email

### 4. Install SynFall
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/synfall.git
   ```
2. Navigate to project directory:
   ```bash
   cd synfall
   ```
3. Create necessary directories:
   ```bash
   mkdir -p models/{characters,animations,combined}
   mkdir -p output/{raw,processed}
   ``` 