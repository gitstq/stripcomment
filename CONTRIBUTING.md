# Contributing to StripComment

Thank you for your interest in contributing to StripComment! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Report Bugs** - Submit issues for any bugs you find
- **Suggest Features** - Share your ideas for new features
- **Submit Pull Requests** - Contribute code improvements
- **Improve Documentation** - Help make our docs better
- **Add Language Support** - Add support for new programming languages

## 🐛 Reporting Bugs

Before submitting a bug report, please:

1. Check if the issue has already been reported
2. Use the latest version of StripComment
3. Provide a clear description of the problem
4. Include steps to reproduce the issue
5. Share sample code if applicable

## 💡 Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature has already been suggested
2. Provide a clear description of the feature
3. Explain why this feature would be useful
4. Include examples if possible

## 🔧 Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/stripcomment.git
cd stripcomment

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black src tests
isort src tests
mypy src
```

## 📝 Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes using conventional commits:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
7. Push to your branch
8. Open a Pull Request

## 📋 Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

## ✅ Testing

- Write unit tests for all new functionality
- Ensure all existing tests pass
- Aim for high test coverage
- Use pytest fixtures for common test setup

## 📚 Adding New Language Support

To add support for a new programming language:

1. Add the language configuration to `src/stripcomment/languages.py`
2. Include test cases in `tests/test_core.py`
3. Update the README with the new language
4. Submit a Pull Request

Example language configuration:

```python
"new_language": LanguageConfig(
    name="New Language",
    extensions={".nl"},
    single_line=["#"],
    multi_line=[("/*", "*/")],
),
```

## 🤝 Code of Conduct

Be respectful and inclusive. We welcome contributions from everyone.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
