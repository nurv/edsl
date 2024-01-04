import pytest
from edsl.exceptions import (
    QuestionAnswerValidationError,
    QuestionResponseValidationError,
)
from edsl.questions import Question, QuestionRank, Settings
from edsl.questions.QuestionRank import QuestionRankEnhanced

valid_question = {
    "question_text": "What are your 2 favorite foods in the list, ranked?",
    "question_options": ["Pizza", "Ice cream", "Cake", "Cereal"],
    "question_name": "food",
    "num_selections": 2,
    "short_names_dict": {},
}

valid_question_wo_extras = {
    "question_text": "What are your 2 favorite foods in the list, ranked?",
    "question_options": ["Pizza", "Ice cream", "Cake", "Cereal"],
    "question_name": "food",
    "short_names_dict": {},
}


def test_QuestionRank_construction():
    """Test QuestionRank construction."""

    q = QuestionRank(**valid_question)
    assert isinstance(q, QuestionRankEnhanced)
    assert q.question_name == valid_question["question_name"]
    assert q.question_text == valid_question["question_text"]
    assert q.question_options == valid_question["question_options"]
    assert q.num_selections == valid_question["num_selections"]
    assert q.uuid is not None
    assert q.answer_data_model is not None
    assert q.data == valid_question

    # QuestionRank should impute extra fields appropriately
    q = QuestionRank(**valid_question_wo_extras)
    assert q.question_name == valid_question["question_name"]
    assert q.question_text == valid_question["question_text"]
    assert q.question_options == valid_question["question_options"]
    assert q.num_selections == 4
    assert q.uuid is not None
    assert q.answer_data_model is not None
    assert q.data != valid_question_wo_extras
    assert q.data != valid_question

    # should raise an exception if question_text is missing
    invalid_question = valid_question.copy()
    invalid_question.pop("question_text")
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if question_text is empty
    invalid_question = valid_question.copy()
    invalid_question.update({"question_text": ""})
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if question_text is too long
    invalid_question = valid_question.copy()
    invalid_question.update({"question_text": "a" * (Settings.MAX_QUESTION_LENGTH + 1)})
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if unexpected attribute is present
    invalid_question = valid_question.copy()
    invalid_question.update({"unexpected_attribute": "unexpected_attribute"})
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if len(question_options) < num_selections
    invalid_question = valid_question.copy()
    invalid_question.update({"num_selections": 5})
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if options are not unique
    invalid_question = valid_question.copy()
    invalid_question.update({"question_options": ["Pizza", "Pizza", "Cake", "Cereal"]})
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)
    # should raise an exception if options are too long
    invalid_question = valid_question.copy()
    invalid_question.update(
        {"question_options": ["Pizza", "Ice cream", "Cake", "Cereal" * 1000]}
    )
    with pytest.raises(Exception):
        QuestionRank(**invalid_question)


def test_QuestionRank_serialization():
    """Test QuestionRank serialization."""

    # serialization should add a "type" attribute
    q = QuestionRank(**valid_question)
    valid_question_w_type = valid_question.copy()
    valid_question_w_type.update({"type": "rank"})
    assert q.to_dict() == valid_question_w_type
    q = QuestionRank(**valid_question_wo_extras)
    valid_question_w_type = valid_question_wo_extras.copy()
    valid_question_w_type.update({"type": "rank", "num_selections": 4})
    assert q.to_dict() == valid_question_w_type

    # deserialization should return a QuestionRankEnhanced object
    q_lazarus = Question.from_dict(q.to_dict())
    assert isinstance(q_lazarus, QuestionRankEnhanced)
    assert type(q) == type(q_lazarus)
    assert repr(q) == repr(q_lazarus)

    # serialization from bad data should raise an exception
    with pytest.raises(Exception):
        Question.from_dict({"type": "rank"})
    with pytest.raises(Exception):
        Question.from_dict({"type": "rank", "question_text": 1})
    with pytest.raises(Exception):
        Question.from_dict({"type": "rank", "question_text": ""})
    with pytest.raises(Exception):
        Question.from_dict(
            {
                "type": "list",
                "question_text": "What are your 2 favorite foods in the list, ranked?",
                "question_options": ["Pizza", "Ice cream", "Cake", "Cereal"],
                "num_selections": 52,
                "short_names_dict": {},
            }
        )
    with pytest.raises(Exception):
        Question.from_dict(
            {
                "type": "list",
                "question_text": "What are your 2 favorite foods in the list, ranked?",
                "question_options": ["Pizza", "Ice cream", "Cake", "Cereal"],
                "num_selections": 3,
                "kirby": "is cute",
                "short_names_dict": {},
            }
        )


def test_QuestionRank_answers():
    q = QuestionRank(**valid_question)
    response_good = {
        "answer": [2, 1],
        "comment": "You got this!",
    }
    response_bad = {
        "answer": [2, 1],
        "comment": "OK",
        "extra": "extra",
    }
    response_terrible = {"you": "will never be able to do this!"}

    # LLM responses are only required to have an "answer" key
    q.validate_response(response_good)
    with pytest.raises(QuestionResponseValidationError):
        q.validate_response(response_terrible)
    # but can have additional keys
    q.validate_response(response_bad)

    # answer validation
    q.validate_answer(response_good)
    q.validate_answer({"answer": ["2", "1"]})
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer(response_terrible)
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": 1})

    # missing answer
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": []})

    # answer not in options
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [5, 1]})

    # not enough answers
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [1]})

    # too many answers
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [3, 2, 1]})

    # wrong answer type
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": ["Ice cream", "Pizza"]})
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [{"answer": "yooooooooo"}]})
    with pytest.raises(QuestionAnswerValidationError):
        q.validate_answer({"answer": [""]})

    # code -> answer translation
    assert q.translate_answer_code_to_answer(response_good["answer"], None) == [
        "Cake",
        "Ice cream",
    ]


def test_QuestionRank_extras():
    """Test QuestionFreeText extra functionalities."""
    q = QuestionRank(**valid_question)
    # instructions
    assert "You are being asked" in q.instructions
    # simulate_answer
    assert q.simulate_answer().keys() == q.simulate_answer(human_readable=True).keys()
    assert q.simulate_answer(human_readable=False)["answer"][0] in range(
        len(q.question_options)
    )
    simulated_answer = q.simulate_answer()
    assert isinstance(simulated_answer, dict)
    assert "answer" in simulated_answer
    assert "comment" in simulated_answer
    assert isinstance(simulated_answer["answer"], list)
    assert len(simulated_answer["answer"]) > 0
    assert len(simulated_answer["answer"][0]) <= Settings.MAX_ANSWER_LENGTH
    assert simulated_answer["answer"][0] in q.question_options
    # form elements
    form_elements = q.form_elements()
    assert "<label>What are your 2 favorite" in q.form_elements()
    for option in q.question_options:
        assert option in form_elements