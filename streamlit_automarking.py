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


def invoke_claude_v4_sonnet(prompt, **kwargs):
    """Invoke Claude model with a simple prompt"""
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

    logging.info(f"Generating feedback for essay: {essay_name}")
    feedback = invoke_claude_v4_sonnet(prompt, max_tokens=3000)
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

    logging.info("Generating class overall feedback")
    class_feedback = invoke_claude_v4_sonnet(prompt, max_tokens=4000)
    return class_feedback


def save_feedback_file(essay_name: str, feedback: str, output_dir: str = "outputs") -> str:
    """Save feedback to a file"""
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(essay_name).stem
    feedback_filename = f"{base_name}.feedback.txt"
    feedback_path = os.path.join(output_dir, feedback_filename)
    
    with open(feedback_path, 'w', encoding='utf-8') as f:
        f.write(feedback)
    
    logging.info(f"Saved feedback to: {feedback_path}")
    return feedback_path


def save_class_feedback(class_feedback: str, output_dir: str = "outputs") -> str:
    """Save class feedback to a file"""
    os.makedirs(output_dir, exist_ok=True)
    class_feedback_path = os.path.join(output_dir, "class_overall.feedback.md")
    
    with open(class_feedback_path, 'w', encoding='utf-8') as f:
        f.write(class_feedback)
    
    logging.info(f"Saved class feedback to: {class_feedback_path}")
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


def tab_upload_and_marking():
    """Tab 1: Upload files and perform automatic marking"""
    st.header("📤 Upload Files & Run Automatic Marking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Student Essays")
        essay_uploads = st.file_uploader(
            "Upload student essay files (.txt)",
            type=['txt'],
            accept_multiple_files=True,
            key="essay_uploader"
        )
        
        if essay_uploads:
            for uploaded_file in essay_uploads:
                if uploaded_file.name not in st.session_state.essay_files:
                    content = uploaded_file.read().decode('utf-8')
                    st.session_state.essay_files[uploaded_file.name] = content
                    logging.info(f"Uploaded essay: {uploaded_file.name}")
            
            st.success(f"✓ {len(st.session_state.essay_files)} essay(s) uploaded")
            
            # Preview selected essay
            if st.session_state.essay_files:
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
                        key="essay_preview_area"
                    )
    
    with col2:
        st.subheader("Upload Rubric")
        rubric_uploads = st.file_uploader(
            "Upload rubric files (.md)",
            type=['md'],
            accept_multiple_files=True,
            key="rubric_uploader"
        )
        
        if rubric_uploads:
            for uploaded_file in rubric_uploads:
                if uploaded_file.name not in st.session_state.rubric_files:
                    content = uploaded_file.read().decode('utf-8')
                    st.session_state.rubric_files[uploaded_file.name] = content
                    logging.info(f"Uploaded rubric: {uploaded_file.name}")
            
            st.success(f"✓ {len(st.session_state.rubric_files)} rubric(s) uploaded")
            
            # Preview selected rubric
            if st.session_state.rubric_files:
                selected_rubric = st.selectbox(
                    "Select rubric to preview:",
                    options=list(st.session_state.rubric_files.keys()),
                    key="rubric_preview_select"
                )
                with st.expander("Preview Rubric", expanded=False):
                    st.markdown(st.session_state.rubric_files[selected_rubric])
    
    st.divider()
    
    # Upload feedback guidance
    st.subheader("Upload Feedback Guidance")
    guidance_upload = st.file_uploader(
        "Upload feedback guidance file (.md)",
        type=['md'],
        key="guidance_uploader"
    )
    
    if guidance_upload:
        st.session_state.feedback_guidance = guidance_upload.read().decode('utf-8')
        st.success("✓ Feedback guidance uploaded")
        with st.expander("Preview Guidance", expanded=False):
            st.markdown(st.session_state.feedback_guidance)
    
    st.divider()
    
    # Select which rubric to use for marking
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
                    logging.error(f"Error processing {essay_name}: {str(e)}")
                
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
                logging.error(f"Error generating class feedback: {str(e)}")
            
            status_text.text("✓ Marking complete!")
            st.session_state.marking_complete = True
            st.success(f"✓ Successfully marked {total_essays} essay(s) and generated class feedback!")
            st.balloons()
    
    if not can_mark:
        st.info("ℹ️ Please upload essays, a rubric, and feedback guidance to start marking.")


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
        "📤 Upload & Marking",
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
        - Upload multiple student essays
        - Use custom rubrics
        - Generate detailed feedback
        - View individual student feedback
        - Get class-level insights
        
        **How to use:**
        1. Upload student essays (.txt)
        2. Upload rubric (.md)
        3. Upload feedback guidance (.md)
        4. Click "Start Automatic Marking"
        5. View results in other tabs
        """)
        
        st.divider()
        
        st.subheader("📊 Status")
        st.write(f"Essays uploaded: **{len(st.session_state.essay_files)}**")
        st.write(f"Rubrics uploaded: **{len(st.session_state.rubric_files)}**")
        st.write(f"Feedback generated: **{len(st.session_state.generated_feedbacks)}**")
        
        if st.session_state.marking_complete:
            st.success("✓ Marking complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main()
