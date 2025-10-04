# Contributing to Auditor Job Posting Agent

Thank you for your interest in contributing to the Auditor Job Posting Agent! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git
- Docker (optional)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/auditor-job-posting-agent.git
   cd auditor-job-posting-agent
   ```

2. **Set up the development environment**
   ```bash
   make setup
   # or manually:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements/backend-requirements.txt
   pip install -r requirements/scraper-requirements.txt
   cd frontend && npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize the database**
   ```bash
   make init-db
   # or: python backend/init_db.py
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   make test
   make lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Coding Standards

#### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use meaningful variable and function names

#### JavaScript/TypeScript
- Follow ESLint configuration
- Use TypeScript for type safety
- Follow React best practices

#### General
- Write clear, descriptive commit messages
- Keep functions small and focused
- Add comments for complex logic
- Update tests when adding new features

### Testing

#### Backend Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_ai_processor.py
```

#### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Code Quality

#### Linting
```bash
# Python
flake8 backend/ scraper/
black backend/ scraper/

# Frontend
cd frontend
npm run lint
```

#### Type Checking
```bash
# Python
mypy backend/ scraper/

# Frontend
cd frontend
npm run type-check
```

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**
   ```bash
   make test
   ```

2. **Check code quality**
   ```bash
   make lint
   ```

3. **Update documentation** if needed

4. **Add/update tests** for new functionality

### Pull Request Template

When creating a pull request, please include:

- **Description**: What changes were made and why
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How the changes were tested
- **Breaking Changes**: Any breaking changes and migration steps
- **Screenshots**: If applicable for UI changes

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Approval** and merge

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Environment**: OS, Python version, Node.js version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots/logs**: If applicable

### Feature Requests

For feature requests, please include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Additional context**: Any other relevant information

## Development Guidelines

### Database Changes

- Always create migrations for schema changes
- Test migrations on sample data
- Document any breaking changes

### API Changes

- Follow RESTful conventions
- Update API documentation
- Consider backward compatibility
- Add proper error handling

### Security

- Never commit API keys or secrets
- Use environment variables for configuration
- Follow security best practices
- Report security issues privately

## Getting Help

- **Documentation**: Check the README and docs/ folder
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the maintainers for sensitive issues

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing! 🎉
