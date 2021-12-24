First check if your python version is up to date using

>>python --version

If not command

>>vim /bin/bashrc

Go into write by pressing i.Add a path for python3

Alias python=’/usr/bin/python3’

Press esc

Enter

>>:w!

To save and than

>>:q!

To exit

check again and version in updated

Check aws version if its not updated than update it.

>>curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

>>unzip awscliv2.zip

Than go to related directory

Open your stack file lambda file is in resources folder

Go to virtual environment

>>source .venv/bin/activate

After that npm  install cdk

>>npm install -g aws-cdk

>>nvm install v16.3.0 && nvm use 16.3.0 && nvm alias default v16.3.0

>>npm install -g aws-cdk

>>export PATH=$PATH:$(npm get prefix)/bin

>>python -m pip install aws-cdk.aws-s3 aws-cdk.aws-lambda

Install requirements

>>python3 -m pip install -r requirements.txt

After this synth the file

>>cdk synth

Than deploy

>>cdk deploy
