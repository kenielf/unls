# University Network Login Script - UNLS
## Installation/Updates
First, clone the repository with
```bash
git clone "https://github.com/kenielf/unls"
```
And `cd` into the newly created directory

### Guided
Use the handy script included with the software to install it for your user:
```bash
./installer -i
```
*Note: you can add `-f` after the `-i` flag if you're updating or reinstalling the software*  
*Note 2: you can set the env var `UNLS_DEBUG=1` to show extra info while isntalling*

### Manual
Create a virtual environment, 
source it and install the needed requirements:
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Credentials / Preparation
Because of the fact that the folder structure for credentials follows this pattern shown below:
```
./
├── cred/
│├── password
│└── username
├── accepted_ssids
└── login_url
```
*Note: for the sake of this being an installation guide, 
I'll use the folder `~/.secrets/university` for demo, 
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

## Usage
Finally, to execute the program, 
you may use `UNLS_DEBUG=1` environment variable to enable debug messages
```bash
UNLS_DEBUG=1 unls
```

## Recommendation
Personally, I run this script manually whenever I need it, 
but it might be best to add it into an autostart script of some sorts.
