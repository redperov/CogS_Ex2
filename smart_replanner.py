from pddlsim.local_simulator import LocalSimulator
from pddlsim.executors.executor import Executor
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

    def initialize(self, services):
        self.services = services
        # self.steps = services.planner(
        #     services.pddl.domain_path, services.pddl.problem_path)

    def next_action(self):
        if self.services.goal_tracking.reached_all_goals():
            return None

        # Get all the current valid options.
        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None

        if len(options) == 1:

            # No need for the current plan.
            self.plan = []
            print("Using options")
            return options[0]

        return self._use_plan(options)

    def _use_plan(self, options):
        if len(self.plan) == 0:
            print("Creating new plan")
            self._create_plan()

        # The next step according to the current plan.
        plan_step = self.plan.pop(0).lower()

        # Check if the next step according to the plan is valid.
        if plan_step in options:
            return plan_step

        # If the plan step is not in options, something changed in the world, re-plan.
        self.plan = []
        return self._use_plan(options)

    def _create_plan(self):
        problem_path = self.services.problem_generator.generate_problem(
            self.services.goal_tracking.uncompleted_goals[0], self.services.perception.get_state())
        self.plan = self.services.planner(self.services.pddl.domain_path, problem_path)

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


if __name__ == "__main__":
    domain_path = sys.argv[1]
    problem_path = sys.argv[2]

    print LocalSimulator(local).run(domain_path, problem_path, SmartRePlanner())
