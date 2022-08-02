# How to deploy:

## Create development environment
See [Getting Started With the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
for additional details and prerequisites

### Clone the code
```bash
git clone https://github.com/Kuba-L/cn.git
cd cn/cdk
```

### Create Python virtual environment and install the dependencies
```bash
python3.7 -m venv .venv
source .venv/bin/activate

$ pip install -r requirements.txt
```

### deploy 
```bash
git clone https://github.com/Kuba-L/cn.git
cd cn/cdk

cdk deploy --all
```

### How to connect to existing
link goes here

### R53 part
R53 part commented out.
ALB, SG not adjusted for HTTPS, no certificates etc.
