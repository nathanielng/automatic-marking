# Automatic Essay Marking System

A Streamlit-based application for automated essay marking using AWS Bedrock and Claude AI models.

## Features

- 📤 **Multi-file Upload**: Upload multiple student essays and rubrics
- 🤖 **AI-Powered Marking**: Automatic marking using Claude Sonnet 4
- 📋 **Individual Feedback**: Detailed feedback for each student essay
- 📊 **Class Analytics**: Overall class performance analysis and recommendations
- 💾 **Export Results**: Download feedback files in various formats

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured
- Claude Sonnet 4 model access in AWS Bedrock

## Installation

### Using UV (Recommended)

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```bash
BEDROCK_REGION=us-west-2
```

Ensure your AWS credentials are configured:
- Via `~/.aws/credentials`
- Or environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)

## Usage

### Running the Application

```bash
uv run streamlit run streamlit_automarking.py --server.port 8087 --server.runOnSave true
```

The application will open in your default browser at `http://localhost:8087`

### Workflow

#### Tab 1: Upload & Marking

1. **Upload Student Essays**
   - Click "Upload student essay files (.txt)"
   - Select one or more `.txt` files containing student essays
   - Preview uploaded essays using the dropdown

2. **Upload Rubric**
   - Click "Upload rubric files (.md)"
   - Select rubric markdown files
   - Preview rubric content

3. **Upload Feedback Guidance**
   - Upload the `feedback_guidance.md` file
   - This file guides the AI on how to structure feedback

4. **Start Marking**
   - Select which rubric to use for marking
   - Click "🚀 Start Automatic Marking"
   - Wait for the marking process to complete

#### Tab 2: Individual Feedback

- View detailed feedback for each student
- Select student from dropdown
- Download individual feedback files
- Feedback includes:
  - Band levels and scores
  - Detailed justifications
  - Specific examples from the essay
  - Actionable recommendations

#### Tab 3: Class Feedback

- View overall class performance analysis
- Download class-level report
- Includes:
  - Performance distribution
  - Common strengths and weaknesses
  - Teaching recommendations
  - Next steps for improvement

## File Structure

```
.
├── streamlit_automarking.py    # Main application
├── requirements.txt             # Python dependencies
├── feedback_guidance.md         # Feedback structure guidelines
├── .env                        # Environment variables (create this)
└── outputs/                    # Generated feedback files (auto-created)
    ├── essay1.feedback.txt
    ├── essay2.feedback.txt
    └── class_overall.feedback.md
```

## Example Files

### Essay File Format (*.txt)

Plain text file containing the student's essay:

```
Environmental Conservation: A Multifaceted Imperative

Environmental conservation represents one of the most pressing challenges...
[essay content]
```

### Rubric File Format (*.md)

Markdown file with grading criteria:

```markdown
# ESSAY MARKING RUBRIC

## 1. Content and Relevance
- **Band 5** (17-20 points): The essay addresses all aspects...
- **Band 4** (13-16 points): The essay addresses most aspects...
...
```

## Customization

### Adjusting AI Parameters

In `streamlit_automarking.py`, you can modify:

```python
# Model selection
BEDROCK_LARGE_MODEL_ID = "global.anthropic.claude-sonnet-4-20250514-v1:0"

# Generation parameters
body = {
    "max_tokens": 2048,      # Adjust response length
    "temperature": 0.5,       # Adjust creativity (0.0-1.0)
    "top_k": 250,
    "top_p": 1,
}
```

### Custom Feedback Structure

Edit `feedback_guidance.md` to customize:
- Feedback sections and structure
- Tone and language
- Level of detail
- Focus areas

## Troubleshooting

### Common Issues

**Issue**: AWS Bedrock connection error
- **Solution**: Verify AWS credentials and Bedrock access
- Check that the region in `.env` has Claude Sonnet 4 available

**Issue**: Timeout errors during marking
- **Solution**: Increase timeout in Config: `Config(read_timeout=2000)`

**Issue**: Model not found error
- **Solution**: Verify model ID and ensure you have access to Claude Sonnet 4

### Logging

The application uses Python's logging module. Check console output for detailed logs:

```python
# Logs show:
# - File uploads
# - Marking progress
# - Error messages
# - File save locations
```

## Performance Notes

- Each essay takes ~10-30 seconds to mark (depending on length)
- Class feedback generation takes ~20-40 seconds
- Files are saved to the `outputs/` directory automatically

## Security Considerations

- Never commit `.env` file or AWS credentials
- Ensure student data is handled according to privacy policies
- Review generated feedback before sharing with students
- Use appropriate AWS IAM permissions

## Contributing

To contribute:
1. Test with sample essays
2. Document any changes to the feedback structure
3. Ensure AWS credentials are not exposed
4. Update README with new features

## License

This project is for educational purposes.

## Support

For issues related to:
- **Streamlit**: https://docs.streamlit.io/
- **AWS Bedrock**: https://docs.aws.amazon.com/bedrock/
- **Claude API**: https://docs.anthropic.com/

## Version History

- **v2.0**: Multi-file upload, three-tab interface, class feedback
- **v1.0**: Initial version with basic marking functionality
