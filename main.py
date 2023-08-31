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
    url2 = st.text_input('Enter second URL for supporting content:')
    url3 = st.text_input('Enter third URL for supporting content:')
    
    # Fetch content from URLs
    urls = [url for url in [url1, url2, url3] if url]
    supporting_content_pages = []
    for url in urls:
        loader = WebBaseLoader(url)
        content = loader.load_and_split()
        # Assuming content is an instance of a class, you might need to extract the relevant text property.
        supporting_content_pages.append(content.text)
    aggregated_content = ' '.join(supporting_content_pages)
    
    # 4. Ask the user if they want to provide any additional notes.
    st.subheader('Enter Additional Notes')
    notes = st.text_area('Any additional notes?')


    if st.button('Generate Topic Ideas'):
        # Prepare the prompt based on the type of blog
        base_prompt = f"Given the topic '{topic}', and the supporting content: {aggregated_content}, along with additional notes: {notes}, provide 3-5"
        if blog_type == 'Hot Take':
            prompt = base_prompt + " hot take blog ideas or headlines."
        elif blog_type == 'Deep Dive':
            prompt = base_prompt + " deep dive blog ideas or headlines."
        elif blog_type == 'Cross-Topic':
            prompt = base_prompt + " cross-topic blog ideas or headlines."
    
        # Fetch results using OpenAI API
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {
              "role": "system",
              "content": aggregated_content  
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
