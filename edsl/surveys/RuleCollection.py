from typing import List, Union
from collections import defaultdict

from edsl.exceptions import (
    SurveyRuleCannotEvaluateError,
    SurveyRuleCollectionHasNoRulesAtNodeError,
)
from edsl.utilities.interface import print_table_with_rich
from edsl.surveys.Rule import Rule
from edsl.surveys.base import EndOfSurvey


from collections import namedtuple

NextQuestion = namedtuple(
    "NextQuestion", "next_q, num_rules_found, expressions_evaluating_to_true, priority"
)

## We're going to need the survey object itself
## so we know how long the survey is, unless we move


class RuleCollection:
    "A collection of rules for a particular survey"

    def __init__(self, num_questions: int = None, rules: List[Rule] = None):
        self.rules = rules or []
        self.num_questions = num_questions

    def __len__(self):
        return len(self.rules)

    def __getitem__(self, index):
        return self.rules[index]

    def __repr__(self):
        return f"RuleCollection(rules = {self.rules})"

    def to_dict(self):
        return {
            "rules": [rule.to_dict() for rule in self.rules],
            "num_questions": self.num_questions,
        }

    @classmethod
    def from_dict(cls, rule_collection_dict):
        rules = [
            Rule.from_dict(rule_dict) for rule_dict in rule_collection_dict["rules"]
        ]
        num_questions = rule_collection_dict["num_questions"]
        new_rc = cls(rules=rules)
        new_rc.num_questions = num_questions
        return new_rc

    def add_rule(self, rule: Rule):
        """Adds a rule to a survey. If it's not, return human-readable complaints"""
        self.rules.append(rule)

    def show_rules(self) -> None:
        keys = ["current_q", "expression", "next_q", "priority"]
        rule_list = []
        for rule in sorted(self.rules, key=lambda r: r.current_q):
            rule_list.append({k: getattr(rule, k) for k in keys})

        print_table_with_rich(rule_list)

    def applicable_rules(self, q_now) -> list:
        """Which rules apply at the current node?

        >>> rule_collection = RuleCollection.example()
        >>> rule_collection.applicable_rules(1)
        [Rule(current_q=1, expression="q1 == 'yes'", next_q=3, priority=1, question_name_to_index={'q1': 1}), Rule(current_q=1, expression="q1 == 'no'", next_q=2, priority=1, question_name_to_index={'q1': 1})]

        More than one rule can apply. E.g., suppose we are at node 1.
        We could have three rules:
        1. "q1 == 'a' ==> 3
        2. "q1 == 'b' ==> 4
        3. "q1 == 'c' ==> 5
        """
        return [rule for rule in self.rules if rule.current_q == q_now]

    def next_question(self, q_now, answers) -> int:
        "Find the next question by index, given the rule collection"
        # what rules apply at the current node?

        # tracking
        expressions_evaluating_to_true = 0
        next_q = None
        highest_priority = -2  # start with -2 to 'pick up' the default rule added
        num_rules_found = 0

        for rule in self.applicable_rules(q_now):
            num_rules_found += 1
            try:
                if rule.evaluate(answers):  # evaluates to True
                    expressions_evaluating_to_true += 1
                    if rule.priority > highest_priority:  # higher priority
                        # we have a new champ!
                        next_q, highest_priority = rule.next_q, rule.priority
            except SurveyRuleCannotEvaluateError:
                raise

        if num_rules_found == 0:
            raise SurveyRuleCollectionHasNoRulesAtNodeError(
                f"No rules found for question {q_now}"
            )

        return NextQuestion(
            next_q, num_rules_found, expressions_evaluating_to_true, highest_priority
        )

    @property
    def non_default_rules(self) -> List[Rule]:
        """Returns all rules that are not the default rule"
        >>> rule_collection = RuleCollection.example()
        >>> len(rule_collection.non_default_rules)
        2
        """
        return [rule for rule in self.rules if rule.priority > -1]

    def keys_between(self, start_q, end_q, right_inclusive=True):
        """Returns a list of all question indices between start_q and end_q
        >>> rule_collection = RuleCollection(num_questions=5)
        >>> rule_collection.keys_between(1, 3)
        [2, 3]
        >>> rule_collection.keys_between(1, 4)
        [2, 3, 4]
        >>> rule_collection.keys_between(1, EndOfSurvey, right_inclusive=False)
        [2, 3, 4]
        """

        if end_q == EndOfSurvey:
            # If it's the end of the survey,
            # all questions between the start_q and the end of the survey
            # now depend on the start_q
            if self.num_questions is None:
                raise ValueError(
                    "Cannot determine DAG when EndOfSurvey and when num_questions is not known"
                )
            end_q = self.num_questions

        question_range = list(range(start_q + 1, end_q + int(right_inclusive)))

        return question_range

    @property
    def dag(self) -> dict:
        """
        Finds the DAG of the survey based on the skip logic.
        They key is parent node, the value is a set of child nodes.

        >>> rule_collection = RuleCollection(num_questions=5)
        >>> qn2i = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}
        >>> rule_collection.add_rule(Rule(current_q=1, expression="q1 == 'yes'", next_q=3, priority=1,  question_name_to_index = qn2i))
        >>> rule_collection.add_rule(Rule(current_q=1, expression="q1 == 'no'", next_q=2, priority=1, question_name_to_index = qn2i))
        >>> rule_collection.dag
        {2: {1}, 3: {1}}
        """
        parent_to_children = defaultdict(set)
        ## Rules are desgined at the current question and then direct where
        ## control goes next. As such, the destination nodes are the keys
        ## and the current nodes are the values. Furthermore, all questions between
        ## the current and destination nodes are also included as keys, as they will depend
        ## on the answer to the focal node as well.

        ## If we have a rule that says "if q1 == 'yes', go to q3",
        ## Then q3 depends on q1, but so does q2
        ## So the DAG would be {3: [1], 2: [1]}

        # we are only interested in non-default rules. Default rules are those
        # that just go to the next question, so they don't add any dependencies
        for rule in self.non_default_rules:
            current_q, next_q = rule.current_q, rule.next_q
            for q in self.keys_between(current_q, next_q):
                parent_to_children[q].add(current_q)
        return dict(sorted(parent_to_children.items()))

    @classmethod
    def example(cls):
        qn2i = {"q1": 1, "q2": 2, "q3": 3, "q4": 4}
        return cls(
            num_questions=5,
            rules=[
                Rule(
                    current_q=1,
                    expression="q1 == 'yes'",
                    next_q=3,
                    priority=1,
                    question_name_to_index=qn2i,
                ),
                Rule(
                    current_q=1,
                    expression="q1 == 'no'",
                    next_q=2,
                    priority=1,
                    question_name_to_index=qn2i,
                ),
            ],
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
