import json

standard = {}
by_category = {}
as_table = {}

list_categories = [
	("CC", "Counting & Cardinality"),
	("OA", "Operations & Algebraic Thinking"),
	("NBT", "Number & Operations in Base 10"),
	("NF", "Number & Operations - Fractions"),
	("MD", "Measurement & Data"),
	("G", "Geometry"),
	("RP", "Ratios & Proportional Relationships"),
	("NS", "The Number System"),
	("EE", "Expressions & Equations"),
	("SP", "Statistics & Probability"),
	("F", "Functions"),
]

cat_index = {}
categories = {}
i = 0
for c in list_categories:
	categories[c[0]] = c[1]
	cat_index[c[1]] = i
	i+=1

for c in categories.values():
	by_category[c] = []

as_table["categories"] = [c[1] for c in list_categories]
as_table["table"] = []
for i in range(9):
 	as_table["table"].append([])
 	for j in range(len(list_categories)):
 		as_table["table"][-1].append([])

grade_index = 0
grade_name = ""
topic_name = ""
f = open("ccmath.txt", "r")
for line in f.readlines():
	if line.startswith("CCSS"):
		name, desc = line.split(" ", 1)
		lesson = {
			"name": name,
			"description": desc.strip(),
		}
		standard[grade_name][topic_name].append(lesson)
		category = categories[name.split(".")[4]]

		by_category[category].append(lesson)
		lesson['mathbreakers'] = "irrelevant"
		as_table["table"][grade_index][cat_index[category]].append(lesson)

	elif line.startswith("Grade"):
		grade_index = int(line[6])
		grade_name = line.strip()
		standard[grade_name] = {}
	elif len(line) > 1:
		topic_name = line.strip()
		standard[grade_name][topic_name] = []

f.close()

f = open("cc-grade.json", "w")
f.write(json.dumps(standard, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()

f = open("cc-categories.json", "w")
f.write(json.dumps(by_category, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()

f = open("cc-table.json", "w")
f.write(json.dumps(as_table, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()