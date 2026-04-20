from app.models.text_input import TextInput

def process_text(input: TextInput):
    # Your logic here
    return {"message": f"Received {len(input.text.splitlines())} lines of text."}
