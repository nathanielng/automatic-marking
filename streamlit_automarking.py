#!/usr/bin/env python

"""
Streamlit application for automated essay marking using Amazon Bedrock.

This application provides a web interface for:
- Uploading and managing student essays and rubrics
- Generating AI-powered feedback using Amazon Bedrock Claude models
- Viewing individual student feedback
- Generating class-level analysis and insights
- Downloading feedback reports

The app uses Streamlit for the UI and Amazon Bedrock for AI capabilities.
Essays are processed using Claude models to generate detailed feedback based on
provided rubrics and guidance.

Usage:
    uv run streamlit run streamlit_automarking.py --server.port 8087 --server.runOnSave true

Setup:
    uv pip install boto3 python-dotenv streamlit
"""

import argparse
import boto3
import json
import logging
import os
import streamlit as st

from botocore.config import Config
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Generator, List

# Load environment variables
load_dotenv()

# ----- Logging -----
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ----- Bedrock -----
BEDROCK_LARGE_MODEL_ID = os.getenv('BEDROCK_LARGE_MODEL_ID', 'global.anthropic.claude-sonnet-4-20250514-v1:0')
BEDROCK_SMALL_MODEL_ID = os.getenv('BEDROCK_SMALL_MODEL_ID', 'global.anthropic.claude-haiku-4-5-20251001-v1:0')
BEDROCK_REGION = os.getenv('BEDROCK_REGION', 'us-west-2')

config = Config(read_timeout=1000)
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    config=config,
    region_name=BEDROCK_REGION
)


def invoke_claude_sonnet(prompt, **kwargs):
    """Invoke Claude Sonnet model with a simple prompt"""
    messages = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            }
        ]
    }
    body = {
        "messages": [messages],
        "max_tokens": 2048,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": [
            "\\n\\nHuman:"
        ],
        "anthropic_version": "bedrock-2023-05-31"
    }

    for parameter in ['max_tokens', 'temperature', 'top_k', 'top_p']:
        if parameter in kwargs:
            body[parameter] = kwargs[parameter]

    response = bedrock_runtime.invoke_model(
        modelId=BEDROCK_LARGE_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )
    response_body = json.loads(response.get('body').read())
    content = response_body.get("content", [])
    completion = [c['text'] for c in content if c['type'] == 'text']
    if len(completion) > 0:
        return '\n'.join(completion)
    else:
        return response_body


def invoke_claude_with_response_stream(messages, **kwargs):
    """Invoke Claude model with streaming response"""
    body = {
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": [
            "\\n\\nHuman:"
        ],
        "anthropic_version": "bedrock-2023-05-31"
    }

    for parameter in ['max_tokens', 'temperature', 'top_k', 'top_p']:
        if parameter in kwargs:
            body[parameter] = kwargs[parameter]

    response_stream = bedrock_runtime.invoke_model_with_response_stream(
        modelId=BEDROCK_LARGE_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )
    stream = response_stream.get('body')
    return stream


def bedrock_generator(model_name: str, messages: Dict) -> Generator:
    """Generator for streaming responses from Bedrock"""
    stream = invoke_claude_with_response_stream(messages)
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            chunk_obj = json.loads(chunk.get('bytes').decode())
            if chunk_obj['type'] == 'content_block_delta':
                yield chunk_obj['delta']['text']


def generate_essay_feedback(essay_text: str, essay_name: str, rubric_text: str, 
                            feedback_guidance: str) -> str:
    """Generate feedback for a single essay"""
    prompt = f"""You are an expert educator providing detailed feedback on student essays.

<essay>
{essay_text}
</essay>

<rubric>
{rubric_text}
</rubric>

<feedback_guidance>
{feedback_guidance}
</feedback_guidance>

Based on the essay, rubric, and feedback guidance provided above, generate comprehensive feedback for this student essay. 
Follow the structure and tone guidelines specified in the feedback guidance.

Provide specific band levels, justifications, and actionable recommendations."""

    logger.info(f"Generating feedback for essay: {essay_name}")
    feedback = invoke_claude_sonnet(prompt, max_tokens=3000)
    return feedback


