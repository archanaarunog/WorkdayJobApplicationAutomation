#!/bin/bash
# Quick cache cleanup script for JAPS project
# Run this whenever VS Code starts lagging

echo "🧹 Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*.pyd" -delete 2>/dev/null || true

echo "🧹 Cleaning macOS files..."
find . -type f -name ".DS_Store" -delete 2>/dev/null || true

echo "🧹 Cleaning Python test cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

echo "🧹 Cleaning log files..."
find . -type f -name "*.log" -delete 2>/dev/null || true

echo "✅ Cache cleanup complete!"
echo ""
echo "💡 To clean VS Code cache, also run:"
echo "   rm -rf ~/Library/Application\ Support/Code/Cache"
echo "   rm -rf ~/Library/Application\ Support/Code/CachedData"
echo ""
