from edsl.language_models.Anthropic import create_anthropic_model
from edsl.enums import LanguageModelType

model_name = LanguageModelType.ANTHROPIC_3_OPUS.value

ClaudeOpus = create_anthropic_model(
    model_name=model_name, model_class_name="ClaudeOpus"
)

if __name__ == "__main__":

    from edsl import QuestionMultipleChoice
    from edsl.language_models import ClaudeOpus
    q = QuestionMultipleChoice.example()
    m = ClaudeOpus()
    results = q.by(m).run()
    print(results)