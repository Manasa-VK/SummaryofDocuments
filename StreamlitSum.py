# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 12:31:27 2023

@author: karun
"""



import streamlit as st
import fitz  # PyMuPDF's main module
import Openai_configsumz 
import openai
openai.api_key = Openai_configsumz.openai_key


def chunk_text(text, chunk_size, overlap):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks



def open_aisum(user_input):

    res_box = st.empty()
    full_answer = []

    ### System Prompt
    system_prompt = '''
    Refactor a short summary for the information given by the user.
    '''

    for chunk in openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": "{}".format(user_input)}],
            stream=True):

        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            
            print(content, end='')
            full_answer.append(content)
            result = "".join(full_answer).strip()
            res_box.markdown(f'<div style="border: 1px solid blue; padding: 10px;">{result}</div>', unsafe_allow_html=True)
            
    return full_answer


def main():
    st.title("Summerization of Documents")

    # Sidebar
    st.sidebar.title("Documents Summarize")
    
    uploaded_file = st.sidebar.file_uploader("Upload Doc", type=["pdf"])
    print(uploaded_file)
    
    if uploaded_file is not None:

        pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    
        print(pdf_document)
        
        
        full_text=''
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text("text")  # Extract text from the page
            full_text = full_text+page_text
            ##print("Page", page_num + 1)
            ##print(page_text)
            
        chunks = chunk_text(full_text, chunk_size=2000, overlap=200)
        print(chunks)
        for c in chunks:
            open_aisum(c)
            

    
   

    
if __name__ == "__main__":
    main()
    
    
    

    
    
    
    
    