def generate_class_feedback(all_feedbacks: List[Dict[str, str]], rubric_text: str) -> str:
    """Generate overall class feedback based on all individual feedbacks"""
    feedback_summary = "\n\n---\n\n".join([
        f"Essay: {item['name']}\n{item['feedback'][:500]}..." 
        for item in all_feedbacks
    ])
    
    prompt = f"""You are an expert educator analyzing overall class performance on an essay assignment.

<rubric>
{rubric_text}
</rubric>

<individual_feedbacks>
{feedback_summary}
</individual_feedbacks>

Based on the rubric and the individual student feedbacks provided above, generate a comprehensive class-level analysis that includes:

1. **Overall Performance Summary**
   - Distribution of band levels across the class
   - General trends and patterns

2. **What Went Well**
   - Common strengths across multiple students
   - Successful application of concepts
   - Positive patterns observed

3. **Areas for Improvement**
   - Common weaknesses or gaps
   - Recurring issues across multiple essays
   - Misconceptions that need addressing

4. **Recommendations for Next Steps**
   - Specific teaching strategies to address common issues
   - Topics that need re-teaching or reinforcement
   - Suggested activities or exercises for the whole class
   - Differentiation strategies for different performance levels

5. **Positive Observations**
   - Growth areas
   - Promising developments
   - Student engagement indicators

Format the response in clear Markdown with appropriate headings and bullet points."""

    logger.info("Generating class overall feedback")
    class_feedback = invoke_claude_sonnet(prompt, max_tokens=4000)
    return class_feedback


def save_feedback_file(essay_name: str, feedback: str, output_dir: str = "outputs") -> str:
    """Save feedback to a file"""
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(essay_name).stem
    feedback_filename = f"{base_name}.feedback.txt"
    feedback_path = os.path.join(output_dir, feedback_filename)
    
    with open(feedback_path, 'w', encoding='utf-8') as f:
        f.write(feedback)
    
    logger.info(f"Saved feedback to: {feedback_path}")
    return feedback_path


def save_class_feedback(class_feedback: str, output_dir: str = "outputs") -> str:
    """Save class feedback to a file"""
    os.makedirs(output_dir, exist_ok=True)
    class_feedback_path = os.path.join(output_dir, "class_overall.feedback.md")
    
    with open(class_feedback_path, 'w', encoding='utf-8') as f:
        f.write(class_feedback)
    
    logger.info(f"Saved class feedback to: {class_feedback_path}")
    return class_feedback_path


# ----- Streamlit UI -----
st.set_page_config(layout="wide", page_title="Automatic Essay Marking System")
st.title("📝 Automatic Essay Marking System")


def initialize_session_state():
    """Initialize session state variables"""
    if "essay_files" not in st.session_state:
        st.session_state.essay_files = {}
    if "rubric_files" not in st.session_state:
        st.session_state.rubric_files = {}
    if "feedback_guidance" not in st.session_state:
        st.session_state.feedback_guidance = ""
    if "generated_feedbacks" not in st.session_state:
        st.session_state.generated_feedbacks = []
    if "class_feedback" not in st.session_state:
        st.session_state.class_feedback = ""
    if "marking_complete" not in st.session_state:
        st.session_state.marking_complete = False


def load_essays_from_folder(folder_path: str = "essays") -> Dict[str, str]:
    """Load all essay files from the essays folder"""
    essays = {}
    
    if not os.path.exists(folder_path):
        logger.warning(f"Essays folder not found: {folder_path}")
        return essays
    
    txt_files = Path(folder_path).glob("*.txt")
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                essays[file_path.name] = content
                logger.info(f"Loaded essay: {file_path.name}")
        except Exception as e:
            logger.error(f"Error loading essay {file_path.name}: {str(e)}")
    
    return essays


def load_rubrics_from_folder(folder_path: str = "rubric") -> Dict[str, str]:
    """Load all rubric files from the rubric folder"""
    rubrics = {}
    
    if not os.path.exists(folder_path):
        logger.warning(f"Rubric folder not found: {folder_path}")
        return rubrics
    
    md_files = Path(folder_path).glob("*.md")
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                rubrics[file_path.name] = content
                logger.info(f"Loaded rubric: {file_path.name}")
        except Exception as e:
            logger.error(f"Error loading rubric {file_path.name}: {str(e)}")
    
    return rubrics


def load_feedback_guidance(file_path: str = "feedback_guidance.md") -> str:
    """Load feedback guidance from file"""
    if not os.path.exists(file_path):
        logger.warning(f"Feedback guidance file not found: {file_path}")
        return ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"Loaded feedback guidance from: {file_path}")
            return content
    except Exception as e:
        logger.error(f"Error loading feedback guidance: {str(e)}")
        return ""


