from rcsbsearchapi.search import TextQuery

q1 = TextQuery("hemoglobin")
for idscore in list(q1(results_verbosity="verbose")):
    print(idscore)