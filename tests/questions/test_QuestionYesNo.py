import pytest
from edsl.exceptions import (
    QuestionResponseValidationError,
    QuestionAnswerValidationError,
)
from edsl.questions import Question, QuestionYesNo
from edsl.questions.derived.QuestionYesNo import QuestionYesNoEnhanced

valid_question = {
    "question_text": "Do you like pizza?",
    "question_options": ["Yes", "No"],
    "question_name": "pizza",
    "short_names_dict": {},
}


def test_QuestionYesNo_construction():
    """Test QuestionYesNo construction."""

    q = QuestionYesNo(**valid_question)
    assert isinstance(q, QuestionYesNoEnhanced)
    assert q.question_name == valid_question["question_name"]
    assert q.question_text == valid_question["question_text"]
    assert q.question_options == valid_question["question_options"]
    assert q.uuid is not None
    assert q.answer_data_model is not None
    assert q.data == valid_question

    no_yes = valid_question.copy()
    no_yes.update({"question_options": ["No", "Yes"]})
    q = QuestionYesNo(**no_yes)

    # should raise an exception if question_options is a list
    invalid_question = valid_question.copy()
    invalid_question.update({"question_options": "question_options"})
    with pytest.raises(Exception):
        QuestionYesNo(**invalid_question)
    # or not exactly == ["Yes", "No"]
    invalid_question.update({"question_options": ["Yes", "No", "Maybe"]})
    with pytest.raises(Exception):
        QuestionYesNo(**invalid_question)


def test_QuestionYesNo_serialization():
    """Test QuestionYesNo serialization."""

    # serialization should add a "type" attribute
    q = QuestionYesNo(**valid_question)
    print(q.to_dict())
    assert q.to_dict() == {
        "question_name": valid_question["question_name"],
        "question_text": valid_question["question_text"],
        "question_options": ["Yes", "No"],
        "type": "yes_no",
        "short_names_dict": {},
    }

    # deserialization should return a QuestionYesNoEnhanced object
    q_lazarus = Question.from_dict(q.to_dict())
    assert isinstance(q_lazarus, QuestionYesNoEnhanced)
    assert type(q) == type(q_lazarus)
    assert repr(q) == repr(q_lazarus)


def test_QuestionYesNo_answers():
    q = QuestionYesNo(**valid_question)
    llm_response_valid1 = {"answer": 0, "comment": "I'm good"}
    llm_response_valid2 = {"answer": 0}
    llm_response_invalid1 = {"comment": "I'm good"}

    # LLM response is required to have an answer key, but is flexible otherwise
    q.validate_response(llm_response_valid1)
    q.validate_response(llm_response_valid2)
    with pytest.raises(QuestionResponseValidationError):
        q.validate_response(llm_response_invalid1)

    # answer must be an integer or interpretable as integer
    q.validate_answer({"answer": 0})
    # TODO: should the following three be allowed?
    q.validate_answer({"answer": "0"})
    q.validate_answer({"answer": True})
    q.validate_answer({"answer": 0, "comment": "I'm good"})
    # answer value required
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": None})
    # answer must be in range of question_options
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": "2"})
    # answer can't be a random string
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": "asdf"})
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [0, 1]})
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": {"answer": 0}})