def tab_upload_and_marking():
    """Tab 1: Load files from folders and perform automatic marking"""
    st.header("📂 Load Files & Run Automatic Marking")
    
    # Instructions for folder structure
    with st.expander("ℹ️ Folder Structure Guide", expanded=False):
        st.markdown("""
        This application automatically loads files from the following folders:
        
        - **`essays/`** - Place all student essay files (.txt) here
        - **`rubric/`** - Place all rubric files (.md) here  
        - **`feedback_guidance.md`** - Place this file in the root directory
        
        Click the "Load/Refresh Files" button below to load or reload files from these folders.
        """)
    
    # Auto-load files button
    col_load1, col_load2, col_load3 = st.columns([1, 2, 1])
    with col_load2:
        if st.button("🔄 Load/Refresh Files from Folders", type="secondary", use_container_width=True):
            # Load essays from essays/ folder
            st.session_state.essay_files = load_essays_from_folder("essays")
            
            # Load rubrics from rubric/ folder
            st.session_state.rubric_files = load_rubrics_from_folder("rubric")
            
            # Load feedback guidance
            guidance = load_feedback_guidance("feedback_guidance.md")
            if guidance:
                st.session_state.feedback_guidance = guidance
            
            if st.session_state.essay_files or st.session_state.rubric_files or st.session_state.feedback_guidance:
                st.success("✓ Files loaded successfully!")
            else:
                st.warning("⚠️ No files found. Please check that essays/ and rubric/ folders exist with files.")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Student Essays")
        
        if not st.session_state.essay_files:
            st.info("ℹ️ No essays loaded. Click 'Load/Refresh Files' to load from `essays/` folder.")
            st.markdown("**Expected:** `essays/*.txt`")
        else:
            st.success(f"✓ {len(st.session_state.essay_files)} essay(s) loaded from `essays/` folder")
            
            # Preview selected essay
            selected_essay = st.selectbox(
                "Select essay to preview:",
                options=list(st.session_state.essay_files.keys()),
                key="essay_preview_select"
            )
            with st.expander("Preview Essay", expanded=False):
                st.text_area(
                    "Essay content:",
                    value=st.session_state.essay_files[selected_essay],
                    height=300,
                    key="essay_preview_area",
                    disabled=True
                )
    
    with col2:
        st.subheader("📋 Rubrics")
        
        if not st.session_state.rubric_files:
            st.info("ℹ️ No rubrics loaded. Click 'Load/Refresh Files' to load from `rubric/` folder.")
            st.markdown("**Expected:** `rubric/*.md`")
        else:
            st.success(f"✓ {len(st.session_state.rubric_files)} rubric(s) loaded from `rubric/` folder")
            
            # Preview selected rubric
            selected_rubric = st.selectbox(
                "Select rubric to preview:",
                options=list(st.session_state.rubric_files.keys()),
                key="rubric_preview_select"
            )
            with st.expander("Preview Rubric", expanded=False):
                st.markdown(st.session_state.rubric_files[selected_rubric])
    
    st.divider()
    
    # Feedback guidance status
    st.subheader("📝 Feedback Guidance")
    if not st.session_state.feedback_guidance:
        st.warning("⚠️ No feedback guidance loaded. Please ensure `feedback_guidance.md` exists in the root folder.")
        st.markdown("**Expected:** `feedback_guidance.md` in root directory")
    else:
        st.success("✓ Feedback guidance loaded from `feedback_guidance.md`")
        with st.expander("Preview Guidance", expanded=False):
            st.markdown(st.session_state.feedback_guidance)
    
    st.divider()
    
    # Select which rubric to use for marking
    selected_rubric_for_marking = None  # Initialize to avoid scope issues
    if st.session_state.rubric_files:
        selected_rubric_for_marking = st.selectbox(
            "Select rubric for marking:",
            options=list(st.session_state.rubric_files.keys()),
            key="marking_rubric_select"
        )
    
    # Start automatic marking button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        can_mark = (len(st.session_state.essay_files) > 0 and 
                   len(st.session_state.rubric_files) > 0 and 
                   st.session_state.feedback_guidance)
        
        if st.button(
            "🚀 Start Automatic Marking",
            type="primary",
            disabled=not can_mark,
            use_container_width=True
        ):
            st.session_state.marking_complete = False
            st.session_state.generated_feedbacks = []
            
            # Safety check: ensure rubric is selected
            if not selected_rubric_for_marking:
                st.error("⚠️ Please select a rubric for marking.")
                return
                
            rubric_text = st.session_state.rubric_files[selected_rubric_for_marking]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_essays = len(st.session_state.essay_files)
            
            for idx, (essay_name, essay_text) in enumerate(st.session_state.essay_files.items()):
                status_text.text(f"Marking essay {idx + 1} of {total_essays}: {essay_name}")
                
                try:
                    feedback = generate_essay_feedback(
                        essay_text,
                        essay_name,
                        rubric_text,
                        st.session_state.feedback_guidance
                    )
                    
                    # Save feedback file
                    feedback_path = save_feedback_file(essay_name, feedback)
                    
                    st.session_state.generated_feedbacks.append({
                        'name': essay_name,
                        'feedback': feedback,
                        'path': feedback_path
                    })
                    
                except Exception as e:
                    st.error(f"Error processing {essay_name}: {str(e)}")
                    logger.error(f"Error processing {essay_name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / total_essays)
            
            # Generate class overall feedback
            status_text.text("Generating class overall feedback...")
            try:
                class_feedback = generate_class_feedback(
                    st.session_state.generated_feedbacks,
                    rubric_text
                )
                st.session_state.class_feedback = class_feedback
                save_class_feedback(class_feedback)
            except Exception as e:
                st.error(f"Error generating class feedback: {str(e)}")
                logger.error(f"Error generating class feedback: {str(e)}")
            
            status_text.text("✓ Marking complete!")
            st.session_state.marking_complete = True
            st.success(f"✓ Successfully marked {total_essays} essay(s) and generated class feedback!")
            st.balloons()
    
    if not can_mark:
        st.info("ℹ️ Please load essays, rubric, and feedback guidance using the button above to start marking.")


def tab_individual_feedback():
    """Tab 2: View individual feedback files"""
    st.header("📋 Individual Student Feedback")
    
    if not st.session_state.generated_feedbacks:
        st.info("ℹ️ No feedback generated yet. Please run automatic marking first.")
        return
    
    st.success(f"✓ {len(st.session_state.generated_feedbacks)} feedback file(s) available")
    
    # Select feedback to view
    feedback_names = [f['name'] for f in st.session_state.generated_feedbacks]
    selected_feedback_name = st.selectbox(
        "Select student essay to view feedback:",
        options=feedback_names,
        key="feedback_select"
    )
    
    # Find the selected feedback
    selected_feedback = next(
        (f for f in st.session_state.generated_feedbacks if f['name'] == selected_feedback_name),
        None
    )
    
    if selected_feedback:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"Feedback for: {selected_feedback_name}")
        
        with col2:
            if st.download_button(
                "⬇️ Download Feedback",
                data=selected_feedback['feedback'],
                file_name=f"{Path(selected_feedback_name).stem}.feedback.txt",
                mime="text/plain"
            ):
                st.success("Downloaded!")
        
        st.divider()
        
        # Display feedback in a nice container
        with st.container():
            st.markdown(selected_feedback['feedback'])


