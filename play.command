DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT_PATH="$DIR/code/human_v_bot.py"

# Check if python3 is in the PATH
if command -v python3 &> /dev/null
then
    echo "python3 found, launching script in a new terminal"
    python3 "$PYTHON_SCRIPT_PATH"
    exit 0
fi

# Check if python is in the PATH
if command -v python &> /dev/null
then
    echo "python found, launching script in a new terminal"
    python "$PYTHON_SCRIPT_PATH"
    exit 0
fi

echo "ERROR: python cannot be found!"
exit 1