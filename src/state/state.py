import json
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine

from src.config import Config

class StateModel(SQLModel, table=True):
    __tablename__ = "state"

    id: Optional[int] = Field(default=None, primary_key=True)
    command: str
    state_stack_json: str

class State:
    def __init__(self):
        config = Config()
        sqlite_path = config.get_sqlite_db()
        self.engine = create_engine(f"sqlite:///{sqlite_path}")
        SQLModel.metadata.create_all(self.engine)

    def new_state(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "internal_monologue": None,
            "browser_session": {
                "url": None,
                "screenshot": None
            },
            "terminal_session": {
                "command": None,
                "output": None,
                "title": None
            },
            "step": None,
            "message": None,
            "completed": False,
            "is_active": True,
            "token_usage": 0,
            "timestamp": timestamp
        }

    def delete_state(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                session.delete(state)
                session.commit()

    def add_to_current_state(self, command: str, state: dict):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                state_stack = json.loads(state.state_stack_json)
                state_stack.append(state)
                state.state_stack_json = json.dumps(state_stack)
                session.commit()
            else:
                state_stack = [state]
                state = StateModel(command=command, state_stack_json=json.dumps(state_stack))
                session.add(state)
                session.commit()

    def get_current_state(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                return json.loads(state.state_stack_json)
            return None

    def update_latest_state(self, command: str, state: dict):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                state_stack = json.loads(state.state_stack_json)
                state_stack[-1] = state
                state.state_stack_json = json.dumps(state_stack)
                session.commit()
            else:
                state_stack = [state]
                state = StateModel(command=command, state_stack_json=json.dumps(state_stack))
                session.add(state)
                session.commit()

    def get_latest_state(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                return json.loads(state.state_stack_json)[-1]
            return None

    def set_active(self, command: str, is_active: bool):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                state_stack = json.loads(state.state_stack_json)
                state_stack[-1]["is_active"] = is_active
                state.state_stack_json = json.dumps(state_stack)
                session.commit()
            else:
                state_stack = [self.new_state()]
                state_stack[-1]["is_active"] = is_active
                state = StateModel(command=command, state_stack_json=json.dumps(state_stack))
                session.add(state)
                session.commit()

    def is_active(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                return json.loads(state.state_stack_json)[-1]["is_active"]
            return None

    def set_completed(self, command: str, is_completed: bool):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                state_stack = json.loads(state.state_stack_json)
                state_stack[-1]["internal_monologue"] = "Agent has completed the task."
                state_stack[-1]["completed"] = is_completed
                state.state_stack_json = json.dumps(state_stack)
                session.commit()
            else:
                state_stack = [self.new_state()]
                state_stack[-1]["completed"] = is_completed
                state = StateModel(command=command, state_stack_json=json.dumps(state_stack))
                session.add(state)
                session.commit()

    def is_completed(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                return json.loads(state.state_stack_json)[-1]["completed"]
            return None
            
    def update_token_usage(self, command: str, token_usage: int):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                state_stack = json.loads(state.state_stack_json)
                state_stack[-1]["token_usage"] += token_usage
                state.state_stack_json = json.dumps(state_stack)
                session.commit()
            else:
                state_stack = [self.new_state()]
                state_stack[-1]["token_usage"] = token_usage
                state = StateModel(command=command, state_stack_json=json.dumps(state_stack))
                session.add(state)
                session.commit()

    def get_latest_token_usage(self, command: str):
        with Session(self.engine) as session:
            state = session.query(StateModel).filter(StateModel.command == command).first()
            if state:
                return json.loads(state.state_stack_json)[-1]["token_usage"]
            return 0
