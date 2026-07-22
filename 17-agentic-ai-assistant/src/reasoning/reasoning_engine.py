from src.agent.state import AgentState


class ReasoningEngine:
    """
    Handles the Think → Act → Observe cycle.
    """

    def __init__(self, llm, executor, planner):
        self.llm = llm
        self.executor = executor
        self.planner = planner

    def think(self, prompt: str):
        """
        Ask the LLM what to do next.
        """
        return self.llm.generate(prompt)

    def act(self, state: AgentState):
        """
        Execute the selected tool.
        """

        result = self.executor.execute(
            tool_name=state.selected_tool,
            **state.tool_arguments,
        )

        state.observation = str(result["result"])
        state.tool_calls.append(result)
        state.iterations += 1

        return result
    
    def observe(self, state: AgentState):

        if state.observation:
            state.final_answer = state.observation
            state.finished = True
    
    def run_loop(self, state: AgentState, prompt: str):

        MAX_ITERATIONS = 5

        while not state.finished and state.iterations < MAX_ITERATIONS:

            print(f"\n========== Iteration {state.iterations + 1} ==========")

            # THINK
            decision = self.think(prompt)

            # Validate the decision
            self.validate_decision(decision)

            # Update state
            state.current_thought = decision.reason
            state.selected_tool = decision.tool
            state.tool_arguments = decision.arguments

            # ACT
            result = self.act(state)

            # OBSERVE
            self.observe(state)

        return result
    
    
    def validate_decision(self, decision):

        if not decision.tool:
            raise ValueError("No tool selected by the LLM.")

        if decision.arguments is None:
            raise ValueError("Tool arguments cannot be None.")

        if decision.tool == "calculator":

            if "expression" not in decision.arguments:

                raise ValueError(
                    f"Calculator requires 'expression'. Received: {decision.arguments}"
                )