import logging
import importlib
import sys
import types
from dataclasses import dataclass

# Create lightweight quiz models for testing
class _Column:
    def in_(self, _):
        return self


class Option:
    id = _Column()

    def __init__(self, id: int, text: str, price_impact: float):
        self.id = id
        self.text = text
        self.price_impact = price_impact


class Question:
    id = _Column()

    def __init__(self, id: int, text: str, question_type: str):
        self.id = id
        self.text = text
        self.question_type = question_type

quiz_module = types.ModuleType('quiz_module')
quiz_module.Option = Option
quiz_module.Question = Question

backend_pkg = importlib.import_module('backend')
sys.modules.setdefault('app', backend_pkg)
app_models = types.ModuleType('app.models')
app_models.quiz = quiz_module
sys.modules['app.models'] = app_models
sys.modules['app.models.quiz'] = quiz_module
sys.modules.setdefault('app.schemas', importlib.import_module('backend.schemas'))

from backend.services.lead_calculator import LeadCalculator
from backend.schemas.lead import LeadAnswerIn


class FakeQuery:
    def __init__(self, data):
        self.data = data

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self.data


class FakeSession:
    def __init__(self, options, questions):
        self.options = options
        self.questions = questions

    def query(self, model):
        if model is Option:
            return FakeQuery(self.options)
        if model is Question:
            return FakeQuery(self.questions)
        return FakeQuery([])


def test_calculate_success():
    q1 = Question(id=1, text="Floor", question_type="single-choice")
    opt1 = Option(id=1, text="Tile", price_impact=100.0)
    slider_q = Question(id=2, text="Area", question_type="slider")
    session = FakeSession(options=[opt1], questions=[q1, slider_q])

    answers = [
        LeadAnswerIn(question_id=q1.id, option_id=opt1.id),
        LeadAnswerIn(question_id=slider_q.id, value="2"),
    ]

    calculator = LeadCalculator(log=logging.getLogger("test"))
    price, details = calculator.calculate(session, answers)
    assert price == 200.0
    assert details[q1.text] == opt1.text
    assert details[slider_q.text] == "2.0 м²"


def test_calculate_invalid_area_caplog(caplog):
    q1 = Question(id=1, text="Floor", question_type="single-choice")
    opt1 = Option(id=1, text="Tile", price_impact=100.0)
    slider_q = Question(id=2, text="Area", question_type="slider")
    session = FakeSession(options=[opt1], questions=[q1, slider_q])

    answers = [
        LeadAnswerIn(question_id=q1.id, option_id=opt1.id),
        LeadAnswerIn(question_id=slider_q.id, value="bad"),
    ]

    calculator = LeadCalculator()
    with caplog.at_level(logging.WARNING):
        price, details = calculator.calculate(session, answers)
    assert price == 100.0
    assert slider_q.text not in details
    assert "Invalid area value" in caplog.text