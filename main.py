import streamlit as st
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
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
    
    st.subheader('Recent Company News')
    company_news = st.text_area('Input the recent company news here')

    if st.button('Generate Cover Letter'):
        # Prepare the context content and prompt content
        context_content = "\n".join(str(document) for document in resume_pages + job_description_pages) + "\n" + company_news
        prompt_content = f"""
        I'm applying for a position at {company_name}. Given my skills and experience, which are outlined in my resume, I believe I would be a good fit. The job description for the role resonates with my professional profile. Furthermore, the recent news from the company has gotten me very excited about this opportunity. I would like to express my interest and enthusiasm for this role in a cover letter. Can you help me draft one?
        """
    
        # Define message templates for context and prompt
        system_message_prompt = SystemMessagePromptTemplate.from_template("{context}")
        human_message_prompt = HumanMessagePromptTemplate.from_template("{prompt}")
    
        # Build a chat prompt template from the system and human message templates
        chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
        # Generate the chat messages using the chat prompt template
        messages = chat_prompt_template.format_prompt(context=context_content, prompt=prompt_content).to_messages()
    
        # Generate the cover letter
        chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=1)
        chat(messages)
    
        # Display the cover letter
        st.markdown(chat.messages[-1].content)


if __name__ == "__main__":
    main()
