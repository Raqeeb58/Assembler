# Assembler
This Streamlit app is a web-based Assembly to Machine Code Converter designed to convert custom assembly instructions into 32-bit machine code. It includes label support, opcode encoding, and immediate/register decoding.
 How It Works (High-Level Flow)
 
User Input:
   The user enters assembly code in a text area.
   
   Assembly can include labels (e.g., loop:), comments (//), and instructions.
   
Instruction Categories:

Categorizes instructions into:

  Arithmetic/Logical: add, sub, or, etc.
  
  Unary/Move: not, mov
  
  Load/Store: ld, st
  
  Branch: b, call, beq, bgt
  
  Others: nop, ret, hlt
  
Functions Breakdown

opcodes(opcode)
Returns 5-bit binary string for a given opcode.

registers(register)
Returns 4-bit binary for a register (e.g., r1 → 0001).

immediate_to_binary(imm, bits)
Handles conversion of immediate values (decimal, hex, binary) into a signed binary string of bits width.

assembly_instruction(...)

The core function:
  Parses and normalizes an instruction.
  
  Decides its type based on length & keywords.
  
  Constructs final 32-bit machine code using opcode + register/immediate encoding.
  
Supports:
  R-type, I-type, memory, branches, unary, and immediate variations.
  
labels(...)
  Finds and stores label addresses (e.g., loop:) in labels_dict during the first pass.
  
formatted_instruction(...)
  Strips label declarations and passes clean instruction to assembly_instruction.
  
Two-Pass Processing
First Pass:
  Scans each line to record label addresses (for branch/jump instructions).
Second Pass:
  Converts each non-comment instruction to machine code using formatted_instruction(...).
Tracks program counter for relative label addressing.

Streamlit UI:
Title and text area for input.
A button: "Convert to Machine Code"
Displays binary output line-by-line after conversion.
Errors out for any invalid instruction.

