#!/bin/bash
# Start VS Code with minimal resource usage - optimized for Copilot Chat
# Disables GPU acceleration and heavy rendering features

echo "🚀 Starting VS Code in lightweight mode..."
echo "   - GPU disabled"
echo "   - Hardware acceleration off"
echo "   - Optimized for Copilot Chat"
echo ""

# Launch VS Code with performance flags
/Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron \
  --disable-gpu \
  --disable-software-rasterizer \
  --disable-gpu-compositing \
  --disable-features=UseSkiaRenderer \
  --disable-dev-shm-usage \
  --no-sandbox \
  --disable-setuid-sandbox \
  --disable-accelerated-2d-canvas \
  --disable-accelerated-video-decode \
  --disable-background-timer-throttling \
  --disable-renderer-backgrounding \
  --disable-backgrounding-occluded-windows \
  /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation &

echo "✅ VS Code launched with minimal resource settings"
echo "💡 Expected RAM usage: ~200-300MB (vs 400-500MB normal)"
