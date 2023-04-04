# University Network Login Script - UNLS
## Installation, Preparation & Usage
First, clone the repository with
```bash
git clone "https://github.com/kenielf/unls"
```

Then, `cd` into the directory that was created and create a virtual environment, 
source it and install the needed requirements:
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Now, since the folder structure for credentials follow this pattern shown below:
```
./
├── cred/
│├── password
│└── username
├── accepted_ssids
└── login_url
```
*Note: for the sake of this being an installation guide, 
I'll use the folder `~/secrets/university` for demo, 
`uni_network` for the ssid, 
`https://university-website/login` for the url. 
You may choose whichever folder you prefer*

You'll need to create the directories and files as such:
```bash
mkdir -p ~/.secrets/university
mkdir ~/.secrets/university/cred
echo "uni_network" > ~/.secrets/university/accepted_ssids
echo "https://university-website/login" > ~/.secrets/university/login_url
echo "username" | gpg -qc > ~/.secrets/university/cred/username
echo "password" | gpg -qc > ~/.secrets/university/cred/password
```

Then, using your favourite shell, 
export the following environment variable in the configuration file:
```bash
export UNI_FLDR="${HOME}/.secrets/university"
```

Finally, to execute the program, 
you may use `UNLS_DEBUG=1` environment variable to enable debug messages
```bash
UNLS_DEBUG=1 ./src/unls
```

## Recommendation
Personally, I run this script manually whenever I need it, 
but it might be best to make it an autostart app in your DE.
