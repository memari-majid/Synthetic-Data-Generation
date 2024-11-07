# Troubleshooting Guide

## Common Issues

### 1. Import Errors
**Problem**: Cannot import 'bpy' module
**Solution**: 
- Run script through Blender
- Use correct Python version

### 2. Model Loading Issues
**Problem**: FBX files not loading
**Solution**:
- Check file paths
- Verify FBX format
- Update Blender

### 3. Rendering Problems
**Problem**: Slow or failed rendering
**Solution**:
- Enable GPU rendering
- Reduce resolution
- Check memory usage

## Error Messages

### Common Error Messages and Solutions

1. **"No module named 'bpy'"**
   - Run script through Blender
   - Don't use external Python

2. **"Cannot find file"**
   - Check file paths
   - Verify file existence
   - Use absolute paths

3. **"Out of memory"**
   - Reduce batch size
   - Lower resolution
   - Close other applications 