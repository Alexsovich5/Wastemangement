#!/bin/bash
# Cleanup script for ERPNext Medical Waste Management project
# Removes temporary files and organizes development artifacts

echo "🧹 Cleaning up project directory..."

# Remove common temporary files
echo "Removing temporary files..."
rm -f *.tmp *.log *.pid
rm -rf __pycache__/ *.pyc

# Clean up Docker artifacts (optional)
echo "Cleaning up Docker artifacts..."
docker system prune -f 2>/dev/null || echo "Docker cleanup skipped (not running)"

# Remove node modules if not needed for testing
if [ "$1" = "--deep" ]; then
    echo "Deep cleanup: removing node_modules..."
    rm -rf node_modules/
    echo "Run 'npm install' to restore testing dependencies if needed"
fi

# Create logs directory if it doesn't exist
mkdir -p logs/

echo "✅ Cleanup completed!"
echo "Project structure:"
echo "  📁 setup/scripts/     - Setup and installation scripts"
echo "  📁 docs/              - Documentation and guides"
echo "  📁 temp_files/        - Development and test files"
echo "  📁 logs/              - System logs (if any)"
echo ""
echo "Use './cleanup.sh --deep' for thorough cleanup including dependencies"