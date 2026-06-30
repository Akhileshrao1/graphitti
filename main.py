from graph import graph


def main():

    print("=" * 60)
    print("      Graphitti Multi-Retriever QA System")
    print("=" * 60)

    print("\nType 'exit' to quit.\n")

    while True:

        question = input("Ask a question: ")

        if question.lower() == "exit":
            break

        state = {
            "question": question,
            "strategy": "",
            "context": "",
            "answer": ""
        }

        result = graph.invoke(state)

        print("\nStrategy :", result["strategy"])
        print("\nAnswer :\n")
        print(result["answer"])
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()