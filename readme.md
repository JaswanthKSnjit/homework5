# Command Pattern Calculator

-- This a Command Pattern Calculator
-- When you run the program with <code>python main.py</code>, it will prompt you to type "menu" to view options or "exit" to quit the program. After that, it will display the four arithmetic operations you can perform. The format is <code>{command} <num1> <num2> (e.g., add 5 5)</code>, and it will then output the result.
-- Basic Calculator program is in [main](https://github.com/JaswanthKSnjit/homework5/tree/main) branch and code with Plugin Architecture is at [Plugins](https://github.com/JaswanthKSnjit/homework5/tree/plugins) branch.

## Setup Instructions

1. Clone Repo: <code> git clone git@github.com:JaswanthKSnjit/basic_calculator.git </code>
2. Navigate to project directory <code> cd basic_calculator </code>
3. Create a Python Virtual Environments <code> python -m venv venv </code>
4. Activate Python Virtual Environments <code> source venv/bin/activate </code>
5. Install dependencies <code> pip install -r requirements.txt </code>
6. Install faker <code> pip install faker </code>
7. Install faker requirements <code> pip freeze > requirements.txt </code>
8. To run the program <code> python main.py </code>
9. Running basic tests <code> pytest tests</code>
10. Faker generated random tests <code> pytest tests --num_records=100 </code>
11. For full debug output <code> pytest tests --num_records=10 -v -s </code>

**NOTE:** If you face any difficulties please contact me at <code> jk795@njit.edu </code>
