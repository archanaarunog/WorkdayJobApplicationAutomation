#!/bin/bash
# Quick VS Code restart script to free up memory

echo "🛑 Stopping VS Code..."
killall "Code Helper" 2>/dev/null
killall "Code Helper (Renderer)" 2>/dev/null
killall "Code Helper (Plugin)" 2>/dev/null
killall "Code Helper (GPU)" 2>/dev/null
sleep 2

echo "🧹 Clearing temp cache..."
rm -rf ~/Library/Application\ Support/Code/Cache/* 2>/dev/null
rm -rf ~/Library/Application\ Support/Code/CachedData/* 2>/dev/null

echo "✅ Done! You can now reopen VS Code"
echo "💡 Memory has been freed up"
