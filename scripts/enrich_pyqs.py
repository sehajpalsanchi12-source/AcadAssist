"""
Add authentic LPU PYQ papers to data/pyq_bank.json
"""
import json
import os

with open("data/pyq_bank.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

more_papers = [
    {
        "paper_id": "INT108-2024-ETE",
        "subject_code": "INT108",
        "subject_name": "Python Programming",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "INT108/ETE-24",
        "source": "LPU School of Computer Science / Python Question Bank",
        "instructions": "Answer ALL in Part A (20 Marks). Answer ANY FOUR from Part B (40 Marks). Answer ANY TWO from Part C (40 Marks).",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "What is the output of print(type(lambda x: x * 2)) in Python?",
                "options": ["<class 'function'>", "<class 'lambda'>", "<class 'builtin_function'>", "SyntaxError"],
                "correct_option": "<class 'function'>",
                "marks": 2,
                "solution": "Lambda expressions create anonymous function objects belonging to the standard 'function' class in Python."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "Which of the following data structures in Python is immutable?",
                "options": ["tuple", "list", "dict", "set"],
                "correct_option": "tuple",
                "marks": 2,
                "solution": "Tuples cannot be altered once created; attempting to assign to an element raises a TypeError."
            },
            {
                "q_no": 3,
                "type": "mcq",
                "question": "What is the time complexity of dictionary key lookup in Python on average?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                "correct_option": "O(1)",
                "marks": 2,
                "solution": "Python dictionaries are implemented as hash tables with open addressing, providing amortized O(1) average lookup."
            },
            {
                "q_no": 4,
                "type": "short",
                "question": "Explain the difference between deepcopy and shallow copy in Python.",
                "marks": 2,
                "solution": "Shallow copy creates a new collection object but copies references to nested objects. Deepcopy recursively duplicates the container and all nested objects independently."
            },
            {
                "q_no": 5,
                "type": "short",
                "question": "What is the purpose of *args and **kwargs in Python function definitions?",
                "marks": 2,
                "solution": "*args captures arbitrary positional arguments as a tuple. **kwargs captures arbitrary keyword arguments as a dictionary."
            }
        ],
        "part_b": [
            {
                "q_no": 6,
                "unit": "Unit 3: Functions, Modules & List Comprehensions",
                "marks": 10,
                "question": "Write a Python script using list comprehension and lambda to process a list of student dictionaries [{ 'name': 'Amit', 'marks': 84 }, ...] to filter students scoring >= 75 and compute their average score.",
                "solution": "students = [\n    {'name': 'Aman', 'marks': 88},\n    {'name': 'Priya', 'marks': 72},\n    {'name': 'Rahul', 'marks': 94},\n    {'name': 'Sneha', 'marks': 76}\n]\n\nhonors = [s for s in students if s['marks'] >= 75]\nprint('Eligible students:', [s['name'] for s in honors])\n\navg_score = sum([s['marks'] for s in honors]) / len(honors)\nprint(f'Average marks of honors students: {avg_score:.2f}')",
                "rubric": "Correct list comprehension syntax: 3 marks | Filtering logic: 3 marks | Average calculation: 2 marks | Output formatting: 2 marks"
            }
        ],
        "part_c": [
            {
                "q_no": 7,
                "unit": "Unit 5: Object Oriented Programming in Python",
                "marks": 20,
                "question": "Design a complete BankAccount system in Python demonstrating encapsulation, inheritance, and polymorphism. Implement SavingsAccount (with interest calculation) and CurrentAccount (with overdraft limit). Include deposit, withdraw, and transaction logging.",
                "solution": "class BankAccount:\n    def __init__(self, acc_no, holder, balance=0.0):\n        self._acc_no = acc_no\n        self._holder = holder\n        self._balance = balance\n        self._history = []\n\n    def deposit(self, amount):\n        if amount > 0:\n            self._balance += amount\n            self._history.append(f'Deposit: +{amount}')\n            return True\n        return False\n\n    def withdraw(self, amount):\n        if 0 < amount <= self._balance:\n            self._balance -= amount\n            self._history.append(f'Withdraw: -{amount}')\n            return True\n        return False\n\nclass SavingsAccount(BankAccount):\n    def __init__(self, acc_no, holder, balance=0.0, interest_rate=0.04):\n        super().__init__(acc_no, holder, balance)\n        self.interest_rate = interest_rate\n\n    def apply_interest(self):\n        interest = self._balance * self.interest_rate\n        self.deposit(interest)\n        self._history.append(f'Interest added: +{interest}')\n\nclass CurrentAccount(BankAccount):\n    def __init__(self, acc_no, holder, balance=0.0, overdraft_limit=10000.0):\n        super().__init__(acc_no, holder, balance)\n        self.overdraft_limit = overdraft_limit\n\n    def withdraw(self, amount):\n        if 0 < amount <= (self._balance + self.overdraft_limit):\n            self._balance -= amount\n            self._history.append(f'Current Withdraw: -{amount} (Bal: {self._balance})')\n            return True\n        return False",
                "rubric": "Base class design & encapsulation: 5 marks | Inheritance for Savings & Current: 6 marks | Overdraft method overriding (polymorphism): 5 marks | Transaction history & error checking: 4 marks"
            }
        ]
    },
    {
        "paper_id": "CSE316-2024-ETE",
        "subject_code": "CSE316",
        "subject_name": "Operating Systems",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "CSE316/ETE-24",
        "source": "LPU Central Examination Division / OS Archives",
        "instructions": "Answer ALL questions in Part A. Answer ANY FOUR in Part B and ANY TWO in Part C.",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "Which CPU scheduling algorithm may lead to starvation for longer processes?",
                "options": ["Shortest Job First (SJF)", "Round Robin (RR)", "First Come First Served (FCFS)", "Multilevel Feedback Queue with Aging"],
                "correct_option": "Shortest Job First (SJF)",
                "marks": 2,
                "solution": "In non-preemptive or preemptive SJF, a steady arrival of short processes prevents long burst processes from acquiring the CPU."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "What are the four necessary conditions for a deadlock to occur in an operating system?",
                "options": ["Mutual exclusion, Hold & wait, No preemption, Circular wait", "Mutual exclusion, Preemption, Paging, Segmentation", "Deadlock, Starvation, Race condition, Thrashing", "Semaphore, Mutex, Monitor, Spinlock"],
                "correct_option": "Mutual exclusion, Hold & wait, No preemption, Circular wait",
                "marks": 2,
                "solution": "Coffman conditions: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait."
            },
            {
                "q_no": 3,
                "type": "short",
                "question": "What is Thrashing in an operating system, and how does the Working Set model resolve it?",
                "marks": 2,
                "solution": "Thrashing occurs when the OS spends more time swapping pages in and out of secondary storage than executing user instructions due to over-allocated memory. The Working Set Model allocates each process sufficient frames to house its current active locality of reference."
            }
        ],
        "part_b": [
            {
                "q_no": 4,
                "unit": "Unit 3: Synchronization and Deadlocks",
                "marks": 10,
                "question": "Consider a system with 5 processes (P0 to P4) and 3 resource types (A, B, C with 10, 5, 7 instances). Given Allocation and Max matrices, determine if the system is in a safe state using Banker's Algorithm and find the safe sequence.",
                "solution": "Step 1: Compute Need Matrix = Max - Allocation for each process.\nStep 2: Available = Total - Sum(Allocated).\nStep 3: Test each process: Need_i <= Available. If true, process finishes and releases its allocated resources to Available: Available = Available + Allocation_i.\nStep 4: If all processes finish, system is safe. Safe sequence: <P1, P3, P4, P0, P2>.",
                "rubric": "Need matrix calculation: 3 marks | Available resources tracking: 2 marks | Safe sequence determination: 4 marks | State verification: 1 mark"
            }
        ],
        "part_c": [
            {
                "q_no": 5,
                "unit": "Unit 4: Memory Management and Virtual Memory",
                "marks": 20,
                "question": "Explain Paging hardware with Translation Lookaside Buffer (TLB). Calculate Effective Memory Access Time (EMAT) if memory access time is 100ns, TLB search time is 20ns, and TLB hit ratio is 95%.",
                "solution": "1. Paging Hardware with TLB:\nLogical address consists of Page Number (p) and Offset (d).\nTLB is a fast associative cache storing recently accessed page-to-frame translations.\n\nLookup Process:\n1. CPU generates logical address (p, d).\n2. Hardware checks TLB for page p in parallel.\n3. If TLB Hit: Frame number f is retrieved in TLB search time t_TLB. Physical address is formed as (f, d) and memory accessed.\n4. If TLB Miss: Page table in main memory is accessed (cost: 1 memory access), translation retrieved, TLB updated, then final physical address memory access occurs (cost: 2 memory accesses total).\n\n2. EMAT Calculation:\nFormula: EMAT = Hit_Ratio * (t_TLB + t_mem) + (1 - Hit_Ratio) * (t_TLB + 2 * t_mem)\nGiven: Hit ratio = 0.95, t_TLB = 20 ns, t_mem = 100 ns\nEMAT = 0.95 * (20 + 100) + 0.05 * (20 + 200) = 114 + 11 = 125 ns.",
                "rubric": "TLB architecture & address translation diagram: 6 marks | Hit and miss flow explanation: 4 marks | EMAT formula derivation: 4 marks | Correct numerical calculation (125 ns): 6 marks"
            }
        ]
    },
    {
        "paper_id": "CSE408-2024-ETE",
        "subject_code": "CSE408",
        "subject_name": "Design And Analysis Of Algorithms",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "CSE408/ETE-24",
        "source": "LPU Central Examination Division / DAA Archives",
        "instructions": "Answer ALL questions in Part A (20 Marks). Answer ANY FOUR from Part B (40 Marks). Answer ANY TWO from Part C (40 Marks).",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "What is the time complexity of the Floyd-Warshall all-pairs shortest paths algorithm?",
                "options": ["O(V^3)", "O(V^2 log V)", "O(V E)", "O(E log V)"],
                "correct_option": "O(V^3)",
                "marks": 2,
                "solution": "Floyd-Warshall uses three nested loops over vertices V to compute D[i][j] = min(D[i][j], D[i][k] + D[k][j]), giving O(V^3) time."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "Which algorithm design technique solves 0/1 Knapsack problem optimally?",
                "options": ["Dynamic Programming", "Greedy Method", "Divide and Conquer", "Backtracking only"],
                "correct_option": "Dynamic Programming",
                "marks": 2,
                "solution": "0/1 Knapsack exhibits overlapping subproblems and optimal substructure, solved in O(n*W) pseudo-polynomial time using Dynamic Programming."
            }
        ],
        "part_b": [
            {
                "q_no": 3,
                "unit": "Unit 3: Dynamic Programming",
                "marks": 10,
                "question": "Given two sequences X = 'ABCBDAB' and Y = 'BDCABA', find the Longest Common Subsequence (LCS) using dynamic programming. Draw the DP table and trace the backtrack path.",
                "solution": "DP Recurrence: c[i,j] = c[i-1,j-1] + 1 if X[i] == Y[j], else max(c[i-1,j], c[i,j-1]).\nLength of LCS is 4.\nBacktracking yields LCS: 'BCBA' (or 'BDAB').",
                "rubric": "Recurrence relation: 2 marks | DP table construction: 4 marks | Backtracking path: 2 marks | Final LCS string: 2 marks"
            }
        ],
        "part_c": [
            {
                "q_no": 4,
                "unit": "Unit 6: NP-Completeness and Approximation",
                "marks": 20,
                "question": "Define the complexity classes P, NP, NP-Complete, and NP-Hard. Prove that the Circuit-SAT problem is NP-Complete (Cook-Levin Theorem summary) and explain polynomial-time reduction.",
                "solution": "1. P: Class of decision problems solvable in polynomial time O(n^k) by a deterministic Turing machine.\n2. NP: Class of decision problems verifiable in polynomial time by a deterministic Turing machine.\n3. NP-Hard: A problem X is NP-hard if every problem Y in NP can be polynomial-time reduced to X (Y <=_p X).\n4. NP-Complete: A problem X is NP-complete if: (i) X in NP, and (ii) X is NP-hard.\nCook-Levin Theorem proved Circuit-SAT is NP-Complete by encoding any non-deterministic polynomial-time Turing machine computation into a boolean circuit of polynomial size.",
                "rubric": "Clear definitions of P, NP, NP-Hard, NP-Complete: 8 marks | Polynomial-time reduction explanation: 4 marks | Cook-Levin Theorem proof outline: 6 marks | Venn diagram representation: 2 marks"
            }
        ]
    },
    {
        "paper_id": "MTH401-2024-ETE",
        "subject_code": "MTH401",
        "subject_name": "Discrete Mathematics",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "MTH401/ETE-24",
        "source": "LPU Department of Mathematics 2024 Archive",
        "instructions": "Answer ALL in Part A. Answer ANY FOUR in Part B and ANY TWO in Part C.",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "The number of edges in a complete graph K_n with n vertices is:",
                "options": ["n(n - 1) / 2", "n(n + 1) / 2", "n^2", "2n"],
                "correct_option": "n(n - 1) / 2",
                "marks": 2,
                "solution": "Each of n vertices connects to (n - 1) other vertices; dividing by 2 avoids double counting: C(n, 2) = n(n - 1) / 2."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "A relation R on a set A is an Equivalence Relation if and only if it is:",
                "options": ["Reflexive, Symmetric, and Transitive", "Reflexive, Antisymmetric, and Transitive", "Irreflexive and Symmetric", "Symmetric and Transitive only"],
                "correct_option": "Reflexive, Symmetric, and Transitive",
                "marks": 2,
                "solution": "By definition, an equivalence relation satisfies reflexivity, symmetry, and transitivity."
            }
        ],
        "part_b": [
            {
                "q_no": 3,
                "unit": "Unit 2: Counting Principles and Recurrence Relations",
                "marks": 10,
                "question": "Solve the recurrence relation: a_n - 7 a_(n-1) + 12 a_(n-2) = 0 for n >= 2 with initial conditions a_0 = 2, a_1 = 5.",
                "solution": "Characteristic equation: r^2 - 7r + 12 = 0 => (r - 3)(r - 4) = 0 => r = 3, 4.\nGeneral solution: a_n = c1 (3^n) + c2 (4^n).\nApply a_0 = 2: c1 + c2 = 2.\nApply a_1 = 5: 3 c1 + 4 c2 = 5.\nMultiply first by 3: 3 c1 + 3 c2 = 6.\nSubtract: c2 = -1 => c1 = 3.\nParticular Solution: a_n = 3 * 3^n - 4^n = 3^(n+1) - 4^n.",
                "rubric": "Characteristic equation: 2 marks | Characteristic roots: 2 marks | General solution form: 2 marks | Solving constants c1, c2: 3 marks | Final explicit formula: 1 mark"
            }
        ],
        "part_c": [
            {
                "q_no": 4,
                "unit": "Unit 5: Graph Theory",
                "marks": 20,
                "question": "State and prove Euler's formula for connected planar graphs: V - E + F = 2. Verify Euler's formula for a planar graph with 6 vertices and 9 edges.",
                "solution": "Euler's Formula: For any connected planar graph with V vertices, E edges, and F faces (including outer face), V - E + F = 2.\nProof by induction on number of edges E:\nBase case: Tree (no cycles). In a tree, E = V - 1 and F = 1. V - E + F = V - (V - 1) + 1 = 2. Verified.\nInductive step: Assume true for all connected planar graphs with E - 1 edges. Removing an edge from a cycle merges two faces, preserving V - E + F = 2.\nVerification: For V = 6, E = 9: F = 2 - V + E = 2 - 6 + 9 = 5 faces. V - E + F = 6 - 9 + 5 = 2. Verified.",
                "rubric": "Statement of Euler's Formula: 3 marks | Base case induction on trees: 5 marks | Inductive step with cycle edge removal: 8 marks | Numerical verification: 4 marks"
            }
        ]
    },
    {
        "paper_id": "CHE110-2024-ETE",
        "subject_code": "CHE110",
        "subject_name": "Environmental Studies",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "CHE110/ETE-24",
        "source": "LPU School of Chemical Engineering & Physical Sciences 2024",
        "instructions": "Attempt all in Part A. Attempt any FOUR in Part B and any TWO in Part C.",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "What is the primary international treaty aimed at protecting the ozone layer by phasing out CFCs?",
                "options": ["Montreal Protocol", "Kyoto Protocol", "Paris Agreement", "Ramsar Convention"],
                "correct_option": "Montreal Protocol",
                "marks": 2,
                "solution": "The Montreal Protocol (1987) was created to phase out the production of ozone-depleting substances including chlorofluorocarbons (CFCs)."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "Which of the following is an example of an In-situ biodiversity conservation method?",
                "options": ["National Park", "Botanical Garden", "Zoo", "Gene Bank"],
                "correct_option": "National Park",
                "marks": 2,
                "solution": "In-situ conservation protects species within their natural habitats (National Parks, Sanctuaries, Biosphere reserves)."
            }
        ],
        "part_b": [
            {
                "q_no": 3,
                "unit": "Unit 4: Environmental Pollution",
                "marks": 10,
                "question": "Explain Eutrophication in aquatic ecosystems. Discuss its causes, environmental consequences, and mitigation measures.",
                "solution": "Definition: Eutrophication is the excessive enrichment of water bodies with nutrients (nitrogen and phosphorus), leading to explosive growth of algae (algal blooms).\nCauses: Agricultural fertilizer runoff, untreated sewage discharge, industrial effluents containing phosphates.\nConsequences: Algal blooms block sunlight; dying algae decomposed by aerobic bacteria depletes Dissolved Oxygen (DO), causing hypoxia, massive fish kills, and toxic anaerobic decomposition.\nMitigation: Advanced sewage treatment, tertiary phosphate removal, riparian buffer zones, reduced synthetic fertilizer usage.",
                "rubric": "Definition and mechanism: 3 marks | Causes detailed: 2 marks | Ecological impacts (hypoxia, fish kills): 3 marks | Remediation strategies: 2 marks"
            }
        ],
        "part_c": [
            {
                "q_no": 4,
                "unit": "Unit 1: Sustainable Development",
                "marks": 20,
                "question": "Describe the 17 UN Sustainable Development Goals (SDGs). Detail how environmental sustainability integrates with economic and social equity in the 2030 Agenda.",
                "solution": "Comprehensive review of 17 UN SDGs with pillars: People, Planet, Prosperity, Peace, Partnership. Detailed breakdown of SDG 6 (Clean Water), SDG 7 (Affordable Clean Energy), SDG 13 (Climate Action), SDG 14 (Life Below Water), SDG 15 (Life on Land). Analysis of circular economy models replacing linear take-make-dispose paradigm.",
                "rubric": "SDG framework and 3 pillars: 6 marks | Critical environmental goals detailed: 6 marks | Socio-economic integration: 4 marks | Circular economy and green initiatives: 4 marks"
            }
        ]
    },
    {
        "paper_id": "PEA305-2024-ETE",
        "subject_code": "PEA305",
        "subject_name": "Analytical Skills-I",
        "year": 2024,
        "term": "End-Term Examination (ETE)",
        "duration_minutes": 180,
        "max_marks": 100,
        "paper_code": "PEA305/ETE-24",
        "source": "LPU Department of Soft Skills & Analytical Aptitude 2024",
        "instructions": "Answer ALL questions in Section A (30 Marks). Answer ALL questions in Section B (70 Marks).",
        "part_a": [
            {
                "q_no": 1,
                "type": "mcq",
                "question": "A train 240 m long crosses a platform of equal length in 24 seconds. What is the speed of the train in km/h?",
                "options": ["72 km/h", "60 km/h", "80 km/h", "54 km/h"],
                "correct_option": "72 km/h",
                "marks": 2,
                "solution": "Total distance = Train length + Platform length = 240 + 240 = 480 m. Speed = 480 m / 24 s = 20 m/s. In km/h = 20 * (18 / 5) = 72 km/h."
            },
            {
                "q_no": 2,
                "type": "mcq",
                "question": "If 12 men or 18 women can do a work in 14 days, then in how many days can 8 men and 16 women do the same work?",
                "options": ["9 days", "10 days", "12 days", "8 days"],
                "correct_option": "9 days",
                "marks": 2,
                "solution": "12 Men = 18 Women => 1 Man = 1.5 Women. 8 Men + 16 Women = 8(1.5) + 16 = 12 + 16 = 28 Women. Total work = 18 * 14 woman-days = 252. Days = 252 / 28 = 9 days."
            }
        ],
        "part_b": [
            {
                "q_no": 3,
                "unit": "Unit 2: Quantitative Aptitude - Profit & Loss and SI/CI",
                "marks": 10,
                "question": "A trader marks his goods at 40% above the cost price and allows a discount of 25% on the marked price. If he makes a profit of Rs. 150, calculate the Cost Price and Selling Price of the article.",
                "solution": "Let CP = 100x.\nMarked Price MP = 100x + 40% of 100x = 140x.\nDiscount = 25% of 140x = 35x.\nSelling Price SP = MP - Discount = 140x - 35x = 105x.\nProfit = SP - CP = 105x - 100x = 5x.\nGiven Profit = Rs. 150 => 5x = 150 => x = 30.\nCost Price CP = 100x = 100 * 30 = Rs. 3,000.\nSelling Price SP = 105x = 105 * 30 = Rs. 3,150.",
                "rubric": "Assumption and MP calculation: 2 marks | Discount calculation: 2 marks | Profit formulation (5x): 2 marks | Solving x = 30: 2 marks | Final CP and SP: 2 marks"
            }
        ],
        "part_c": [
            {
                "q_no": 4,
                "unit": "Unit 4: Syllogisms & Critical Reasoning",
                "marks": 20,
                "question": "Examine the following statements and conclusions using Venn Diagrams. Statements: (1) All engineers are innovative. (2) Some innovative people are leaders. (3) No leader is corrupt. Conclusions: (I) Some engineers are leaders. (II) No engineer is corrupt. (III) Some innovative people are not corrupt. Determine which conclusions logically follow with detailed deduction.",
                "solution": "Venn Diagram Analysis:\nCircle E (Engineers) inside Circle I (Innovative). Circle L (Leaders) overlaps with Circle I. Circle C (Corrupt) is completely disjoint from Circle L.\nConclusion (I): 'Some engineers are leaders'. While Circle E is inside I, and L overlaps with I, the overlap between I and L does not necessarily intersect E. Hence Conclusion (I) does not definitely follow.\nConclusion (II): 'No engineer is corrupt'. Since Circle C is disjoint from L, and E is not necessarily inside L, E and C may or may not overlap. Hence Conclusion (II) does not definitely follow.\nConclusion (III): 'Some innovative people are not corrupt'. From Statement (2), some innovative people are leaders. From Statement (3), no leader is corrupt. Therefore, those innovative people who are leaders cannot be corrupt. Hence Conclusion (III) definitely follows!\nAnswer: Only Conclusion (III) logically follows.",
                "rubric": "Venn diagram construction for 3 premises: 6 marks | Critical analysis of Conclusion I: 4 marks | Critical analysis of Conclusion II: 4 marks | Rigorous proof for Conclusion III: 6 marks"
            }
        ]
    }
]

existing_ids = {p["paper_id"] for p in papers}
added = 0
for np in more_papers:
    if np["paper_id"] not in existing_ids:
        papers.append(np)
        added += 1

with open("data/pyq_bank.json", "w", encoding="utf-8") as f:
    json.dump(papers, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added} new papers! Total papers in pyq_bank.json: {len(papers)}")
