# Quick Reference Guide

## 📁 File Structure

```
streamlit_automarking.py    # Main application
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── UPDATE_SUMMARY.md       # What's new in v2.0
├── .env.example            # Environment template
├── feedback_guidance.md    # AI feedback instructions
│
├── [Your Files]
│   ├── essay1.txt          # Student essays (you upload)
│   ├── essay2.txt
│   ├── rubric1.md          # Grading rubrics (you upload)
│   └── ...
│
└── outputs/                # Generated files (auto-created)
    ├── essay1.feedback.txt
    ├── essay2.feedback.txt
    └── class_overall.feedback.md
```

## 🔄 Workflow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                   TAB 1: Upload & Marking                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Upload Essays        2. Upload Rubric                    │
│     ┌─────────┐             ┌─────────┐                      │
│     │ essay1  │             │rubric1  │                      │
│     │ essay2  │   ────►     │rubric2  │                      │
│     │ essay3  │             └─────────┘                      │
│     └─────────┘                                              │
│          │                        │                          │
│          └────────┬───────────────┘                          │
│                   ▼                                          │
│  3. Upload Feedback Guidance                                 │
│     ┌──────────────────────┐                                 │
│     │feedback_guidance.md  │                                 │
│     └──────────────────────┘                                 │
│                   │                                          │
│                   ▼                                          │
│  4. Click "Start Automatic Marking"                          │
│     ┌──────────────────────┐                                 │
│     │   🚀 Start Marking   │                                 │
│     └──────────────────────┘                                 │
│                   │                                          │
│                   ▼                                          │
│         ┌─────────────────┐                                  │
│         │  AI Processing   │                                 │
│         │   (Claude AI)    │                                 │
│         └─────────────────┘                                  │
│                   │                                          │
│                   ▼                                          │
│         ┌─────────────────┐                                  │
│         │ Generate Files   │                                 │
│         │  in outputs/     │                                 │
│         └─────────────────┘                                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│               TAB 2: Individual Feedback                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Select Student: [Dropdown ▼]                                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Feedback for: essay1.txt                               │  │
│  │                                                        │  │
│  │ Band Level: 5 (17-20 points)                           │  │
│  │                                                        │  │
│  │ Strengths:                                             │  │
│  │ - Excellent vocabulary                                 │  │
│  │ - Clear structure                                      │  │
│  │                                                        │  │
│  │ Areas for Improvement:                                 │  │
│  │ - Add more examples                                    │  │
│  │                                                        │  │
│  │ [⬇️ Download Feedback]                                 │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                TAB 3: Class Feedback                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Class Performance Analysis                             │  │
│  │                                                        │  │
│  │ Overall Performance Summary                            │  │
│  │ - Band 5: 2 students (20%)                             │  │
│  │ - Band 4: 5 students (50%)                             │  │
│  │ - Band 3: 3 students (30%)                             │  │
│  │                                                        │  │
│  │ What Went Well ✓                                       │  │
│  │ - Strong vocabulary usage across class                 │  │
│  │ - Good understanding of essay structure                │  │
│  │                                                        │  │
│  │ Areas for Improvement ⚠️                               │  │
│  │ - Need more specific examples                          │  │
│  │ - Some grammar inconsistencies                         │  │
│  │                                                        │  │
│  │ Recommendations for Next Steps 🎯                      │  │
│  │ - Focus on example integration                         │  │
│  │ - Grammar review exercises                             │  │
│  │                                                        │  │
│  │ [⬇️ Download Analysis]                                 │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## ⚡ Quick Commands

### Setup (One-time)
```bash
# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AWS region
```

### Run Application
```bash
streamlit run streamlit_automarking.py --server.port 8087
```

### Alternative Run (Auto-reload on save)
```bash
streamlit run streamlit_automarking.py --server.port 8087 --server.runOnSave true
```

## 🎯 Key Features at a Glance

