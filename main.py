import streamlit as st
from langchain.document_loaders import WebBaseLoader
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title('AI Content Assistant')

    # Sidebar navigation
    choice = st.sidebar.radio("Choose an action", ["Topic Generator", "Content Creator"])

    if choice == "Topic Generator":
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
                prompt = base_prompt + " hot take blog ideas or headlines and provide a few sentence overview about the content for each blog. In which the idea or headline is an opinion or view that goes against the mainstream or could be somewhat taboo."
            elif blog_type == 'Deep Dive':
                prompt = base_prompt + " deep dive blog ideas or headlines and provide a few sentence overview about the content for each blog. In which the idea or headline is an exploration of some interesting details related to the topic."
            elif blog_type == 'Cross-Topic':
                prompt = base_prompt + " cross-topic blog ideas or headlines and provide a few sentence overview about the content for each blog. In which the idea or headline is an exploration of both the topic and a seemingly irrelevant topic, but one that actually has some interesting connections."
        
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
            st.write(response.choices[0]['message']['content'].strip())
    
  
    # Content Generator Section
    elif choice == "Content Creator":
        st.title('Content Creator')
    
        st.subheader('Enter Blog Topic')
        blog_topic = st.text_input('Provide the topic of the blog:')
    
        st.subheader('Select Blog Type')
        content_blog_type = st.selectbox('What type of blog are you writing?', ['Select', 'Hot Take', 'Deep Dive', 'Cross-Topic'])
    
        if content_blog_type == 'Hot Take':
            angle = st.text_input('What angle do you want to take with the hot take?')
        elif content_blog_type == 'Deep Dive':
            focus = st.text_input('What focus do you want for the deep dive?')
        elif content_blog_type == 'Cross-Topic':
            cross_focus = st.text_input('What focus do you want for the cross topic?')
    
        st.subheader('Supporting Content URLs')
        support_url1 = st.text_input('Enter the first URL for supporting content:')
        support_url1_type = st.selectbox('How does this URL serve your topic?', ['Select', 'Supporting', 'Not Supporting', 'Pure Context'], key='url1_type_selectbox')
        support_url2 = st.text_input('Enter the second URL for supporting content:')
        support_url2_type = st.selectbox('How does this URL serve your topic?', ['Select', 'Supporting', 'Not Supporting', 'Pure Context'], key='url2_type_selectbox')
    
        url1_text = ""
        if support_url1:
            loader = WebBaseLoader(support_url1)
            url1_pages = loader.load_and_split()
            url1_text = " ".join([doc.text for doc in url1_pages if hasattr(doc, 'text')]) 
        
        url2_text = ""
        if support_url2:
            loader = WebBaseLoader(support_url2)
            url2_pages = loader.load_and_split()
            url2_text = " ".join([doc.text for doc in url2_pages if hasattr(doc, 'text')]) 
      
        keywords = st.text_input('Provide any keywords to be utilized in the copy:')
        blog_length = st.text_input('Desired length of the blog (in number of words):')
        tone = st.selectbox('What tone would you like for the content?', ['Casual', 'Comedic', 'Pompous', 'Dry'])
        theme = st.selectbox('Choose the overall theme of the topic:', ['Analytical', 'Satirical', 'Controversial', 'Comedic', 'Entertaining', 'Childish', 'Insightful', 'Deep'])
    
        if st.button('Generate Content'):
            base_prompt = f"I'm aiming to write a '{content_blog_type}' blog about '{blog_topic}'. Here are the specifics:"
            
            if content_blog_type == 'Hot Take':
                base_prompt += f" The angle of the hot take is '{angle}'."
            elif content_blog_type == 'Deep Dive':
                base_prompt += f" The focus is to dive deep into '{focus}'."
            elif content_blog_type == 'Cross-Topic':
                base_prompt += f" The focus for cross-topic exploration is '{cross_focus}'."
            
            base_prompt += f" I have found two articles, the first one is '{support_url1_type}' and its content is: '{url1_text}'. The second one is '{support_url2_type}' and its content is: '{url2_text}'. I would like to emphasize on these keywords: '{keywords}'. The desired length is about {blog_length} words and should be written in a '{tone}' tone with an overall '{theme}' theme."
        
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": base_prompt}],
                temperature=1,
                max_tokens=5000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.25
            )
            
            st.subheader('Generated Content')
            st.write(response.choices[0]['message']['content'].strip())


if __name__ == "__main__":
    main()
