# ACI Learning Labs 

## Local Workstation Requirements
The code samples in these labs all leverage Python as the programming language.  In order to run the exercises and code, you'll need to meet the following requirements.  

> Full details on how to setup are included in the Learning Lab Setup Steps.  

1. Python 2.7.12 or higher
1. Python Virtual Environment `pip install virtualenv`
1. [ACI Cobra SDK](http://cobra.readthedocs.io) for Python
1. [ACI Toolkit](http://acitoolkit.readthedocs.io) for Python

> It is highly recommended to install all Python requirements within a virtual environment, and not the default Python environment on your workstation.  

## Sandbox Lab Infrastructure Setup
Also included in this repository are scripts to prepare the DevNet Always On Sandbox for ACI/APIC.  These scripts initialize the APIC Simulator and deploy the tenants and application policy leveraged in the Learning Labs.  To run the baselining scripts:

> Details also included within the Learning Labs themselves

```bash
# Clone down this code repository & enter the setup directory
git clone https://github.com/netengpy/aci-labs.git
cd aci-labs/apic_fabric_setup

# Run the baseline scripts
python baseline.py

```

```bash
# Expected Output
Baselining APIC Simulator for Learning Labs
Setting up Fabric Nodes
Configuring Fabric Policies
Setting up Common Tenant
Setting up Heroes Tenant
Setting up SnV Tenant  
```
