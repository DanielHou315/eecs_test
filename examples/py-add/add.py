import sys

def add(f1, f2, out_f):
    num1, num2 = 0,0
    # Read in the two numbers
    with open(f1, "r") as f:
        num1 = int(f.readline())
    with open(f2, "r") as f:
        num2 = int(f.readline())
    
    # Compute result
    result = abs(num1) + num2

    # Write to file
    with open(out_f, "w") as f:
        f.write(str(result))
    
if __name__ == "__main__":
    if len(sys.argv) == 4:
        add(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Please provide three arguments: [num1 file], [num2 file], [result file]")