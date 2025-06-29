# LLM Engineering

This directory contains the implementation of Clara's Language Model (LLM) system, which powers the email management and response generation capabilities.

## Architecture

The LLM system is organized into three main components:

### 1. Model Layer (`/model`)
- `gemini_provider.py`: Implements the Gemini AI client integration
  - Handles API authentication and configuration
  - Provides text generation capabilities with customizable parameters
  - Uses Gemini 2.0 Flash Lite model for optimal performance
- `operations.py`: Core LLM operations and business logic

### 2. Infrastructure Layer (`/infrastructure`)
- `prompts.py`: Contains all prompt templates for different use cases:
  - Email classification
  - Email reading and summarization
  - Message generation
  - Message validation
- `schemas/`: Data structures and validation schemas

### 3. Application Layer (`/application`)
- `services.py`: High-level service implementations that coordinate between different components

## Key Features

1. **Email Classification**
   - Categorizes incoming emails into: Alumni, Company, Internal NJIT Partner, or Unrelated
   - Extracts relevant metadata based on classification

2. **Email Processing**
   - Structured email reading and summarization
   - Extracts sender information, purpose, and call-to-action items

3. **Message Generation**
   - Creates formatted WhatsApp messages
   - Includes key action items and maintains consistent formatting

4. **Message Validation**
   - Validates generated messages against source material
   - Provides accuracy scoring and discrepancy analysis
   - Ensures format compliance and completeness

## Setup

1. Ensure you have a valid Gemini API key
2. Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

The LLM system is designed to be used as part of the larger Clara application. It provides the following main functionalities:

1. Email classification and routing
2. Email summarization and structured information extraction
3. Automated response generation
4. Message validation and quality control

For detailed implementation examples, refer to the individual component documentation. 