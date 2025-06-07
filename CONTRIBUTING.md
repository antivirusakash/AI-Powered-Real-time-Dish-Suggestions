# Contributing to AI Powered Real-time Dish Suggestions

First off, thank you for considering contributing to AI Powered Real-time Dish Suggestions! 🎉

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Node.js version, browser)

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and which behavior you expected to see**
- **Explain why this enhancement would be useful**

### 🔧 Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test your changes thoroughly**
5. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
6. **Push to the branch** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python (3.7 or higher)
- pip3
- Azure OpenAI access with GPT 4.1 Nano deployment

### Local Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/ai-powered-dish-suggestions.git
   cd ai-powered-dish-suggestions
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

4. **Start the development server**:
   ```bash
   python3 app.py
   ```

## Coding Standards

### JavaScript Style Guide

- Use **ES6+ features** where appropriate
- Use **const** for variables that don't change, **let** for variables that do
- Use **arrow functions** for short functions
- Add **comments** for complex logic
- Keep functions **small and focused**
- Use **meaningful variable and function names**

### Code Examples

**Good**:
```javascript
// Calculate debounced search with user input validation
const handleUserInput = (inputText) => {
    if (!inputText || inputText.length < 2) {
        return [];
    }
    
    return debouncedSearch(inputText);
};
```

**Avoid**:
```javascript
function func(x) {
    if (x && x.length >= 2) return search(x);
    return [];
}
```

### CSS Guidelines

- Use **BEM methodology** for class naming
- Keep **responsive design** in mind
- Use **CSS custom properties** for theming
- Maintain **consistent spacing** and typography

### Commit Messages

- Use the **present tense** ("Add feature" not "Added feature")
- Use the **imperative mood** ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to **72 characters or less**
- Reference issues and pull requests liberally after the first line

**Examples**:
```
Add real-time format detection for user input

- Implement regex patterns for common food formats
- Add unit tests for format detection
- Update documentation with new examples

Fixes #123
```

## Project Structure

```
ai-powered-dish-suggestions/
├── app.py              # Flask backend with Azure OpenAI
├── index.html          # Main frontend HTML
├── style.css           # Responsive CSS styling
├── script.js           # Frontend JavaScript logic
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # Project documentation
└── CONTRIBUTING.md     # This file
```

## Testing

### Manual Testing

Before submitting a PR, please test:

1. **Basic functionality**:
   - Type various food items and check suggestions
   - Test with different portion formats
   - Verify keyboard navigation works

2. **Edge cases**:
   - Very short inputs (< 2 characters)
   - Very long inputs
   - Special characters and emojis
   - Network failures

3. **UI/UX**:
   - Test on different screen sizes
   - Check loading states
   - Verify error messages are clear

### Automated Testing

Currently, the project relies on manual testing. We welcome contributions to add:
- Unit tests for utility functions with pytest
- Integration tests for Flask API endpoints
- Frontend testing with tools like Selenium or Playwright

## Feature Development Guidelines

### New Features Should:

- **Be backward compatible** when possible
- **Include comprehensive documentation**
- **Handle error cases gracefully**
- **Maintain the existing UI/UX patterns**
- **Be tested across different browsers**

### AI Prompt Modifications

When modifying the AI prompts:

- **Test thoroughly** with various inputs
- **Ensure Azure OpenAI compliance** (avoid content filter issues)
- **Maintain format consistency** across suggestions
- **Document prompt changes** in your PR description

## Questions?

Don't hesitate to ask questions in:
- **GitHub Issues** for bugs and feature requests
- **GitHub Discussions** for general questions
- **Pull Request comments** for code-specific questions

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- GitHub's contributor graph

Thank you for helping make AI Powered Real-time Dish Suggestions better! 🚀 