from transformers import pipeline
import streamlit as st
from PIL import Image 

#tab name and favicon
st.set_page_config(page_title='Text Summarizer', page_icon='📖', layout='centered')

summarizer=pipeline('summarization')



#image=Image.open('image.png')
#st.image('bot.gif',use_column_width=True)
st.image('logodone.png',use_column_width=True)

st.write("""
# Text Summarizer 🎨 
Using Hugging Face Transformers 🤗
""")

import streamlit as st


with st.form(key='my_form'):

    input=st.text_area('Enter your Text',height=300)
    # Create two columns for responsive layout
    cols = st.columns(2)

# Access individual columns for content placement
    left_column, right_column = cols[0], cols[1]

# Place content within each column using 'with' blocks
with left_column:
    # Your content for the left column
    min=left_column.number_input('Minimum words',value=30)

with right_column:
    # Your content for the right column
    max=right_column.number_input('Maximum words',value=130)

    submit_button = st.form_submit_button("Summarize")


if submit_button:
    # This block executes only when the user clicks the submit button
    summary=summarizer(input,max_length=max, min_length=min, do_sample=False)
    st.subheader('Result 🎉')
    st.info(summary[0]['summary_text'])
    st.write('**Length:** '+str(len(summary[0]['summary_text'].split(' ')))+' words')





