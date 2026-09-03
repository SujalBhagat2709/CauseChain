"""
CauseChain
==========

A small Python OOP system for tracing a problem backward through
possible causes.

Real-life problem:
When something goes wrong, the visible problem is often only a symptom.
The actual cause may be several steps deeper.

CauseChain helps build a cause → effect chain and analyze it.
"""


class CauseChain:
    """Stores problems, causes, and relationships between them."""

    def __init__(self):
        self.problems = {}

    def create_problem(self, problem_id, title, description):
        """Create a new problem investigation."""
        if problem_id in self.problems:
            return False, "Problem ID already exists."

        self.problems[problem_id] = {
            "title": title,
            "description": description,
            "causes": []
        }

        return True, "Problem created successfully."

    def add_cause(
        self,
        problem_id,
        cause,
        category,
        confidence="medium",
        evidence=""
    ):
        """Add a possible cause to a problem."""
        if problem_id not in self.problems:
            return False, "Problem not found."

        valid_confidence = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        confidence = confidence.lower()

        if confidence not in valid_confidence:
            return False, "Confidence must be Low, Medium, or High."

        cause_data = {
            "cause": cause,
            "category": category,
            "confidence": confidence,
            "confidence_score": valid_confidence[confidence],
            "evidence": evidence,
            "parent": None
        }

        self.problems[problem_id]["causes"].append(cause_data)

        return True, "Cause added successfully."

    def connect_causes(
        self,
        problem_id,
        cause,
        parent_cause
    ):
        """
        Connect one cause to another.

        Example:

        Server Overloaded
                ↓
        API Requests Increased
                ↓
        Traffic Spike

        Here 'Server Overloaded' can be connected to
        'API Requests Increased'.
        """
        if problem_id not in self.problems:
            return False, "Problem not found."

        causes = self.problems[problem_id]["causes"]

        cause_item = self._find_cause(causes, cause)
        parent_item = self._find_cause(causes, parent_cause)

        if not cause_item:
            return False, "Cause not found."

        if not parent_item:
            return False, "Parent cause not found."

        if cause == parent_cause:
            return False, "A cause cannot be connected to itself."

        cause_item["parent"] = parent_cause

        return True, "Cause relationship created successfully."

    def _find_cause(self, causes, cause_name):
        """Find a cause by name."""
        for item in causes:
            if item["cause"].lower() == cause_name.lower():
                return item

        return None

    def get_problem(self, problem_id):
        """Return a problem."""
        return self.problems.get(problem_id)

    def get_root_causes(self, problem_id):
        """
        Return causes that do not have another cause above them.

        A root cause here means the deepest cause currently recorded
        in the investigation chain.
        """
        problem = self.get_problem(problem_id)

        if not problem:
            return []

        causes = problem["causes"]

        return [
            item
            for item in causes
            if item["parent"] is None
        ]

    def get_leaf_causes(self, problem_id):
        """
        Find causes that are not parents of another cause.

        These represent possible starting points for deeper investigation.
        """
        problem = self.get_problem(problem_id)

        if not problem:
            return []

        causes = problem["causes"]

        parent_names = {
            item["parent"].lower()
            for item in causes
            if item["parent"] is not None
        }

        return [
            item
            for item in causes
            if item["cause"].lower() not in parent_names
        ]

    def calculate_confidence(self, problem_id):
        """
        Calculate average confidence across recorded causes.
        """
        problem = self.get_problem(problem_id)

        if not problem or not problem["causes"]:
            return 0

        total = sum(
            item["confidence_score"]
            for item in problem["causes"]
        )

        maximum = len(problem["causes"]) * 3

        return round((total / maximum) * 100, 2)

    def count_evidence_gaps(self, problem_id):
        """Count causes where supporting evidence is missing."""
        problem = self.get_problem(problem_id)

        if not problem:
            return 0

        return sum(
            1
            for item in problem["causes"]
            if not item["evidence"].strip()
        )

    def get_chain(self, problem_id):
        """
        Build cause chain from a recorded cause toward its
        connected parent causes.
        """
        problem = self.get_problem(problem_id)

        if not problem:
            return []

        causes = problem["causes"]

        if not causes:
            return []

        leaf_causes = self.get_leaf_causes(problem_id)

        if not leaf_causes:
            return []

        chain = []
        current = leaf_causes[0]

        visited = set()

        while current:
            cause_name = current["cause"]

            if cause_name.lower() in visited:
                break

            visited.add(cause_name.lower())
            chain.append(cause_name)

            parent_name = current["parent"]

            if not parent_name:
                break

            current = self._find_cause(causes, parent_name)

        return chain

    def find_high_confidence_causes(self, problem_id):
        """Return causes supported with high confidence."""
        problem = self.get_problem(problem_id)

        if not problem:
            return []

        return [
            item
            for item in problem["causes"]
            if item["confidence"] == "high"
        ]

    def generate_recommendation(self, problem_id):
        """Generate a simple investigation recommendation."""
        problem = self.get_problem(problem_id)

        if not problem:
            return "Problem not found."

        if not problem["causes"]:
            return (
                "No causes have been recorded. Start by identifying "
                "possible causes of the problem."
            )

        gaps = self.count_evidence_gaps(problem_id)
        confidence = self.calculate_confidence(problem_id)
        chain = self.get_chain(problem_id)

        if gaps > 0:
            return (
                f"{gaps} cause(s) have no supporting evidence. "
                "Collect evidence before treating them as confirmed causes."
            )

        if confidence < 50:
            return (
                "Overall confidence is low. Investigate the recorded "
                "causes further before reaching a conclusion."
            )

        if len(chain) <= 1:
            return (
                "The cause chain is shallow. Consider asking why the "
                "identified cause happened."
            )

        if confidence >= 80:
            return (
                "The investigation has strong supporting confidence. "
                "Review the deepest cause and confirm it with evidence."
            )

        return (
            "The cause chain is useful but should be validated with "
            "additional evidence."
        )

    def analyze_problem(self, problem_id):
        """Return a complete problem analysis."""
        problem = self.get_problem(problem_id)

        if not problem:
            return None

        chain = self.get_chain(problem_id)

        return {
            "id": problem_id,
            "title": problem["title"],
            "description": problem["description"],
            "cause_count": len(problem["causes"]),
            "confidence": self.calculate_confidence(problem_id),
            "evidence_gaps": self.count_evidence_gaps(problem_id),
            "root_causes": self.get_root_causes(problem_id),
            "leaf_causes": self.get_leaf_causes(problem_id),
            "chain": chain,
            "high_confidence_causes": (
                self.find_high_confidence_causes(problem_id)
            ),
            "recommendation": self.generate_recommendation(problem_id)
        }

    def display_problem(self, problem_id):
        """Display the complete problem investigation."""
        analysis = self.analyze_problem(problem_id)

        if not analysis:
            print("\nProblem not found.")
            return

        print("\n" + "=" * 60)
        print("CAUSECHAIN ANALYSIS")
        print("=" * 60)

        print(f"ID: {analysis['id']}")
        print(f"Title: {analysis['title']}")
        print(f"Description: {analysis['description']}")

        print(f"\nCauses Recorded: {analysis['cause_count']}")
        print(f"Overall Confidence: {analysis['confidence']}%")
        print(f"Evidence Gaps: {analysis['evidence_gaps']}")

        print("\nCause Chain:")

        if analysis["chain"]:
            print("  " + "  →  ".join(analysis["chain"]))
        else:
            print("  No connected cause chain available.")

        print("\nRecorded Causes:")

        if not self.problems[problem_id]["causes"]:
            print("  No causes recorded.")
        else:
            for number, item in enumerate(
                self.problems[problem_id]["causes"],
                start=1
            ):
                print(f"\n  {number}. {item['cause']}")
                print(f"     Category: {item['category']}")
                print(f"     Confidence: {item['confidence'].title()}")
                print(
                    "     Evidence: "
                    + (
                        item["evidence"]
                        if item["evidence"].strip()
                        else "Not provided"
                    )
                )

                if item["parent"]:
                    print(f"     Caused By: {item['parent']}")
                else:
                    print("     Caused By: None recorded")

        print("\nRecommendation:")
        print(f"  {analysis['recommendation']}")

        print("=" * 60)

    def list_problems(self):
        """Return all stored problems."""
        return self.problems
