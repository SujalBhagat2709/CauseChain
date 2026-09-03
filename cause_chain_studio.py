"""
CauseChain Studio
=================

Interactive interface for the CauseChain system.
"""

from cause_chain import CauseChain


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("CAUSECHAIN STUDIO")
    print("=" * 60)
    print("1. Create Problem")
    print("2. Add Cause")
    print("3. Connect Causes")
    print("4. View All Problems")
    print("5. View Problem Details")
    print("6. Analyze Problem")
    print("7. Show Recommendation")
    print("8. Exit")
    print("=" * 60)


def create_problem(system):
    """Create a new problem."""
    print("\n--- Create Problem ---")

    problem_id = input("Enter problem ID: ").strip()
    title = input("Enter problem title: ").strip()
    description = input("Describe the problem: ").strip()

    success, message = system.create_problem(
        problem_id,
        title,
        description
    )

    print(f"\n{message}")


def add_cause(system):
    """Add a possible cause."""
    print("\n--- Add Cause ---")

    problem_id = input("Enter problem ID: ").strip()

    if not system.get_problem(problem_id):
        print("\nProblem not found.")
        return

    cause = input("Enter cause: ").strip()
    category = input("Enter cause category: ").strip()

    print("\nConfidence:")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    confidence_choice = input("Choose confidence: ").strip()

    confidence_map = {
        "1": "low",
        "2": "medium",
        "3": "high"
    }

    if confidence_choice not in confidence_map:
        print("\nInvalid confidence.")
        return

    evidence = input(
        "Supporting evidence (optional): "
    ).strip()

    success, message = system.add_cause(
        problem_id,
        cause,
        category,
        confidence_map[confidence_choice],
        evidence
    )

    print(f"\n{message}")


def connect_causes(system):
    """Connect a cause to another cause."""
    print("\n--- Connect Causes ---")

    problem_id = input("Enter problem ID: ").strip()

    if not system.get_problem(problem_id):
        print("\nProblem not found.")
        return

    cause = input(
        "Enter the cause that was produced: "
    ).strip()

    parent_cause = input(
        "Enter what caused it: "
    ).strip()

    success, message = system.connect_causes(
        problem_id,
        cause,
        parent_cause
    )

    print(f"\n{message}")


def view_all_problems(system):
    """Display all recorded problems."""
    print("\n--- All Problems ---")

    problems = system.list_problems()

    if not problems:
        print("No problems have been created.")
        return

    for problem_id, problem in problems.items():
        confidence = system.calculate_confidence(problem_id)
        cause_count = len(problem["causes"])

        print(f"\nID: {problem_id}")
        print(f"Title: {problem['title']}")
        print(f"Causes: {cause_count}")
        print(f"Confidence: {confidence}%")


def view_problem_details(system):
    """Display detailed information about a problem."""
    print("\n--- Problem Details ---")

    problem_id = input("Enter problem ID: ").strip()

    if not system.get_problem(problem_id):
        print("\nProblem not found.")
        return

    system.display_problem(problem_id)


def analyze_problem(system):
    """Display a compact analysis."""
    print("\n--- Analyze Problem ---")

    problem_id = input("Enter problem ID: ").strip()

    analysis = system.analyze_problem(problem_id)

    if not analysis:
        print("\nProblem not found.")
        return

    print("\n" + "=" * 60)
    print("CAUSECHAIN SUMMARY")
    print("=" * 60)

    print(f"Problem: {analysis['title']}")
    print(f"Causes Recorded: {analysis['cause_count']}")
    print(f"Overall Confidence: {analysis['confidence']}%")
    print(f"Evidence Gaps: {analysis['evidence_gaps']}")

    print("\nCause Chain:")

    if analysis["chain"]:
        print("  " + "  →  ".join(analysis["chain"]))
    else:
        print("  No connected chain available.")

    print("\nRecommendation:")
    print(f"  {analysis['recommendation']}")

    print("=" * 60)


def show_recommendation(system):
    """Display investigation recommendation."""
    print("\n--- Investigation Recommendation ---")

    problem_id = input("Enter problem ID: ").strip()

    if not system.get_problem(problem_id):
        print("\nProblem not found.")
        return

    print("\nRecommendation:")
    print(system.generate_recommendation(problem_id))


def main():
    """Run CauseChain Studio."""
    system = CauseChain()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_problem(system)

        elif choice == "2":
            add_cause(system)

        elif choice == "3":
            connect_causes(system)

        elif choice == "4":
            view_all_problems(system)

        elif choice == "5":
            view_problem_details(system)

        elif choice == "6":
            analyze_problem(system)

        elif choice == "7":
            show_recommendation(system)

        elif choice == "8":
            print("\nThank you for using CauseChain Studio.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
