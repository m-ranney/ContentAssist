import streamlit as st
from langchain.document_loaders import WebBaseLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import openai
import os
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title('AI Content Assistant')
    st.title('Topic Generator')
    
    # 1. Ask the user to input the topic they want to write about
    st.subheader('Enter Topic')
    topic = st.text_input('What topic would you like to write about?')
    
    # 2. Ask the user to Select the type of blog they want to write: Hot Take, Deep Dive, Cross-Topic
    st.subheader('Select Blog Type')
    blog_type = st.selectbox('What type of blog do you want to write?', ['Select', 'Hot Take', 'Deep Dive', 'Cross-Topic'])
    
    # 3. Supporting Content URLs
    st.subheader('Enter Supporting Content URLs')
    url1 = st.text_input('Enter first URL for supporting content:')
    url1_context = st.text_area('Enter context for first URL:')
    url2 = st.text_input('Enter second URL for supporting content:')
    url2_context = st.text_area('Enter context for second URL:')
    url3 = st.text_input('Enter third URL for supporting content:')
    url3_context = st.text_area('Enter context for third URL:')

    if url1:
        # Use WebBaseLoader to load the job description
        loader = WebBaseLoader(url1)
        url1_pages = loader.load_and_split()
        url1_text = " ".join([doc.text for doc in url1_pages if hasattr(doc, 'text')]) 
    else:
        st.warning('Want a URL?')
  
    if url2:
        # Use WebBaseLoader to load the job description
        loader = WebBaseLoader(url2)
        url2_pages = loader.load_and_split()
        url2_text = " ".join([doc.text for doc in url2_pages if hasattr(doc, 'text')]) 
    else:
        st.warning('Want a URL?')
  
    # 4. Ask the user if they want to provide any additional notes.
    st.subheader('Enter Additional Notes')
    notes = st.text_area('Any additional notes?')


    if st.button('Generate Topic Ideas'):
        # Prepare the prompt based on the type of blog
        base_prompt = f"You are a creative senior marketer. I want to write a blog about '{topic}'. I have provided some content that I'd like to use as context to help brainstorm creative blog ideas. This includes an article that is {url1_context} and the supporting content for that article is: {url1_text}. Finally a few additional notes that I would like to incorporate into the ideation of blog ideation is: {notes}. Please provide 3-5"
        if blog_type == 'Hot Take':
            prompt = base_prompt + " hot take blog ideas or headlines. In which the idea or headline is an opinion or view that goes against the mainstream or could be somewhat taboo."
        elif blog_type == 'Deep Dive':
            prompt = base_prompt + " deep dive blog ideas or headlines. In which the idea or headline is an exploration of some interesting details related to the topic."
        elif blog_type == 'Cross-Topic':
            prompt = base_prompt + " cross-topic blog ideas or headlines. In which the idea or headline is an exploration of both the topic and a seemingly irrelevant topic, but one that actually has some interesting connections."
    
        # Fetch results using OpenAI API
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {
              "role": "system",
              "content": url1_text  
            },
            {
              "role": "user",
              "content": prompt
            }
          ],
          temperature=1,
          max_tokens=2000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0.25
        )
    
        # Display topic ideas
        st.subheader('Generated Topic Ideas')
        st.write(response.choices[0].text.strip())

if __name__ == "__main__":
    main()
