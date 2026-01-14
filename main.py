#!/usr/bin/env python3
"""
Simple Calculator
Supports: +, -, *, /, ^ (power)
Run and enter expressions like: 2 + 2 or 5 * 3
Type 'q' or 'quit' to exit.
"""


def calculator():
    print("Simple Calculator — operations: +, -, *, /, ^ (power). Type 'q' to quit.")
    while True:
        expr = input("Enter expression (e.g., 2 + 2) or 'q' to quit: ").strip()
        if expr.lower() in ('q', 'quit', 'exit'):
            print("Goodbye!")
            break

        parts = expr.split()
        if len(parts) != 3:
            print("Please enter expression in format: number operator number (e.g., 2 + 3).")
            continue

        a_str, op, b_str = parts
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            print("Invalid numbers. Use format: number operator number (e.g., 3 * 4).")
            continue

        if op == '+':
            res = a + b
        elif op == '-':
            res = a - b
        elif op == '*':
            res = a * b
        elif op == '/':
            if b == 0:
                print("Error: Division by zero.")
                continue
            res = a / b
        elif op in ('^', '**'):
            res = a ** b
        else:
            print("Unknown operator. Use +, -, *, /, ^.")
            continue

        # Display integer results without a decimal when possible
        if res == int(res):
            res = int(res)
        print("Result:", res)


if __name__ == "__main__":
    calculator()