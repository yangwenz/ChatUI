from abc import abstractmethod
from typing import Dict, List, Union


class BaseModel:

    def __init__(self, model_path=None):
        self.model_path = model_path

    @abstractmethod
    def predict(self, inputs: Dict, **kwargs) -> Union[str, List]:
        """
        Generates answers given contexts and questions.

        :param inputs: ``inputs`` is a dict with the following format:
            `{"inputs": {
                "past_user_inputs": past_user_inputs,
                "generated_responses": generated_responses,
                "text": user_question,
                "prompt": prompt}
            }`, where `past_user_inputs` is a list of past user questions,
            `generated_responses` is a list of past generated answers, and
            `prompt` is the input prompt which can be empty.
        :return: One of multiple answers.
        """
        pass

    @staticmethod
    def get_model_input(
            inputs,
            question_prefix="Question:",
            answer_prefix="Answer:",
            sep="\n",
            prompt=None,
            **kwargs
    ):
        prompt = prompt + sep if prompt else ""
        inputs = inputs["inputs"]
        if "past_user_inputs" in inputs and "generated_responses" in inputs:
            for question, answer in zip(inputs["past_user_inputs"], inputs["generated_responses"]):
                if answer.startswith("ERROR:"):
                    continue
                prompt += f"{question_prefix} {question}{sep}{answer_prefix} {answer}{sep}"
        if "text" in inputs:
            prompt += f"{question_prefix} {inputs['text']}{sep}{answer_prefix} "
        return BaseModel._check_length(prompt, sep=sep)

    @staticmethod
    def _check_length(prompt, sep, max_length=1600):
        n = len(prompt.split())
        if n > max_length:
            sentences = prompt.split(sep)
            while len(sentences) > 4:
                question = sentences.pop(0)
                answer = sentences.pop(0)
                k = len(question.split()) + len(answer.split())
                n -= k
                if n < max_length * 0.95:
                    break
            return sep.join(sentences)
        return prompt
