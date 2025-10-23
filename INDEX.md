# 📦 Streamlit Automarking System v2.0 - Complete Package

## 📋 Package Contents

This package contains everything you need to run the automatic essay marking system.

### 🚀 Core Files

1. **streamlit_automarking.py** (18 KB)
   - Main application file
   - Run this to start the system
   - Contains all the UI and AI logic

2. **requirements.txt** (53 bytes)
   - Python dependencies
   - Use with: `uv pip install -r requirements.txt`

3. **.env.example** (290 bytes)
   - Environment variable template
   - Copy to `.env` and customize
   - Contains AWS Bedrock configuration

### 📖 Documentation Files

4. **README.md** (5.9 KB)
   - **START HERE** - Complete documentation
   - Installation instructions
   - Configuration guide
   - Troubleshooting tips
   - Usage examples

5. **UPDATE_SUMMARY.md** (6.6 KB)
   - What's new in version 2.0
   - Feature comparison with v1.0
   - Migration guide
   - Technical improvements

6. **QUICK_REFERENCE.md** (8.4 KB)
   - Quick start guide
   - Workflow diagrams (ASCII art)
   - Command cheat sheet
   - Common mistakes to avoid
   - Pro tips

### 🎯 Configuration Files

7. **feedback_guidance.md** (1.6 KB)
   - **IMPORTANT**: Upload this file in the app
   - Instructs the AI on feedback structure
   - Defines tone and formatting
   - Customizable for your needs

## 🎬 Getting Started (30 seconds)

### Step 1: Install Dependencies
```bash
uv pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your AWS_REGION
```

### Step 3: Run the App
```bash
uv run streamlit run streamlit_automarking.py --server.port 8087
```

That's it! The app will open in your browser.

## 📚 Which File to Read First?

```
New User?
    ↓
START → README.md (full setup guide)
    ↓
    ↓
Want quick start?
    ↓
    → QUICK_REFERENCE.md (visual guide + commands)
    ↓
    ↓
Upgrading from v1.0?
    ↓
    → UPDATE_SUMMARY.md (what's new)
    ↓
    ↓
Ready to run!
    ↓
    → streamlit_automarking.py
```

## 🎯 Feature Highlights

✅ Upload multiple student essays at once
✅ Use custom rubrics (upload .md files)
✅ AI-powered feedback generation
✅ Batch processing with progress tracking
✅ Individual student feedback (Tab 2)
✅ Class-level analysis (Tab 3)
✅ Download all feedback files
✅ Automatic file saving to outputs/

## 📁 Directory Structure After Setup

```
your-project/
├── streamlit_automarking.py    # Main app
├── requirements.txt            # Dependencies
├── .env                        # Your config (you create)
├── .env.example                # Template
├── feedback_guidance.md        # AI instructions
├── README.md                   # Documentation
├── UPDATE_SUMMARY.md           # What's new
├── QUICK_REFERENCE.md          # Quick guide
│
├── essays/                     # Your essay files (you provide)
│   ├── student1.txt
│   ├── student2.txt
│   └── ...
│
├── rubrics/                    # Your rubric files (you provide)
│   ├── rubric1.md
│   └── ...
│
└── outputs/                    # Generated files (auto-created)
    ├── student1.feedback.txt
    ├── student2.feedback.txt
    └── class_overall.feedback.md
```

## 🔑 Key Concepts

### Input Files (You Upload in App)
- **Essays**: `.txt` files with student work
- **Rubrics**: `.md` files with grading criteria
- **Guidance**: `feedback_guidance.md` (provided)

### Output Files (Auto-Generated)
- **Individual**: `{name}.feedback.txt` for each essay
- **Class**: `class_overall.feedback.md` for whole class
- **Location**: `outputs/` directory

### Three Tabs
1. **Upload & Marking**: Upload files and start processing
2. **Individual Feedback**: Review per-student feedback
3. **Class Feedback**: View overall class analysis

## ⚙️ System Requirements

- **Python**: 3.8 or higher
- **AWS**: Bedrock access with Claude Sonnet 4
- **OS**: Windows, macOS, or Linux
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## 📝 Configuration Required

Before first run, you need:

1. ✅ AWS Account with Bedrock enabled
2. ✅ AWS credentials configured
3. ✅ Claude Sonnet 4 model access
4. ✅ `.env` file created from `.env.example`

See README.md for detailed instructions.

## 🆘 Quick Troubleshooting

| Problem | Solution | File to Check |
|---------|----------|---------------|
| Can't start app | Install deps | requirements.txt |
| AWS error | Check config | .env |
| No feedback | Upload guidance | feedback_guidance.md |
| Wrong format | Use .txt/.md | README.md |
| Timeout | Increase timeout | streamlit_automarking.py |

## 💡 Pro Tips

1. **Read README.md first** for complete setup
2. **Use QUICK_REFERENCE.md** for visual guides
3. **Keep feedback_guidance.md** ready to upload
4. **Test with 2-3 essays** before full batch
5. **Check outputs/ folder** for generated files

## 📊 File Size Reference

| File | Size | Type |
|------|------|------|
| streamlit_automarking.py | 18 KB | Python |
| README.md | 5.9 KB | Markdown |
| UPDATE_SUMMARY.md | 6.6 KB | Markdown |
| QUICK_REFERENCE.md | 8.4 KB | Markdown |
| feedback_guidance.md | 1.6 KB | Markdown |
| requirements.txt | 53 B | Text |
| .env.example | 290 B | Text |
| **Total** | **~41 KB** | - |

## 🎓 Example Workflow

```
1. Install dependencies (1 minute)
2. Configure .env file (1 minute)
3. Run streamlit app (10 seconds)
4. Upload 5 essays in Tab 1 (30 seconds)
5. Upload rubric and guidance (20 seconds)
6. Click "Start Marking" (1 click)
7. Wait for processing (2-3 minutes)
8. Review feedback in Tab 2 (5 minutes)
9. Check class analysis in Tab 3 (2 minutes)
10. Download all files (1 minute)

Total time: ~15 minutes for 5 essays
```

## 📦 What's Included vs. What You Need

### ✅ Included in This Package
- Application code
- Documentation
- Configuration templates
- Feedback guidance
- Requirements list

### 📝 You Need to Provide
- Student essays (.txt files)
- Grading rubrics (.md files)
- AWS Bedrock access
- AWS credentials

## 🚀 Next Steps

1. **Read README.md** - Understand the system
2. **Follow setup instructions** - Get it running
3. **Test with sample essays** - Verify it works
4. **Process your essays** - Run the marking
5. **Review and download** - Get your results

## 📞 Support Resources

- **Full Documentation**: README.md
- **Quick Start**: QUICK_REFERENCE.md
- **What's New**: UPDATE_SUMMARY.md
- **Streamlit Docs**: https://docs.streamlit.io/
- **AWS Bedrock**: https://docs.aws.amazon.com/bedrock/

## 🎯 Success Checklist

Before running, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (requirements.txt)
- [ ] .env file created and configured
- [ ] AWS credentials set up
- [ ] Claude Sonnet 4 access enabled
- [ ] Student essays ready (.txt format)
- [ ] Rubric files ready (.md format)
- [ ] feedback_guidance.md available

## 🏆 You're Ready!

All files are in place. Follow README.md for detailed setup, or use QUICK_REFERENCE.md for a fast start.

**Command to run:**
```bash
streamlit run streamlit_automarking.py --server.port 8087
```

Good luck with your essay marking! 🎓

---

**Version**: 2.0  
**Author**: Updated with AI assistance  
**License**: Educational use  
**Support**: See documentation files
