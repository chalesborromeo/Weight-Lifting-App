from fastapi import FastAPI

app = FastAPI()

posts = []

@app.get("/")
def root():
    return {"message": "Spotter backend is running"}

@app.get("/about")
def about():
    return {"message": "Track lifts and connect with spotters"}

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts")
def create_post(post: dict):
    posts.append(post)
    return {"message": "Post created", "post": post}