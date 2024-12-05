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

# Define the endpoint
@app.post("/recommendation")
async def get_recommendation(query: QueryRequest):
    result = await chain.invoke({"input": query.mood})
    response = {"genres": result['answer']}
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="", port=8000)
# To run the FastAPI app, run the following command in the terminal:
# uvicorn app:app --reload