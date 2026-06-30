import spacy


class Processor:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

        self.ignore = {
            "he", "she", "it", "they", "them",
            "this", "that", "these", "those",
            "who", "which", "we", "you", "i"
        }

        self.predicate_map = {
            "raise": "RAISES",
            "throw": "RAISES",

            "return": "RETURNS",
            "yield": "YIELDS",

            "accept": "ACCEPTS",
            "pass": "PASSES",

            "call": "CALLS",
            "invoke": "CALLS",

            "import": "IMPORTS",
            "export": "EXPORTS",

            "inherit": "INHERITS",
            "extend": "EXTENDS",

            "override": "OVERRIDES",

            "instantiate": "INSTANTIATES",

            "instantiate": "CREATES_INSTANCE",

            "iterate": "ITERATES",

            "evaluate": "EVALUATES",

            "convert": "CONVERTS_TO",

            "encode": "ENCODES",

            "decode": "DECODES",

            "serialize": "SERIALIZES",

            "deserialize": "DESERIALIZES",

            "compare": "COMPARES",

            "sort": "SORTS",

            "index": "INDEXES",

            "reference": "REFERENCES",

            "represent": "REPRESENTS",

            "belong": "BELONGS_TO",

            "derive": "DERIVES_FROM",

            "subclass": "SUBCLASSES",

            "instantiate": "INSTANTIATES",

            "contain": "CONTAINS",

            "consist": "CONSISTS_OF",

            "wrap": "WRAPS",

            "embed": "EMBEDS",

            "expose": "EXPOSES",

            "represent": "REPRESENTS",

            "map": "MAPS_TO",

            "resolve": "RESOLVES",

            "search": "SEARCHES",

            "locate": "LOCATES",
            "refer":"REFERENCES",
            "mention":"MENTIONS",

            "reference": "REFERENCES",

            "replace": "REPLACES",

            "remove": "REMOVES",

            "delete": "DELETES",

            "append": "APPENDS",

            "insert": "INSERTS",

            "update": "UPDATES",

            "modify": "MODIFIES",

            "use": "USES",
            "utilize": "USES",

            "support": "SUPPORTS",

            "provide": "PROVIDES",
            "offer": "PROVIDES",

            "contain": "CONTAINS",
            "include": "INCLUDES",

            "allow": "ALLOWS",
            "enable": "ENABLES",
            "permit": "PERMITS",

            "require": "REQUIRES",
            "need": "REQUIRES",
            "depend": "DEPENDS_ON",

            "implement": "IMPLEMENTS",
            "define": "DEFINES",
            "describe": "DESCRIBES",
            "represent": "REPRESENTS",

            "create": "CREATES",
            "build": "BUILDS",
            "develop": "DEVELOPS",
            "generate": "GENERATES",

            "produce": "PRODUCES",
            "construct": "CONSTRUCTS",

            "install": "INSTALLS",
            "configure": "CONFIGURES",
            "initialize": "INITIALIZES",

            "run": "RUNS",
            "execute": "EXECUTES",
            "compile": "COMPILES",
            "interpret": "INTERPRETS",

            "parse": "PARSES",
            "extract": "EXTRACTS",
            "process": "PROCESSES",
            "analyze": "ANALYZES",
        
            "read": "READS",
            "write": "WRITES",
            "load": "LOADS",
            "save": "SAVES",
            "store": "STORES",
    
            "access": "ACCESSES",
            "retrieve": "RETRIEVES",
            "fetch": "FETCHES",
    
            "connect": "CONNECTS_TO",
            "communicate": "COMMUNICATES_WITH",
            "send": "SENDS",
            "receive": "RECEIVES",
    
            "return": "RETURNS",
            "call": "CALLS",
            "invoke": "INVOKES",
    
            "extend": "EXTENDS",
            "inherit": "INHERITS",
            "derive": "DERIVES_FROM",
    
            "convert": "CONVERTS",
            "transform": "TRANSFORMS",
    
            "compare": "COMPARES",
            "match": "MATCHES",
    
            "display": "DISPLAYS",
            "show": "SHOWS",
            "print": "PRINTS",
    
            "validate": "VALIDATES",
            "verify": "VERIFIES",
            "check": "CHECKS",
    
            "manage": "MANAGES",
            "handle": "HANDLES",
            "control": "CONTROLS",
            "monitor": "MONITORS",
    
            "optimize": "OPTIMIZES",
            "improve": "IMPROVES",
            "reduce": "REDUCES",
            "increase": "INCREASES",
    
            "link": "LINKS_TO",
            "reference": "REFERENCES",
            "relate": "RELATES_TO",
    
            "share": "SHARES",
            "publish": "PUBLISHES",
    
            "start": "STARTS",
            "stop": "STOPS",
    
            "learn": "LEARNS",
            "train": "TRAINS",
            "predict": "PREDICTS",
    
            "encode": "ENCODES",
            "decode": "DECODES",
    
            "import": "IMPORTS",
            "export": "EXPORTS"
    }

    def valid_entity(self, text):

        if not text:
            return False

        text = text.strip()

        if len(text) < 2:
            return False

        if text.lower() in self.ignore:
            return False

        if text.startswith("\\"):
            return False

        return True

    def valid_predicate(self, predicate):

        if not predicate:
            return False

        return predicate in self.predicate_map

    def process(self, text, source_url):

        doc = self.nlp(text)

        entities = []

        triples = []

        seen_entities = set()

        seen_triples = set()

        for ent in doc.ents:

            if not self.valid_entity(ent.text):
                continue

            key = (
                ent.text,
                ent.label_
            )

            if key not in seen_entities:

                seen_entities.add(key)

                entities.append({

                    "text": ent.text,

                    "label": ent.label_

                })

        for sent in doc.sents:

            subject = None
            predicate = None
            object_ = None

            for token in sent:
              

    # Subject
                if token.dep_ in ("nsubj", "nsubjpass"):

                    if token.pos_ in ("NOUN", "PROPN"):

                     subject = " ".join(w.text for w in token.subtree)

    # Main verb
                elif token.dep_ == "ROOT" and token.pos_ == "VERB":

                     predicate = token.lemma_.upper()

    # Active voice object
                elif token.dep_ in ("dobj", "obj", "attr","pobj","dative","oprd"):

                    if token.pos_ in ("NOUN", "PROPN"):

                       object_ = " ".join(w.text for w in token.subtree)

    # Passive voice: by + PERSON/ORG
                elif token.dep_ == "agent":

                    for child in token.children:

                        if child.dep_ == "pobj":

                            object_ = " ".join(
                               w.text for w in child.subtree
                           )

                            if predicate == "CREATE":
                                predicate = "CREATED_BY"

                            elif predicate == "DEVELOP":
                                 predicate = "DEVELOPED_BY"

                            elif predicate == "WRITE":
                                predicate = "WRITTEN_BY"

                            elif predicate == "DESIGN":
                                predicate = "DESIGNED_BY"


                    if (
                        token.pos_ in ("NOUN", "PROPN")
                        and self.valid_entity(token.text)
                    ):

                        obj = " ".join(
                            word.text
                            for word in token.subtree
                        )

            if not (
                subject and
                predicate and
                object_
            ):
                continue

            key = (
                subject,
                predicate,
                object_
            )

            if key in seen_triples:
                continue

            seen_triples.add(key)

            triples.append({

                "subject": subject,

                "predicate": predicate,

                "object": object_,

                "source_url": source_url

            })

        return entities, triples
