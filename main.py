import pandas as pd
import numpy as np
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import gradio as gr

load_dotenv()


books=pd.read_csv("books_with_emotions.csv")
books['large_thumbnail']=books['thumbnail']+"&fife=w800"
books['large_thumbnail']=np.where(books['large_thumbnail'].isna()
                                ,"missing_cover.png",
                                books['large_thumbnail'])

raw_document = TextLoader('tagged_description.txt', encoding='utf-8').load()
text_splitter=CharacterTextSplitter(chunk_size=0,chunk_overlap=0,separator='\n')
documents=text_splitter.split_documents(raw_document)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
dp_books = Chroma.from_documents(documents, embedding_model)

# Function to retrieve semantic recommendations
def retrieve_semantic_recommendations(
        query:str,
        category:str=None,
        tone:str=None,
        initial_top_k:int=50,
        final_top_k:int=12
        )->pd.DataFrame:
        """
        This Function takes a Query and number of results that You want to retrieve
        and then return a pandas df of the result
        """
        recs=dp_books.similarity_search(query,k=initial_top_k)
        books_List=[int(rec.page_content.strip('"').split()[0]) for rec in recs]
        book_rcs=books[books["isbn13"].isin(books_List)].head(initial_top_k)


        if category!="All":        
            book_rcs=book_rcs[book_rcs['simplified_categories']==category][:final_top_k]

        else:
            book_rcs=book_rcs.head(final_top_k)

        if tone=="Happy":
            book_rcs.sort_values(by='joy',ascending=False,inplace=True)
        elif tone=="Sad":
            book_rcs.sort_values(by='sad',ascending=False,inplace=True)
        elif tone=="Angry":
            book_rcs.sort_values(by='angry',ascending=False,inplace=True)
        elif tone=="Suspensful":
            book_rcs.sort_values(by='fear',ascending=False,inplace=True)
        elif tone=="Surprising":
            book_rcs.sort_values(by='surprise',ascending=False,inplace=True)
        elif tone=="Neutral":
            book_rcs.sort_values(by='neutral',ascending=False,inplace=True)
        
        return book_rcs


def recommend_books(query:str,category:str,tone:str)->pd.DataFrame:
    """
    This function takes a query and returns a pandas df of the result
    """
    recommendations= retrieve_semantic_recommendations(query,category,tone)
    results=[]
    for _,row in recommendations.iterrows():
        description=row['description']
        truncated_description=description[:50] + '...' if len(description) > 50 else description

        authors_split=row['authors'].split(";")
        if len(authors_split)==2:
            authors_str=f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split)>2:
            authors_str=f"{', '.join(authors_split[:-1])} and {authors_split[-1]}"
        else:
            authors_str=row['authors']


        caption=f"{row['title']} by {authors_str} \n\n {truncated_description}"
        results.append((row['large_thumbnail'], caption))

    return results


categories=["All"]+sorted(books['simplified_categories'].unique())
tones=["All"]+["Happy","Sad","Angry","Suspensful","Surprising","Neutral"]

def show_loading():
    return gr.update(value="⏳ Loading recommendations...", visible=True)

def hide_loading():
    return gr.update(value="", visible=False)

with gr.Blocks(theme=gr.themes.Glass().set(
    body_text_size="32px",
    )) as dashboard:
    gr.Markdown(
        """
        <h1 style="text-align: center;">📚 Book Recommender</h1>
        <p style="text-align: center;">Find your next read based on your mood and preferences!</p>
        """
    )

    query = gr.Textbox(
        label="Enter a Description of a Book",
        placeholder="What are you looking for?",
        lines=3,
        info="E.g., 'A heartwarming romantic story with a twist'",
        elem_classes="input-textbox"
    )

    category = gr.Dropdown(label="Select a category", choices=categories, value="All")
    tone = gr.Dropdown(label="Select a tone", choices=tones, value="All")
    submit_button = gr.Button("🔍 Get Recommendations")

    loading_msg = gr.Text(value="", visible=False, elem_classes="loading-text")

    output = gr.Gallery(label="Recommended Books", columns=2, rows=5, show_label=False, elem_id="gallery")

    gr.Markdown(
        """
        <p style="text-align: center; margin-top: 20px;">Scroll down to see your personalized recommendations!</p>
        """
    )

    submit_button.click(fn=show_loading, inputs=[], outputs=loading_msg)
    submit_button.click(fn=recommend_books, inputs=[query, category, tone], outputs=output)
    submit_button.click(fn=hide_loading, inputs=[], outputs=loading_msg)

if __name__ == "__main__":
    dashboard.launch()