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

    def initialize(self, services):
        self.services = services

    def next_action(self):
        if self.services.goal_tracking.reached_all_goals():
            return None

        # Get all the current valid options.
        options = self.services.valid_actions.get()

        if len(options) == 0:
            return None

        if len(options) == 1:

            # No need for the current plan, delete it.
            self.plan = []
            return options[0]

        return self._use_plan(options)

    def _use_plan(self, options):
        """
        Returns a step according to a plan.
        :param options: options list
        :return: a step
        """
        if len(self.plan) == 0:
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
        """
        Creates a new plan.
        :return: None
        """
        problem_path = self.services.problem_generator.generate_problem(
            self.services.goal_tracking.uncompleted_goals[0], self.services.perception.get_state())
        self.plan = self.services.planner(self.services.pddl.domain_path, problem_path)


if __name__ == "__main__":
    domain_path = sys.argv[1]
    problem_path = sys.argv[2]

    print LocalSimulator(local).run(domain_path, problem_path, SmartRePlanner())