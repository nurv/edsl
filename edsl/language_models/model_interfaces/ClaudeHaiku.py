from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_3_HAIKU.value

ClaudeHaiku = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeHaiku"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeHaiku
    q = QuestionMultipleChoice.example()
    m = ClaudeHaiku()
    results = q.by(m).run()
    print(results)