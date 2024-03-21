#!/bin/bash
echo "✨️ Starting printer configurations setup..."
sudo rm -rf build
sudo rm -rf dist
sudo rm -rf env
sudo apt-get install python3-venv
env_dir="env"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    python -m venv $env_dir
    source $env_dir/Scripts/activate
    elif [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv $env_dir
    source $env_dir/bin/activate
else
    echo "Unsupported operating system: $OSTYPE"
    exit 1
fi
echo "Virtual environment $env_dir activated."
pip install -r requirements.txt
pyinstaller --onefile main.py

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo."
    exit 1
fi

install_dir="/usr/local/bin"

script_name="main"
service_name="HILabelPrinter"


if [ -f "$install_dir/$service_name" ]; then
    echo "$service_name is already installed."
else
    cp "./dist/$script_name" "$install_dir/"

    mv "$install_dir/$script_name" "$install_dir/$service_name"

    # chmod +x "$install_dir/$script_name"
    chmod +x "$install_dir/$service_name"

    echo "$service_name has been installed in $install_dir."

    if systemctl is-active --quiet "$service_name.service"; then
        echo "Stopping and disabling $service_name.service..."
        systemctl stop "$service_name.service"
        systemctl disable "$service_name.service"

        service_file="/etc/systemd/system/$service_name.service"
        rm -f "$service_file"

        echo "$service_name.service has been removed."
    else
        echo "$service_name.service does not exist."
    fi

    if [[ "$(uname -s)" == "Linux" ]]; then
        service_file="/etc/systemd/system/$service_name.service"
        username=$(logname)

        current_dir=$(pwd)

        echo "[Unit]" > "$service_file"
        echo "Description=$service_name" >> "$service_file"
        echo "After=network.target" >> "$service_file"
        echo "" >> "$service_file"
        echo "[Service]" >> "$service_file"
        echo "ExecStart=$install_dir/$service_name" >> "$service_file"
        echo "WorkingDirectory=$current_dir"  >> "$service_file"
        echo "Restart=always" >> "$service_file"
        echo "User=$username"  >> "$service_file"
        echo "" >> "$service_file"
        echo "[Install]" >> "$service_file"
        echo "WantedBy=multi-user.target" >> "$service_file"

        systemctl daemon-reload
        systemctl enable "$service_name.service"
        systemctl start "$service_name.service"

        echo "$service_name has been configured to run on startup (systemd)."
    fi
fi
echo "✨️ Setup successfully completed..."
exit 0



