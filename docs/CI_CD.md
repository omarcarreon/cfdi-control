# CI/CD Pipeline Documentation

## Overview

The CFDI Control Application uses GitHub Actions for continuous integration and deployment (CI/CD). This pipeline ensures code quality, security, and automated releases.

## Workflow Structure

### 1. Main CI/CD Pipeline (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` branch

**Jobs:**

#### Test Suite
- **Runs on:** Ubuntu Latest
- **Python versions:** 3.11, 3.12
- **Actions:**
  - Install dependencies
  - Run linting (flake8)
  - Check code formatting (black)
  - Run tests with coverage
  - Upload coverage to Codecov

#### Security Scan
- **Runs on:** Ubuntu Latest
- **Actions:**
  - Install security tools (bandit, safety)
  - Run security scans
  - Upload security reports

#### Build Executables
- **Runs on:** Ubuntu, Windows, macOS
- **Triggers:** Only on push to main
- **Actions:**
  - Install PyInstaller
  - Build platform-specific executables
  - Upload build artifacts

#### Create Release
- **Runs on:** Ubuntu Latest
- **Triggers:** Only on push to main
- **Actions:**
  - Download all build artifacts
  - Create GitHub release with executables
  - Tag with version number

### 2. Development Checks (`.github/workflows/dev.yml`)

**Triggers:**
- Pull requests to `main` or `develop`
- Push to `develop`, `feature/*`, `bugfix/*` branches

**Jobs:**

#### Code Quality
- **Actions:**
  - Check code formatting (black, isort)
  - Run linting (flake8)
  - Type checking (mypy)

#### Test Suite
- **Dependencies:** Code Quality job
- **Actions:**
  - Run tests with coverage
  - Upload coverage reports

#### Security Check
- **Actions:**
  - Run security scans (bandit, safety)
  - Upload security reports

#### Dependency Check
- **Actions:**
  - Check for outdated dependencies
  - Check for security vulnerabilities

## Configuration Files

### pyproject.toml
Modern Python project configuration with:
- **Build system:** setuptools
- **Dependencies:** openpyxl, lxml, pydantic
- **Dev dependencies:** pytest, black, flake8, mypy, etc.
- **Tool configurations:** black, isort, mypy, pytest, coverage

### .gitignore
Excludes:
- Python cache files
- Virtual environments
- Build artifacts
- IDE files
- OS-specific files

## Quality Gates

### Code Quality
- **Black formatting:** Enforced code style
- **Flake8 linting:** Code quality checks
- **isort:** Import sorting
- **mypy:** Type checking

### Testing
- **Coverage:** Minimum 80% code coverage
- **Test count:** 44 tests covering all components
- **Integration tests:** Complete workflow validation

### Security
- **Bandit:** Security vulnerability scanning
- **Safety:** Dependency security checks
- **Dependency updates:** Automated outdated dependency detection

## Build Process

### Executable Creation
```bash
# Linux/macOS
pyinstaller --onefile --windowed src/main.py --name cfdi_control

# Windows
pyinstaller --onefile --windowed src/main.py --name cfdi_control.exe
```

### Release Process
1. **Trigger:** Push to main branch
2. **Build:** Create executables for all platforms
3. **Test:** Run full test suite
4. **Security:** Run security scans
5. **Release:** Create GitHub release with artifacts

## Monitoring and Reporting

### Coverage Reports
- **HTML reports:** Available as artifacts
- **XML reports:** For CI integration
- **Terminal output:** Real-time coverage display

### Security Reports
- **Bandit reports:** JSON format for analysis
- **Safety reports:** Dependency vulnerability reports
- **Artifacts:** Available for download

### Test Results
- **JUnit XML:** For CI integration
- **HTML reports:** Detailed test results
- **Console output:** Real-time test progress

## Local Development

### Running Quality Checks
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run formatting
black src/ tests/
isort src/ tests/

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run tests
pytest tests/ -v

# Run security checks
bandit -r src/
safety check
```

### Pre-commit Setup
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files
```

## Troubleshooting

### Common Issues

#### Build Failures
- **Missing dependencies:** Check requirements.txt
- **Platform-specific issues:** Check PyInstaller configuration
- **Permission errors:** Check file permissions

#### Test Failures
- **Import errors:** Check Python path and dependencies
- **File not found:** Check test data files
- **Timeout issues:** Check test performance

#### Security Failures
- **False positives:** Review bandit configuration
- **Dependency issues:** Update requirements.txt
- **Vulnerability reports:** Review safety output

### Debug Mode
```bash
# Run with verbose output
pytest tests/ -v -s

# Run specific test
pytest tests/test_xml_parser.py::TestCFDIXMLParser::test_parse_cfdi_file_valid -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Best Practices

### Code Quality
1. **Format code** before committing
2. **Run tests** locally before pushing
3. **Check type hints** with mypy
4. **Review security** reports regularly

### Development Workflow
1. **Create feature branch** from develop
2. **Make changes** with tests
3. **Run quality checks** locally
4. **Push and create PR**
5. **Wait for CI checks**
6. **Merge after approval**

### Release Process
1. **Merge to main** triggers release
2. **CI builds** executables
3. **Security scans** run
4. **Release created** automatically
5. **Artifacts uploaded** to GitHub

## Metrics and KPIs

### Quality Metrics
- **Test coverage:** >80%
- **Code quality:** No flake8 errors
- **Security:** No high-severity vulnerabilities
- **Build success:** >95%

### Performance Metrics
- **Build time:** <10 minutes
- **Test execution:** <5 minutes
- **Deployment time:** <2 minutes

### Reliability Metrics
- **Build success rate:** >95%
- **Test pass rate:** >98%
- **Release frequency:** Weekly
- **Bug detection:** <24 hours

## Future Enhancements

### Planned Improvements
1. **Automated dependency updates** with Dependabot
2. **Performance testing** in CI
3. **Automated documentation** generation
4. **Docker containerization** for builds
5. **Multi-platform testing** matrix expansion

### Monitoring Enhancements
1. **Real-time notifications** for failures
2. **Performance dashboards** for metrics
3. **Automated rollback** capabilities
4. **A/B testing** infrastructure 