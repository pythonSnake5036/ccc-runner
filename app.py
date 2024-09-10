import asyncio
from typing import Tuple
from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Collapsible, Header, Footer, Input, DirectoryTree, Button, Label, Static

from runner import run_problems

class TestCaseDisplay(Static):
    test_output: Tuple[Tuple[str, str, str], bool, float, str, str]

    def compose(self) -> ComposeResult:
        test_case, success, elapsed, out, expected = self.test_output

        text = None
        if success:
            text = f"{test_case[0]}: Pass ({elapsed:.2f}s)"
            self.add_class("pass")
        else:
            text = f"{test_case[0]}: Fail ({elapsed:.2f}s)\nOutput:\n{out}\nExpected Output:\n{expected}\n"
            self.add_class("fail")

        yield Label(text)

class CCCRunner(App):
    TITLE = "CCC Runner"
    CSS_PATH = "app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    test_data = ""
    program = ""
    output = reactive("")

    def compose(self) -> ComposeResult:
        yield Header()

        with Collapsible(title="File Tree"):
            yield DirectoryTree("./")

        yield Input(placeholder="Test Data", id="data")
        yield Input(placeholder="Program", id="program")

        yield Button(label="Run", id="run")

        yield ScrollableContainer(id="output")

        yield Footer()

    @on(Input.Changed, "#data")
    def test_data_changed(self, event: Input.Changed) -> None:
        self.test_data = event.value

    @on(Input.Changed, "#program")
    def program_changed(self, event: Input.Changed) -> None:
        self.program = event.value

    async def run_test_cases(self) -> None:
        run = self.query_one("#run")
        run.disabled = True
        output = self.query_one("#output")

        for child in output.children:
            child.remove()

        async for test_case_output in run_problems(self.test_data, self.program):
            test_case_display = TestCaseDisplay()
            test_case_display.test_output = test_case_output
            output.mount(test_case_display)

        run.disabled = False

    @on(Button.Pressed, "#run")
    def start_test(self) -> None:
        asyncio.create_task(self.run_test_cases())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = CCCRunner()
    app.run()

