# University Network Login Script - UNLS
![Showcase](/img/showcase.png)

## Usage
Finally, to execute the program, 
you may use `UNLS_DEBUG=1` environment variable to enable debug messages
```bash
UNLS_DEBUG=1 unls
```

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
*Note 2: you can set the env var `UNLS_DEBUG=1` to show extra info while installing*

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

## How does it work?
It first checks the dependencies on runtime, then the current active network, 
to guarantee that the environment is setup properly. Then, it gets your encrypted credentials, starts a webdriver, 
connects to the website provided and searches for a form that contains an id equivalent to password, 
fills it with your credentials and submits it!

This way, it should be mostly independent and work for a majority of cases and different universities.

## Recommendation
Personally, I run this script manually whenever I need it, 
but it might be best to add it into an autostart script of some sort.

## Development
For some info on development status, [click here](/docs/DEVELOPMENT.md).

# License
This program is [MIT](/LICENSE) licensed.
