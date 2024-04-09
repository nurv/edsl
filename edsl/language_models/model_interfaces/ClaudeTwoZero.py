from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_2_0.value

ClaudeTwoZero = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeTwoZero"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeTwoZero
    q = QuestionMultipleChoice.example()
    m = ClaudeTwoZero()
    results = q.by(m).run()
    print(results)