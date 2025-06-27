

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def chunk_prompt(prompt: str, chunk_size: int = 10000):
    # Split by lines and strip whitespace from each line
    lines = [line.strip() for line in prompt.split('\n')]
    # Filter out empty lines that might result from stripping
    lines = [line for line in lines if line]

    chunks = []
    current_chunk_lines = []
    current_chunk_length = 0 # This will track the length of the joined string

    for line in lines:
        # Length of the line itself
        line_len = len(line)

        # If current_chunk_lines is not empty, we'll add a newline before the new line
        # So, the length added by this line is its length + 1 for the newline
        # If current_chunk_lines is empty, it's just the line's length
        length_to_add = line_len + (1 if current_chunk_lines else 0)

        # If adding this line would exceed the chunk_size, and we already have content in the current chunk
        if current_chunk_length + length_to_add > chunk_size and current_chunk_lines:
            chunks.append("\n".join(current_chunk_lines))
            current_chunk_lines = []
            current_chunk_length = 0
            # After creating a new chunk, the current line becomes the first line of the new chunk
            current_chunk_lines.append(line)
            current_chunk_length = line_len # No leading newline for the first line of a new chunk
        elif line_len > chunk_size: # If a single line is too long, it becomes its own chunk
            if current_chunk_lines: # Finalize any existing partial chunk
                chunks.append("\n".join(current_chunk_lines))
                current_chunk_lines = []
                current_chunk_length = 0
            chunks.append(line) # Add the oversized line as its own chunk
            current_chunk_length = 0 # Reset for the next chunk
        else: # Add the line to the current chunk
            current_chunk_lines.append(line)
            current_chunk_length += length_to_add

    # Add any remaining lines as the last chunk
    if current_chunk_lines:
        chunks.append("\n".join(current_chunk_lines))

    print(f"DEBUG: Generated {len(chunks)} chunks.")
    return chunks

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chunk", response_class=HTMLResponse)
async def chunk(request: Request, prompt: str = Form(...), chunk_size: int = Form(10000)):
    chunks = chunk_prompt(prompt, chunk_size)
    num_chunks = len(chunks)
    
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        is_last_chunk = i == num_chunks - 1
        
        if is_last_chunk:
            chunk_prompt_text = f"This is the final part of the prompt. Please provide the complete response based on all the parts provided.\n\n{chunk}"
        else:
            chunk_prompt_text = f"This is part {i+1}/{num_chunks} of a larger prompt. Store this information and wait for the final part before providing a complete response. Do not provide any output until you receive the final part.\n\n{chunk}"
        
        processed_chunks.append(chunk_prompt_text)
        
    return templates.TemplateResponse("chunks.html", {"request": request, "chunks": processed_chunks})