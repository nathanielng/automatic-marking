# Automatic Essay Marking System (Node.js/Next.js)

A modern web application for automated essay marking using Amazon Bedrock and Claude AI. Built with Next.js, TypeScript, shadcn/ui, and Tailwind CSS.

## Features

- **File Upload Interface**: Upload student essays (.txt), rubrics (.md), and feedback guidance (.md)
- **AI-Powered Marking**: Automated essay marking using Amazon Bedrock Claude models
- **Individual Feedback**: View and download feedback for each student essay
- **Class Analytics**: Generate overall class performance analysis and insights
- **Dark/Light Mode**: Toggle between dark and light themes
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Real-time Progress**: Track marking progress with visual indicators

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui (Radix UI primitives)
- **AI Service**: Amazon Bedrock (Claude models)
- **Icons**: Lucide React
- **Theme**: next-themes

## Prerequisites

- Node.js 18+ and npm
- AWS Account with Bedrock access
- AWS credentials configured (via AWS CLI or environment variables)

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd automarking-web
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env.local
   ```

   Edit `.env.local` and update with your AWS Bedrock settings:
   ```env
   BEDROCK_LARGE_MODEL_ID=global.anthropic.claude-sonnet-4-20250514-v1:0
   BEDROCK_REGION=us-west-2
   ```

4. **Set up AWS credentials**:

   You can configure AWS credentials using one of these methods:

   - **AWS CLI** (recommended):
     ```bash
     aws configure
     ```

   - **Environment variables** in `.env.local`:
     ```env
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     AWS_SESSION_TOKEN=your_session_token  # if using temporary credentials
     ```

## Usage

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production

Build and run the production version:

```bash
npm run build
npm start
```

## How to Use the Application

1. **Upload Files**:
   - Navigate to the "Load & Marking" tab
   - Upload student essays (.txt files)
   - Upload rubrics (.md files)
   - Upload feedback guidance (.md file)

2. **Configure Marking**:
   - Select which rubric to use for marking
   - Click "Start Automatic Marking"

3. **View Results**:
   - **Individual Feedback**: View and download feedback for each student
   - **Class Feedback**: View overall class performance analysis

4. **Toggle Theme**:
   - Click the sun/moon icon in the header to switch between light and dark modes

## Project Structure

```
automarking-web/
├── app/
│   ├── api/
│   │   ├── mark-essay/
│   │   │   └── route.ts          # API endpoint for marking individual essays
│   │   └── class-feedback/
│   │       └── route.ts          # API endpoint for class feedback
│   ├── globals.css               # Global styles and theme variables
│   ├── layout.tsx                # Root layout with theme provider
│   └── page.tsx                  # Main application page
├── components/
│   ├── ui/
│   │   ├── button.tsx            # Button component
│   │   ├── card.tsx              # Card component
│   │   ├── tabs.tsx              # Tabs component
│   │   ├── progress.tsx          # Progress bar component
│   │   ├── select.tsx            # Select dropdown component
│   │   └── textarea.tsx          # Textarea component
│   ├── theme-provider.tsx        # Theme context provider
│   └── theme-toggle.tsx          # Dark/light mode toggle
├── lib/
│   ├── bedrock.ts                # Amazon Bedrock integration
│   └── utils.ts                  # Utility functions
└── package.json
```

## API Endpoints

### POST /api/mark-essay

Mark a single essay.

**Request Body**:
```json
{
  "essayText": "string",
  "essayName": "string",
  "rubricText": "string",
  "feedbackGuidance": "string"
}
```

**Response**:
```json
{
  "feedback": "string"
}
```

### POST /api/class-feedback

Generate class-level feedback.

**Request Body**:
```json
{
  "allFeedbacks": [
    {
      "name": "string",
      "feedback": "string"
    }
  ],
  "rubricText": "string"
}
```

**Response**:
```json
{
  "classFeedback": "string"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BEDROCK_LARGE_MODEL_ID` | Amazon Bedrock model ID | `global.anthropic.claude-sonnet-4-20250514-v1:0` |
| `BEDROCK_REGION` | AWS region for Bedrock | `us-west-2` |

## Differences from Python Version

This Node.js version differs from the original Python Streamlit application in the following ways:

1. **File Loading**: Uses browser file upload instead of loading from local folders
2. **UI Framework**: Next.js with shadcn/ui instead of Streamlit
3. **Theme Support**: Built-in dark/light mode toggle
4. **Client-Side State**: All state management happens in the browser
5. **Modern Stack**: TypeScript, React, and modern web technologies

## Troubleshooting

### AWS Credentials

If you encounter authentication errors:
- Ensure AWS credentials are properly configured
- Verify your AWS account has access to Amazon Bedrock
- Check that the Bedrock model ID is correct for your region

### Build Errors

If you encounter build errors:
```bash
rm -rf .next node_modules
npm install
npm run dev
```

## License

This project is part of the automatic-marking system.

## Related

- Original Python/Streamlit version: `../streamlit_automarking.py`