| Feature           | Description             | Location |
|-------------------|-------------------------|----------|
| Upload Essays     | Multiple .txt files     | Tab 1    |
| Upload Rubrics    | Multiple .md files      | Tab 1    |
| Preview Files     | Dropdown selectors      | Tab 1    |
| Start Marking     | One-click batch process | Tab 1    |
| View Feedback     | Individual student feedback | Tab 2|
| Download Feedback | Export individual files | Tab 2    |
| Class Analysis    | Overall performance report | Tab 3 |
| Download Analysis | Export class report     | Tab 3    |

## 📝 File Naming Conventions

### Input Files (Your Files)
- Essays: `studentname.txt` or `essay1.txt`
- Rubrics: `rubric1.md` or `assignment1_rubric.md`
- Guidance: `feedback_guidance.md` (provided)

### Output Files (Generated)
- Individual: `{essay_name}.feedback.txt`
- Class: `class_overall.feedback.md`
- Location: `outputs/` directory (auto-created)

## 🔍 What Each File Does

### streamlit_automarking.py
- Main application code
- Handles UI, file uploads, AI processing
- Manages three-tab interface

### requirements.txt
- Lists all Python dependencies
- Use with `uv pip install` or `pip install`

### feedback_guidance.md
- Instructions for the AI
- Defines feedback structure
- Sets tone and style

### .env (you create from .env.example)
- Environment variables
- AWS configuration
- Credentials (keep secure!)

### README.md
- Complete documentation
- Setup instructions
- Troubleshooting guide

### UPDATE_SUMMARY.md
- What's new in v2.0
- Feature comparison
- Migration guide

## 💡 Pro Tips

1. **Organize Before Upload**
   - Keep essays in one folder
   - Keep rubrics in another
   - Use clear file names

2. **Preview Everything**
   - Check essays after upload
   - Verify rubric content
   - Review guidance file

3. **Start Small**
   - Test with 2-3 essays first
   - Verify output quality
   - Then process full batch

4. **Check Progress**
   - Watch the progress bar
   - Monitor console logs
   - Verify outputs/ folder

5. **Review Before Sharing**
   - Read generated feedback
   - Check for accuracy
   - Customize if needed

## ⚠️ Common Mistakes to Avoid

❌ Forgetting to upload feedback_guidance.md
✅ Upload all three file types before marking

❌ Not configuring .env file
✅ Copy .env.example to .env and edit

❌ Using wrong file formats
✅ Use .txt for essays, .md for rubrics

❌ Not checking AWS credentials
✅ Verify Bedrock access before running

❌ Closing browser during marking
✅ Wait for "Marking complete!" message

## 🎓 Example Usage

```
1. Open terminal
2. cd to project directory
3. Run: streamlit run streamlit_automarking.py --server.port 8087
4. Browser opens automatically
5. Go to Tab 1
6. Upload 5 student essays
7. Upload rubric file
8. Upload feedback_guidance.md
9. Select rubric from dropdown
10. Click "Start Automatic Marking"
11. Wait 2-3 minutes (5 essays × ~30 sec each)
12. Go to Tab 2 to review individual feedback
13. Go to Tab 3 to see class analysis
14. Download all files from outputs/ folder
```

## 📊 Expected Processing Time

| Number of Essays| Approx. Time   |
|-----------------|----------------|
| 1 essay         | ~30 seconds    |
| 5 essays        | ~2-3 minutes   |
| 10 essays       | ~5-6 minutes   |
| 20 essays       | ~10-12 minutes |

*Plus ~30-40 seconds for class feedback generation*

## 🚨 Troubleshooting Quick Fixes

**Problem**: Can't connect to AWS
- **Fix**: Check .env file and AWS credentials

**Problem**: Button disabled
- **Fix**: Upload all three file types (essays, rubric, guidance)

**Problem**: No outputs/ folder
- **Fix**: Folder creates automatically; check permissions

**Problem**: Feedback looks wrong
- **Fix**: Edit feedback_guidance.md to adjust instructions

**Problem**: Timeout error
- **Fix**: Increase read_timeout in code (line 28)

## 📞 Need Help?

1. Check README.md for detailed docs
2. Review UPDATE_SUMMARY.md for features
3. Look at console logs for errors
4. Verify all files are uploaded
5. Test with example files first

---

**Happy Marking! 🎓**
