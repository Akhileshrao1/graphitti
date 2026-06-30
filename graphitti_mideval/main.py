import json
from datetime import datetime

from parser import Parser
from processor import Processor


def main():

    parser = Parser()
    processor = Processor()

    with open("output/python_docs.json","r",encoding="utf-8") as file:
        pages = json.load(file)
    
    graph_output = {
        "metadata": {
            "project": "Graphitti",
            "source": pages[0]["url"] if pages else "",
            "pages_crawled": len(pages),
            "generated_at": str(datetime.now())
        },
        "text_chunks": [],
        "triples": []
    }

    seen_chunks = set()
    seen_triples = set()

    for page in pages:
        page = parser.parse(page)
        for chunk in page["chunks"]:
            if chunk not in seen_chunks:
                seen_chunks.add(chunk)
                graph_output["text_chunks"].append(chunk)
            entities, triples = processor.process(
                chunk,
                page["url"]
            )

            for triple in triples:
                key = (
                    triple["subject"],
                    triple["predicate"],
                    triple["object"]
                )

                if key not in seen_triples:
                    seen_triples.add(key)
                    graph_output["triples"].append(triple)

    with open("output/graph_output.json","w",encoding="utf-8") as file:
        json.dump(graph_output,file,indent=4,ensure_ascii=False)

    print()
    print("Done!")
    print("------------------------")
    print("Pages   :", len(pages))
    print("Chunks  :", len(graph_output["text_chunks"]))
    print("Triples :", len(graph_output["triples"]))
    print("------------------------")
if __name__ == "__main__":
    main()