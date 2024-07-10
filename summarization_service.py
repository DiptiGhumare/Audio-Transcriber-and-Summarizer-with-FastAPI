from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load summarization model and tokenizer
try:
    model_name = "t5-small"  # You can also use "t5-base" or "t5-large" for better performance
    summarization_model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)
except Exception as e:
    raise RuntimeError(f"Failed to load summarization model: {str(e)}")

def summarize_text(text: str) -> str:
    try:
        # Preprocess text
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate summary
        summary_ids = summarization_model.generate(inputs, max_length=130, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        
        # Decode summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return summary
    except Exception as e:
        raise RuntimeError(f"Error in summarization: {str(e)}")
