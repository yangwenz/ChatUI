from models.base import BaseModel
from typing import Dict, List, Union


class NaiveBot(BaseModel):

    def __init__(self, model_path=None):
        import torch
        from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

        super().__init__(model_path)
        if self.model_path is None:
            self.model_path = "facebook/blenderbot-400M-distill"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
        self.tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
        self.model.to(self.device)

    def predict(self, inputs: Dict, **kwargs) -> Union[str, List]:
        input_text = self.get_model_input(inputs, prompt=inputs.get("prompt", None), **kwargs)
        input_ids = self.tokenizer([input_text], return_tensors="pt").to(self.device)
        reply_ids = self.model.generate(**input_ids)
        outputs = self.tokenizer.batch_decode(reply_ids)

        # Generated answers
        answer = outputs[0][4:-4]
        # References
        references = "Reference: xxx"
        # Follow ups
        followup_questions = "What's next?"
        return [answer, references, followup_questions]
