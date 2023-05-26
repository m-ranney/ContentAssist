import streamlit as st
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import openai
import os
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title('AI Cover Letter Generator')

    st.subheader('Upload Resume')
    resume = st.file_uploader('Choose a resume file', type=['pdf'])
    if resume is not None:
        # Save UploadedFile to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(resume.read())
        # Use PyPDFLoader to load the resume
        loader = PyPDFLoader(fp.name)
        resume_pages = loader.load_and_split()
    else:
        st.warning('Please upload a resume.')

    st.subheader('Job Description URL')
    job_url = st.text_input('Input the URL here')
    if job_url:
        # Use WebBaseLoader to load the job description
        loader = WebBaseLoader(job_url)
        job_description_pages = loader.load_and_split()
    else:
        st.warning('Please enter a job URL.')

    st.subheader('Company Name')
    company_name = st.text_input('Input the company name here')
    
    st.subheader('Any additional information you would like to include?')
    additional_info = st.text_area('Input any additional information here')

    if st.button('Generate Cover Letter'):
        # Prepare the context content and prompt content
        context_content = str.join('\n', [document.page_content for document in resume_pages + job_description_pages])
        prompt_content = f"""
        I'm applying for a position at {company_name}. Given my skills and experience, which are outlined in my resume, I believe I would be a good fit. The job description for the role resonates with my professional profile, and I have provided this additional information that is relevant for my interest and fit for the job: {additional_info}. Furthermore, the strategic direction from the company has gotten me very excited about this opportunity. I would like to express my interest and enthusiasm for this role in a cover letter. Can you help me draft one?
        """
    
        # Define message templates for context and prompt
        system_message_prompt = SystemMessagePromptTemplate.from_template(context_content)
        human_message_prompt = HumanMessagePromptTemplate.from_template(prompt_content)
    
        # Build a chat prompt template from the system and human message templates
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
        # Generate the chat messages using the chat prompt template
        messages = chat_prompt.format_prompt(company_name=company_name, additional_info=additional_info).to_messages()
    
        # Generate the cover letter
        chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=1)
        
        response = chat(messages)
    
        # Format the output
        formatted_content = '\n'.join(response.content.splitlines())

        # Display the cover letter
        st.subheader('Cover Letter')
        with st.form(key='cover_letter_form'):
            # Initialize session state
            if 'text' not in st.session_state:
                st.session_state['text'] = formatted_content
    
            # Get the current text_area content
            current_text = st.text_area("Edit your cover letter:", value=st.session_state['text'], height=600)
            if st.form_submit_button('Export Cover Letter'):
                # Update session state with the current text
                st.session_state['text'] = current_text
                # Save the cover letter as a PDF file
                with open('cover_letter.pdf', 'w') as f:
                    f.write(st.session_state['text'])
                st.success('Cover letter exported successfully!')

if __name__ == "__main__":
    main()
