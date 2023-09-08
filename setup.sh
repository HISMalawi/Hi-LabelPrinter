#!/bin/bash
echo "✨️ Starting printer configurations setup..."
sudo rm -rf build
sudo rm -rf dist
sudo rm -rf env
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

if [ -f "$install_dir/$script_name" ]; then
   echo "$script_name is already installed."
else
   cp "./dist/$script_name" "$install_dir/"

   chmod +x "$install_dir/$script_name"

   echo "$script_name has been installed in $install_dir."

   if [[ "$(uname -s)" == "Linux" ]]; then
      service_file="/etc/systemd/system/$script_name.service"

      echo "[Unit]" > "$service_file"
      echo "Description=$script_name" >> "$service_file"
      echo "After=network.target" >> "$`service_file`"
      echo "" >> "$service_file"
      echo "[Service]" >> "$service_file"
      echo "ExecStart=$install_dir/$script_name" >> "$service_file"
      echo "Restart=always" >> "$service_file"
      echo "" >> "$service_file"
      echo "[Install]" >> "$service_file"
      echo "WantedBy=multi-user.target" >> "$service_file"

      systemctl daemon-reload
      systemctl start "$script_name.service"
      systemctl enable "$script_name.service"

      echo "$script_name has been configured to run on startup (systemd)."
   fi
fi
echo "✨️ Setup successfully completed..."
exit 0



