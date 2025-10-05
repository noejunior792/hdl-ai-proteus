# 📚 HDL AI Proteus Documentation

Welcome to the comprehensive documentation for HDL AI Proteus - the modular API for generating HDL code from natural language using AI providers.

## 📋 Documentation Index

### 🚀 Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Step-by-step setup with virtual environment and first HDL generation
- **[Configuration Guide](CONFIGURATION.md)** - AI provider setup, environment variables, and security best practices

### 📖 Usage and Integration
- **[Examples & Usage Patterns](EXAMPLES.md)** - Comprehensive integration examples for web, CLI, and Python
- **[Complete API Documentation](DOCS.md)** - Full API reference with all endpoints and parameters
- **[API Context for Developers](api_context.json)** - Machine-readable API specification

### 🔧 Support and Maintenance
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues, debugging, and FAQ

## 🎯 Quick Navigation

### For First-Time Users
1. Start with **[Quick Start Guide](QUICK_START.md)** for setup and virtual environment
2. Follow **[Configuration Guide](CONFIGURATION.md)** to set up your AI provider
3. Try the examples in **[Examples Guide](EXAMPLES.md)**

### For Developers
1. Review **[API Documentation](DOCS.md)** for complete endpoint reference
2. Use **[API Context](api_context.json)** for frontend/backend integration
3. Check **[Examples Guide](EXAMPLES.md)** for integration patterns

### For Troubleshooting
1. Check **[Troubleshooting Guide](TROUBLESHOOTING.md)** for common issues
2. Enable debug logging as described in the troubleshooting guide
3. Review configuration in **[Configuration Guide](CONFIGURATION.md)**

## 📁 Documentation Structure

```
docs/
├── README.md              # This file - documentation index
├── QUICK_START.md         # Setup and virtual environment guide
├── CONFIGURATION.md       # Provider setup and environment config
├── EXAMPLES.md           # Comprehensive usage examples
├── DOCS.md              # Complete API reference
├── TROUBLESHOOTING.md   # Common issues and solutions
└── api_context.json     # Machine-readable API specification
```

## 🔗 Related Resources

- **[Main README](../README.md)** - Project overview and basic setup
- **[Examples Directory](../examples/)** - Practical example files
- **[Commands Reference](../COMMANDS.md)** - Available make commands
- **[Environment Template](../env.template)** - Environment variable template

## 🆘 Need Help?

1. **Common Issues**: Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. **Setup Problems**: Review [Quick Start Guide](QUICK_START.md)
3. **Provider Issues**: See [Configuration Guide](CONFIGURATION.md)
4. **Integration Help**: Check [Examples Guide](EXAMPLES.md)
5. **API Reference**: See [API Documentation](DOCS.md)

## 📖 Documentation Overview

### Quick Start Guide
Essential setup instructions including virtual environment creation, dependency installation, and your first HDL generation. Perfect for getting up and running quickly.

### Configuration Guide
Comprehensive guide to setting up AI providers (Azure OpenAI, OpenAI, Google Gemini), environment variables, security best practices, and advanced configuration options.

### Examples & Usage Patterns
Detailed examples showing how to integrate the API into various environments:
- Web frontend integration with JavaScript
- Command-line usage with cURL and shell scripts
- Python client library with error handling
- Batch processing and workflow automation

### API Documentation
Complete reference for all API endpoints, request/response formats, error codes, and configuration options. Essential for developers building integrations.

### Troubleshooting Guide
Comprehensive troubleshooting resource covering:
- Installation and setup issues
- Virtual environment problems
- Provider authentication failures
- HDL generation and compilation errors
- Performance optimization
- Debug logging and diagnostics

## 🎯 Quick Tips

- **Always activate your virtual environment** before running the API
- **Test provider connection first** using the `/test-provider` endpoint
- **Use `--fail` flag with cURL** to avoid saving error responses
- **Start with simple prompts** and gradually increase complexity
- **Check logs** for detailed error information

---

**Happy HDL generation! 🎉**