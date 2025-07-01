# ERPNext Medical Waste Management - Project Structure

## Directory Organization

```
erpnext-medwaste/
├── README.md                          # Main project documentation
├── CLAUDE.md                          # Development instructions
├── PROJECT-STRUCTURE.md               # This file
├── docker-compose.yml                 # Docker orchestration
├── .env                              # Environment configuration
│
├── setup/                            # Setup and installation scripts
│   ├── scripts/                      # Python setup scripts
│   │   ├── setup_medical_waste.py    # Main consolidated setup script
│   │   ├── setup-item-categories.py  # Item groups and categories
│   │   ├── create-custom-doctypes.py # Custom DocTypes
│   │   ├── setup-stock-module.py     # Stock management setup
│   │   ├── setup-manufacturing-workflows.py # Manufacturing workflows
│   │   ├── setup-buying-module.py    # Buying module configuration
│   │   ├── create-compliance-reports.py # Compliance reporting
│   │   ├── basic_setup.py            # Basic system setup
│   │   ├── setup_commands.py         # Setup command utilities
│   │   └── test_setup.py             # Setup testing
│   └── templates/                    # Configuration templates
│
├── docs/                             # Documentation
│   ├── DEPLOYMENT.md                 # Deployment guide
│   ├── MEDICAL-WASTE-SETUP-GUIDE.md  # Medical waste setup instructions
│   ├── SECURITY-CHECKLIST.md         # Security guidelines
│   ├── dev-plan-ongoing.md           # Development planning
│   ├── docker-issues-ongoing&fixed.md # Docker troubleshooting
│   ├── medical-waste-analysis.md     # System analysis
│   ├── site-capability-report.md     # System capabilities
│   └── screenshots/                  # UI screenshots
│       ├── before-login.png
│       ├── login-page.png
│       └── styled-login.png
│
├── temp_files/                       # Temporary and test files
│   ├── init-erpnext.sh
│   ├── load-env.sh
│   ├── manual-init.sh
│   ├── test-config.sh
│   ├── test-environment-switching.sh
│   ├── test-setup.sh
│   ├── test-site.js
│   ├── test-styling.js
│   ├── validate-ports.sh
│   └── validate-production.sh
│
├── node_modules/                     # Node.js dependencies (testing)
├── package.json                      # Node.js package configuration
├── package-lock.json                 # Node.js lockfile
│
└── Scripts/                          # Main operational scripts
    ├── start.sh                      # Start ERPNext system
    ├── stop.sh                       # Stop ERPNext system
    ├── restart.sh                    # Restart ERPNext system
    ├── logs.sh                       # View system logs
    ├── setup-site.sh                 # Initial site setup
    ├── run-setup.sh                  # Run medical waste setup
    └── fix-site.sh                   # Site repair utilities
```

## Key Files Description

### Core Configuration
- **docker-compose.yml**: Official ERPNext docker setup with medical waste customizations
- **.env**: Environment variables for ports, passwords, and configuration
- **CLAUDE.md**: Development workflow and command reference

### Setup Scripts
- **setup_medical_waste.py**: Main script that creates all medical waste features
- **run-setup.sh**: Shell script to execute all setup scripts in sequence
- Individual setup scripts for modular installation of specific features

### Operational Scripts
- **start.sh/stop.sh/restart.sh**: Basic system management
- **logs.sh**: Real-time log monitoring
- **setup-site.sh**: One-time initial site creation

### Documentation
- Complete documentation for deployment, setup, and troubleshooting
- Screenshots showing UI progress and features
- Security checklists and best practices

## Usage

1. **Initial Setup**: `./start.sh && ./setup-site.sh`
2. **Medical Waste Setup**: `./run-setup.sh`
3. **Daily Operations**: `./start.sh`, `./stop.sh`, `./logs.sh`
4. **Development**: See CLAUDE.md for detailed workflows

## Clean Environment

This organization separates:
- **Production code** (root level)
- **Setup utilities** (setup/ directory)
- **Documentation** (docs/ directory)  
- **Testing/Development** (temp_files/ directory)
- **Dependencies** (node_modules/, package files)

All temporary files and development artifacts are contained in dedicated directories for easy maintenance.