import streamlit as st

# Streamlit UI setup
st.title("Assembly to Machine Code Converter")
st.write("Enter your assembly code below:")

# Text area for user input
assembly_code = st.text_area("Assembly Code", height=200)

# Define register names
r = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13"]

# Instruction categories
arithmetic_logical = ["add", "sub", "mul", "div", "mod", "and", "or", "lsl", "lsr", "asr"]
not_mov = ["not", "mov"]
ld_st = ["ld", "st"]
branch = ["b", "call", "bgt", "beq"]
nop_ret = ["nop", "ret", "hlt"]

# Dictionary to store label addresses
labels_dict = {}

def opcodes(opcode):
    """Returns the binary opcode for a given assembly instruction."""
    op = {
        "add": "00000", "sub": "00001", "mul": "00010", "div": "00011", "mod": "00100",
        "cmp": "00101", "and": "00110", "or": "00111", "not": "01000", "mov": "01001",
        "lsl": "01010", "lsr": "01011", "asr": "01100", "nop": "01101", "ld": "01110",
        "st": "01111", "beq": "10000", "bgt": "10001", "b": "10010", "call": "10011",
        "ret": "10100", "hlt": "11111"
    }
    return op.get(opcode, "Invalid_opcode")

def registers(register):
    """Returns the binary encoding for a given register name."""
    rg = {
        "r0": "0000", "r1": "0001", "r2": "0010", "r3": "0011",
        "r4": "0100", "r5": "0101", "r6": "0110", "r7": "0111",
        "r8": "1000", "r9": "1001", "r10": "1010", "r11": "1011",
        "r12": "1100", "r13": "1101"
    }
    return rg.get(register, "Invalid_register")

def immediate_to_binary(imm, bits):
    """Converts an immediate value to a binary string with the specified bit width."""
    imm = int(imm)
    if imm >= 0:
        return bin(imm)[2:].zfill(bits)
    else:
        return bin((1 << bits) + imm)[2:]

def assembly_instruction(instruction, program_counter):
    """Converts an assembly instruction into binary machine code."""
    instruct_ = instruction.replace(",", " ").split()

    # Handle load/store instructions with memory access
    if "[" in instruct_[-1] or "]" in instruct_[-1]:
        imm_part = instruct_[2].split("[")
        imm_rs2 = imm_part[0]
        rs1_ = imm_part[1].replace("]", "").strip()
        final_instruction = f"{instruct_[0]} {instruct_[1]},{imm_rs2},{rs1_}"
        instruct_ = final_instruction.replace(",", " ").split()

    s = instruct_[0]

    # Handle arithmetic, logical, load/store, and branch instructions
    if len(instruct_) == 4:
        if s in arithmetic_logical:
            opcode = opcodes(s)
            rd = registers(instruct_[1])
            rs1 = registers(instruct_[2])
            if instruct_[3] in r:
                rs2 = registers(instruct_[3])
                return opcode + "0" + rd + rs1 + rs2 + "00000000000000"
            else:
                immediate = immediate_to_binary(instruct_[3], 16)
                return opcode + "1" + rd + rs1 + "00" + immediate

    elif len(instruct_) == 3:
        if instruct_[0] == "cmp":
            opcode = opcodes(instruct_[0])
            rs1 = registers(instruct_[1])
            if instruct_[2] in r:
                rs2 = registers(instruct_[2])
                return opcode + "0" + "0000" + rs1 + rs2 + "00" + "000000000000"
            else:
                immediate = immediate_to_binary(instruct_[2], 16)
                return opcode + "1" + "0000" + rs1 + "00" + immediate

    elif len(instruct_) == 2:
        if instruct_[0] in branch:
            opcode = opcodes(instruct_[0])
            if instruct_[1] not in labels_dict:
                immediate = immediate_to_binary(instruct_[1], 27)
            else:
                immediate = immediate_to_binary((labels_dict[instruct_[1]] - program_counter) // 4, 27)
            return opcode + immediate

    elif len(instruct_) == 1:
        if instruct_[0] in nop_ret:
            opcode = opcodes(instruct_[0])
            return opcode + "000000000000000000000000000"

    return "invalid_code"

def labels(instruction_, address):
    """Stores label addresses in the dictionary for branch instructions."""
    instruct_ = instruction_.replace(",", " ").split()
    if len(instruct_) > 1 and instruct_[1] == ":":
        labels_dict[instruct_[0]] = address

def formatted_instruction(instruction_, program_counter):
    """Formats and processes assembly instructions before conversion."""
    instruct_ = instruction_.replace(",", " ").split()
    if len(instruct_) > 1 and instruct_[1] == ":":
        return assembly_instruction(" ".join(instruct_[2:]), program_counter)
    return assembly_instruction(instruction_, program_counter)

# Button to convert assembly code to machine code
if st.button("Convert to Machine Code"):
    instruction_lines = assembly_code.strip().split("\n")
    address = 0
    program_counter = 0
    binary_output = []

    # First pass: Record label addresses
    for line in instruction_lines:
        labels(line.strip(), address)
        address += 4

    # Second pass: Convert instructions to machine code
    for line in instruction_lines:
        machine_code = formatted_instruction(line.strip(), program_counter)
        binary_output.append(machine_code)
        program_counter += 4
        if machine_code == "invalid_code":
            st.error(f"Invalid instruction: {line}")
            break

    # Display the converted machine code
    st.write("### Machine Code Output")
    st.code("\n".join(binary_output), language="plaintext")

