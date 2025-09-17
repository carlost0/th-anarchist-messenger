# The Anarchist Messenger

- **Decentralized**: each user runs their own server

- **End-to-end encrypted** and secure connections

- **No central server** → effectively immune to EU Chat Control

- **Private messages fully** under user control

# Install guide
## Linux:
1. **Install Dependencies:**
  - Git:
    - On Arch: `sudo pacman -S git`
    - On Ubuntu/Debian: `sudo apt install git`
  - Python:
    - On Arch: `sudo pacman -S python3`
    - On Ubuntu/Debian: `sudo apt install python3`
  - Python packages: `pip install json5 cryptography`
2. **Clone the repo:**
  - `git clone https://github.com/carlost0/th-anarchist-messenger.git`
3. **Setup:**
    - TSL:
      - Go into the setup directory (`cd th-anarchist-messenger/setup`)
      - Run your tsl_setup script: `chmod +x tsl_setup.sh; ./tsl_setup.sh` when on bash/zsh, `chmod +x tsl_setup.fish; ./tsl_setup.fish` when on fish
    - User configuration: Open `config/config.json`, further instructions are provided there
    - Contacts:
        1. Make a `*contact name*.json` file in the `/contacts` directory
        2. Follow the `template.json` template
    - E2EE:
        - When you run `main.py` you are going to be asked if you know your encryption key, if you don't have the key as an enviroment variable and if you're on zsh/bash, then add the provided line to your shell config (`~/.bashrc` on bash and `~/.zshrc` on zsh)
        - If you are on fish, then you add: `set -x CHAT_SECRET_KEY "*your key*"` to your fish config (/.config/fish/config.fish)
---
**You can now run the messenger with `python3 src/main.py`**
