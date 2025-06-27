

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def split_prompt(prompt: str, split_size: int = 10000):
    # Split by lines and strip whitespace from each line
    lines = [line.strip() for line in prompt.split('\n')]
    # Filter out empty lines that might result from stripping
    lines = [line for line in lines if line]

    splits = []
    current_split_lines = []
    current_split_length = 0 # This will track the length of the joined string

    for line in lines:
        # Length of the line itself
        line_len = len(line)

        # If current_split_lines is not empty, we'll add a newline before the new line
        # So, the length added by this line is its length + 1 for the newline
        # If current_split_lines is empty, it's just the line's length
        length_to_add = line_len + (1 if current_split_lines else 0)

        # If adding this line would exceed the split_size, and we already have content in the current split
        if current_split_length + length_to_add > split_size and current_split_lines:
            splits.append("\n".join(current_split_lines))
            current_split_lines = []
            current_split_length = 0
            # After creating a new split, the current line becomes the first line of the new split
            current_split_lines.append(line)
            current_split_length = line_len # No leading newline for the first line of a new split
        elif line_len > split_size: # If a single line is too long, it becomes its own split
            if current_split_lines: # Finalize any existing partial split
                splits.append("\n".join(current_split_lines))
                current_split_lines = []
                current_split_length = 0
            splits.append(line) # Add the oversized line as its own split
            current_split_length = 0 # Reset for the next split
        else: # Add the line to the current split
            current_split_lines.append(line)
            current_split_length += length_to_add

    # Add any remaining lines as the last split
    if current_split_lines:
        splits.append("\n".join(current_split_lines))

    print(f"DEBUG: Generated {len(splits)} splits.")
    return splits

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/split", response_class=HTMLResponse)
async def split(request: Request, prompt: str = Form(...), split_size: int = Form(10000)):
    splits = split_prompt(prompt, split_size)
    num_splits = len(splits)
    
    processed_splits = []
    for i, split_part in enumerate(splits):
        is_last_split = i == num_splits - 1
        
        if is_last_split:
            split_prompt_text = f"[START PART {i+1}/{num_splits}]\n{split_part}\n[END PART {i+1}/{num_splits}]\n\nALL PARTS SENT. Now you can continue processing the data and answering my requests."
        else:
            split_prompt_text = f'[START PART {i+1}/{num_splits}]\n{split_part}\n[END PART {i+1}/{num_splits}]\n\nAfter you receive this, just answer with "Received part {i+1}/{num_splits}" and nothing else.'
        
        processed_splits.append(split_prompt_text)
        
    return templates.TemplateResponse("chunks.html", {"request": request, "chunks": processed_splits})