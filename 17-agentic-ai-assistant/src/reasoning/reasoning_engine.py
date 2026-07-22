from src.agent.state import AgentState


class ReasoningEngine:

    def __init__(self, llm, executor, planner):
        self.llm = llm
        self.executor = executor
        self.planner = planner

    def think(self, prompt: str):
        return self.llm.generate(prompt)

    def act(self, state: AgentState):

        result = self.executor.execute(
            tool_name=state.selected_tool,
            **state.tool_arguments,
        )

        if result["success"]:
            state.observation = str(result["result"])
        else:
            state.observation = result["error"]

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
        
        if decision.tool == "directory" and "path" not in decision.arguments:
            decision.arguments["path"] = "."

        required_arguments = {
            "calculator": ["expression"],
            "file_reader": ["filepath"],
            "system": [],
            "directory": ["path"],

        }

        required = required_arguments.get(decision.tool, [])

        for argument in required:
            if argument not in decision.arguments:
                raise ValueError(
                    f"{decision.tool} requires '{argument}'. Received: {decision.arguments}"
                )