def tab_class_feedback():
    """Tab 3: View class overall feedback"""
    st.header("📊 Class Overall Feedback & Analysis")
    
    if not st.session_state.class_feedback:
        st.info("ℹ️ No class feedback generated yet. Please run automatic marking first.")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Class Performance Analysis")
    
    with col2:
        if st.download_button(
            "⬇️ Download Analysis",
            data=st.session_state.class_feedback,
            file_name="class_overall.feedback.md",
            mime="text/markdown"
        ):
            st.success("Downloaded!")
    
    st.divider()
    
    # Display class feedback
    with st.container():
        st.markdown(st.session_state.class_feedback)


def main():
    """Main application"""
    initialize_session_state()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "📂 Load & Marking",
        "📋 Individual Feedback",
        "📊 Class Feedback"
    ])
    
    with tab1:
        tab_upload_and_marking()
    
    with tab2:
        tab_individual_feedback()
    
    with tab3:
        tab_class_feedback()
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This application provides automated essay marking using AI.
        
        **Features:**
        - Auto-load essays from `essays/` folder
        - Auto-load rubrics from `rubric/` folder
        - Generate detailed feedback
        - View individual student feedback
        - Get class-level insights
        
        **Folder Structure:**
        ```
        essays/         # Student essays (.txt)
        rubric/         # Rubrics (.md)
        feedback_guidance.md  # Root folder
        outputs/        # Generated feedback
        ```
        
        **How to use:**
        1. Place essays in `essays/` folder
        2. Place rubric in `rubric/` folder
        3. Ensure `feedback_guidance.md` exists
        4. Click "Load/Refresh Files"
        5. Click "Start Automatic Marking"
        6. View results in other tabs
        """)
        
        st.divider()
        
        st.subheader("📊 Status")
        st.write(f"Essays loaded: **{len(st.session_state.essay_files)}**")
        st.write(f"Rubrics loaded: **{len(st.session_state.rubric_files)}**")
        st.write(f"Feedback generated: **{len(st.session_state.generated_feedbacks)}**")
        
        if st.session_state.marking_complete:
            st.success("✓ Marking complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main()
