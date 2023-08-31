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
        content_blog_type = st.selectbox('What type of blog are you writing?', ['Select', 'Hot Take', 'Deep Dive', 'Juxtaposition / Fusion'])
    
        if content_blog_type == 'Hot Take':
            angle = st.text_input('The angle of the hot take is:')
        elif content_blog_type == 'Deep Dive':
            focus = st.text_input('I want the focus of the deep dive to be:')
        elif content_blog_type == 'Juxtaposition / Fusion':
            cross_focus = st.text_input('The focus for Juxtaposition / Fusion blog is to explore:')

        audience = st.selectbox('Who is the target audience of this blog?', ['Select', 'Tech Professionals', 'Educated Millenials', 'Emotional Gen-Zs', 'Educated Millenials and Gen-Zs', 'Uneducated Middle Aged Americans'])

        reader_response = st.selectbox('What response do you want from the readers?', ['Select', 'curious to learn more about the topic', 'frustrated that the blog opposes their typical views on the topic', 'surprised that they had not made a connection between these topics before', 'amused by the funny take on the topic'])
    
        st.subheader('Supporting Content URLs')
        support_url1 = st.text_input('Enter the first URL for supporting content:')
        support_url1_type = st.selectbox('How does this URL serve your topic?', ['Select', 'supportive', 'not supportive', 'to be used purely for context in relation'], key='url1_type_selectbox')
        support_url2 = st.text_input('Enter the second URL for supporting content:')
        support_url2_type = st.selectbox('How does this URL serve your topic?', ['Select', 'supportive', 'not supportive', 'to be used purely for context in relation'], key='url2_type_selectbox')
    
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
        theme = st.selectbox('Choose the overall theme of the topic:', ['analytical', 'satirical', 'controversial', 'comedic', 'entertaining', 'childish', 'insightful', 'deep', 'snobby', 'sarcastic', 'dark', 'dark humor', 'extravegent', 'subtle', 'mysterious'])

      
        # All prompt information for content creation
        if st.button('Generate Content'):
            base_prompt = f"As a Senior Copywriter with over 10 years of experience, and a side hustle of owning a very successful blog focused on modern technology, known for its smart humor. Please help me write a '{content_blog_type}' blog about '{blog_topic}'. The target audience for this blog is '{audience}'. We respect the intelligence of all of our readers so the content of the blog should lean on intelligent and entertaining discourse. The response we want from the target audience is that they are '{reader_response}'. Some additional information about the blog is that I want it to be a"
            
            if content_blog_type == 'Hot Take':
                base_prompt += f" hot take, meaning that it is a quickly produced, strongly worded, and often deliberately provocative or sensational opinion or reaction. The angle of the hot take is: '{angle}'."
            elif content_blog_type == 'Deep Dive':
                base_prompt += f" deep dive, meaning that it is an exhaustive investigation, study, or analysis of a question or topic. I want the focus of the deep dive to be: '{focus}'."
            elif content_blog_type == 'Juxtaposition / Fusion':
                base_prompt += f" Juxtaposition / Fusion of the topics, meaning looking at the two or more topics side by side to compare or contrast or to create an interesting effect among the different topics. The focus for Juxtaposition / Fusion blog is to explore: '{cross_focus}'."
            
            base_prompt += f" I have found two articles to support and enhance the quality of the blog. Please use the information provided by these articles, as you see fit, to create interesting connections, provide additional smart humor, or to generally enhance the quality of the blog itself. The first article text is: '{support_url1_type}'. This article is '{url1_text}' of the topic. The second article text is '{support_url2_type}'. This article is '{url2_text}' of the topic. Additionally, I would like to incorporate the following keywords as naturally as possible to promote SEO: '{keywords}'. The desired length of the blog is roughly {blog_length} words. The blog should be written in a '{tone}' tone, but always with an emphasis on using less jargon and more normal casual communication. And the overall theme of the blog should be: '{theme}'. Finally, please provide 2 short descriptions of the blog, one will be used in an accompanying instagram post, one will be used in an accompanying twitter post. It should be written in an engaging, smart humor voice that avoids jargon. Each should use best practices to maximize engagement on each platform. Thanks so much for your help, you are the best Senior Copywriter in the world!"
        
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
