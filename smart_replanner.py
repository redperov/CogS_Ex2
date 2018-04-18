from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.executor import Executor
from pddlsim.parser_independent import PreconditionFalseError
from pddlsim.planner import local
import sys


class SmartRePlanner(Executor):
    """
    This planner plans only if there is more than one legal action to take.
    """

    def __init__(self):
        super(SmartRePlanner, self).__init__()
        self.steps = []
        self.services = None
        self.plan = []
        self.k = 5  # TODO maybe use k to perform k actions instead of only one like now
        self.previous_states = [] # TODO maybe save only the last state
        # self.counter = -1

    def initialize(self, services):
        self.services = services

    def next_action(self):
        # TODO idea: save previous states, apply all options on current state, if one doesn't lead to the previous states, choose it
        if self.services.goal_tracking.reached_all_goals():
            return None

        # self.counter += 1

        # Get all the current valid options.
        options = self.services.valid_actions.get()
        # print("Number of valid actions: " + str(len(options)))

        if len(options) == 0:
            return None

        if len(options) == 1:
            # No need for the current plan.
            self.plan = []
            # TODO delete
            print("Using options")
            # Add current state to the closed list.
            current_state = self.services.perception.get_state()
            self.previous_states.append(current_state)
            return options[0]

        untaken_option = self._look_for_one_new_option(options)

        # If found an untaken option, return it.
        if untaken_option is not None:
            print("Using untaken step")
            return untaken_option

        return self._use_plan(options)

    def _look_for_one_new_option(self, options):
        """
        Looks if there is one new option that isn't in the closed list.
        :param options: options list
        :return: option
        """
        current_state = self.services.perception.get_state()
        untaken_option = None
        counter = 0

        # Apply all options on the current state.
        for option in options:

            future_state = current_state

            # Check if the future state already appeared in the closed list.
            try:
                self.services.pddl.apply_action_to_state(option, future_state)
            except Exception:
                future_state = None

            if future_state is not None and future_state not in self.previous_states:
                untaken_option = option
                counter += 1
            if counter > 1:
                return None

        return untaken_option

    def _use_plan(self, options):

        # If plan is empty, create a new plan.
        if len(self.plan) == 0:
            print("Creating new plan")
            self._create_plan()

        # The next step according to the current plan.
        plan_step = self.plan.pop(0).lower()

        # Check if the next step according to the plan is valid.
        if plan_step in options:

            # Add the current state to the closed list.
            current_state = self.services.perception.get_state()
            self.previous_states.append(current_state)

            return plan_step

        # If the plan step is not in options, something changed in the world, re-plan.
        self.plan = []
        return self._use_plan(options)

    def _create_plan(self):
        problem_path = self.services.problem_generator.generate_problem(
            self.services.goal_tracking.uncompleted_goals[0], self.services.perception.get_state())
        self.plan = self.services.planner(self.services.pddl.domain_path, problem_path)


if __name__ == "__main__":
    domain_path = sys.argv[1]
    problem_path = sys.argv[2]

    print LocalSimulator(local).run(domain_path, problem_path, SmartRePlanner())

    # if len(self.plan) > 0:
    #     return self._use_plan()
    #
    # options = self.services.valid_actions.get()
    # if len(options) == 0:
    #     return None
    # if len(options) == 1:
    #     return options[0]
    #
    # self._plan_k_steps_ahead()
    # return self._use_plan()

    # if len(self.steps) > 0:
    #     return self.steps.pop(0).lower()
    # return None

    # def _use_plan(self):
    #     if len(self.plan) > 0:
    #         return self.plan.pop(0).lower()
    #     return None
    #
    # def _plan_k_steps_ahead(self):
    #     problem_path = self.services.problem_generator.generate_problem(
    #         self.services.goal_tracking.uncompleted_goals[0], self.services.perception.get_state())
    #     self.plan = self.services.planner(self.services.pddl.domain_path, problem_path)
    #
    #     print(len(self.plan))
    #     # Trim the list to length <= k.
    #     self.plan = self.plan[:self.k]
