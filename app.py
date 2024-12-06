from main_logic import setup_chain
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Define the query model
class QueryRequest(BaseModel):
    mood: str

# Load the chain
chain = setup_chain()

@app.post("/recommendation")
def get_recommendation(query: QueryRequest):
    result = chain.invoke({"input": query.mood})
    genres = result['answer'].replace("Genre: ", "").split(", ")
    response = {"genres": genres}
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="", port=8000)
# To run the FastAPI app, run the following command in the terminal:
# uvicorn app:app --reload