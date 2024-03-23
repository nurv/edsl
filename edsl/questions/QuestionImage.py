"""This module contains the QuestionExtract class. It is a subclass of the Question class and is used to create questions that ask the user to extract values from a string, and return them in a given template.
Example usage:

.. code-block:: python

    from edsl.questions import QuestionImage

    q = QuestionImage(
        question_name = "image_ask",
        question_text = "Selecte the destinations that you would like to visit",
        images = ["link1","link2"]

    )

"""
#TODO two way solution user provieds the images (like what car do you like)
#TODO ai is generating based on the question text the suggested images
#TODO user provies a list of links
#TODO from image start suggesting possible questions like I have this place that I want to promote. Give me some ideas in a list

from __future__ import annotations
import re
import json
from typing import Any
from edsl.questions import Question
from edsl.questions.descriptors import AnyDescriptor
from edsl.scenarios import Scenario
from edsl.utilities import random_string


class QuestionImage(Question):
    """
    This question asks the respondent to extract values from a string, and return them in a given template.

    """
    question_type = "image"

    question_options: list[str] = AnyDescriptor()
    sub_type: str = AnyDescriptor()
    question_images: list[str] = AnyDescriptor()

    def __init__(
        self,
        question_text: str,
        question_name: str,
        question_images:list[str],
        sub_type:str = None,
        question_options: list[str] = None,

    ):
        """Initialize the question."""
        self.question_name = question_name
        self.question_text = question_text
        self.question_options = question_options
        self.question_images = question_images
        self.sub_type = sub_type

    ################
    # Answer methods
    ################
    def validate_answer(self, answer: Any) -> dict[str, Any]:
        """Validate the answer."""
        # raw_json = answer["answer"]
        # fixed_json_data = re.sub(r"\'", '"', raw_json)
        # answer["answer"] = json.loads(fixed_json_data)
        #self.validate_answer_template_basic(answer)
        # self.validate_answer_key_value(answer, "answer", dict)
        #TODO implement this
        #self.validate_answer_extract(answer)
        return answer
    def translate_answer_code_to_answer(self, answer, scenario):
        """Required by Question, but not used by QuestionImage."""
        return answer
    def simulate_answer(self, human_readable: bool = True) -> dict[str, str]:
        """Simulate a valid answer for debugging purposes."""
        return {
            "answer": {key: random_string() for key in self.answer_template.keys()},
            "comment": random_string(),
        }

    ################
    # Helpful methods
    ################
    @classmethod
    def example(cls) -> QuestionImage:
        """Return an example question."""
        return cls(
            question_name="image_test2",
            question_text="2.Whould you visit this plance and why?",
            question_images=["https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"],

        )


def main():
    from edsl.questions import QuestionImage
    from edsl import Model
    q1 = QuestionImage(
        question_name="image",
        question_text="Give me a slogan for each image",
        question_images=[
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNiMdOiJoRIereQ4fb6rNsgPngPNyqvYWSBrIDcSbCCg&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEB8lb6UtOE7szUxVEFKbs1PG2z5uJUiBlypJn4xE_1A&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpTotNcLz_n1qOO0rqQsADyt5uaAzFsK6FtBZewTybgw&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQl-W4lpydB5z8EhifIo_NcjQW2W_etUHbcGF9-7Cw_HA&s"]
    )
    model = Model("gpt-4-vision-preview")
    res  = q1.by(model).run()
    print(res)

if __name__ == "__main__":
    main()