import streamlit as st

# Streamlit UI
st.title("Assembly to Machine Code Converter")
st.write("Enter your assembly code below:")

# Text area for user input
assembly_code = st.text_area("Assembly Code", height=200)

# Define register names
r =["r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11","r12","r13"]

# Instruction categories
arithmetic_logical = ["add","sub","mul","div","mod","and","or","lsl","lsr","asr"]
not_mov =["not","mov"]
ld_st =["ld","st"]
branch = ["b","call","bgt","beq"]
nop_ret = ["nop","ret","hlt"] 

# Dictionary to store label addresses
labels_dict = {}

def opcodes(opcode):
    """Returns the binary opcode for a given assembly instruction."""
    op = {"add": "00000",
              "sub": "00001",
              "mul": "00010",
              "div": "00011",
              "mod": "00100",
              "cmp": "00101",
              "and": "00110",
              "or": "00111",
              "not": "01000",
              "mov": "01001",
              "lsl": "01010",
              "lsr": "01011",
              "asr": "01100",
              "nop": "01101",
              "ld": "01110",
              "st": "01111",
              "beq": "10000",
              "bgt": "10001",
              "b": "10010",
              "call": "10011",
              "ret": "10100",
              "hlt":"11111" }
    return op.get(opcode,"Invalid_opcode")

def registers(register):
    """Returns the binary encoding for a given register name."""
    rg = {"r0": "0000", 
        "r1": "0001", "r2": "0010", "r3": "0011",
                "r4": "0100", "r5": "0101", "r6": "0110",
                "r7": "0111", "r8": "1000", "r9": "1001", "r10": "1010",
                "r11": "1011", "r12": "1100", "r13": "1101"}
    return rg.get(register,"Invalid_register")
    
def immediate_to_binary(imm,bits):
    """Converts an immediate value to a binary string with the specified bit width."""
   
    if imm.startswith("0x") or imm.startswith("0X"):
        imm = int(imm, 16)
    elif imm.startswith("0b") or imm.startswith("0B"):
        imm = int(imm, 2)
    else:
        imm = int(imm)
    
    if imm > 0 :
        imm_bin = bin(imm)[2:].zfill(bits)
    else :
        imm_bin = bin((1 << bits) + imm)[2:] 
    return imm_bin
    
def assembly_instruction(instruction,program_counter):
    """Converts an assembly instruction into binary machine code."""
    instruct_ = instruction.replace(","," ").lower().split()
    
    # Handle load/store instructions with memory access
    if "[" in instruct_[-1] or "]" in instruct_[-1]:
        imm_part = instruct_[2].split("[") 
        imm_rs2 = imm_part[0]
        rs1_ = imm_part[1].replace("]"," ").strip()
        final_instruction = instruct_[0] +" "+ instruct_[1]+"," + imm_rs2 +"," + rs1_
        instruct_ = final_instruction.replace(","," ").split()    
    s = instruct_[0] 
    
    # Handle arithmetic, logical, load/store, and branch instructions
    if len(instruct_) == 4:
        if instruct_[0] in arithmetic_logical:
            opcode = opcodes(instruct_[0])
            rd     = registers(instruct_[1])
            rs1    = registers(instruct_[2])
            if instruct_[3] in r:
                rs2 = registers(instruct_[3])
                return opcode + "0"+ rd+rs1+rs2+"00000000000000"
            else :
                immediate = immediate_to_binary(instruct_[3],16)
                return opcode +"1"+rd+rs1+"00"+immediate    
        elif s[:-1] in arithmetic_logical :
            opcode = opcodes(s[:-1])
            rd     = registers(instruct_[1])
            rs1    = registers(instruct_[2])
            immediate = immediate_to_binary(instruct_[3],16)
            if(s[-1]=="u"):
                return opcode + "1" +rd+ rs1+"01"+immediate
            elif (s[-1]=="h"):
                return opcode + "1"+rd+ rs1+"10"+immediate    
        elif instruct_[0] in ld_st :
            opcode = opcodes(instruct_[0])
            rd     = registers(instruct_[1])
            rs1    = registers(rs1_)
            if imm_rs2 in r:
                rs2 = registers(imm_rs2)
                return opcode + "0"+ rd + rs1 + rs2 + "00000000000000"
            else:
                immediate = immediate_to_binary(imm_rs2,16)
                return opcode + "1"+ rd + rs1 + "00" + immediate 
        elif s[:-1] in ld_st :
            opcode = opcodes(s[:-1])
            rd     = registers(instruct_[1])
            rs1    = registers(rs1_)
            immediate = immediate_to_binary(imm_rs2,16)
            if(s[-1]=="u"):
                return opcode + "1"+ rd + rs1 + "01" + immediate
            elif (s[-1]=="h"):
                return opcode + "1"+ rd + rs1 + "10" + immediate
        else :
            return "invalid_code"
    elif(len(instruct_))== 3:
        if instruct_[0] == "cmp":
            opcode = opcodes(instruct_[0])
            rs1     = registers(instruct_[1])
            if instruct_[2] in r:
                rs2 = registers(instruct_[2])
                return opcode + "0" + "0000" +rs1+ rs2 + "00"+"000000000000"
            else :
                immediate = immediate_to_binary(instruct_[2],16)
                return opcode + "1" + "0000" +rs1+"00"+ immediate
        elif s[:-1]  == "cmp" :
            opcode = opcodes(s[:-1])
            rs1     = registers(instruct_[1])
            immediate = immediate_to_binary(instruct_[2],16)
            if(s[-1]=="u"):
                return opcode + "1" +"0000"+ rs1+"01"+immediate
            elif (s[-1]=="h"):
                return opcode + "1" +"0000"+ rs1+"10"+immediate
        elif instruct_[0] in not_mov :
            opcode = opcodes(instruct_[0])
            rd     = registers(instruct_[1])
            if instruct_[2] in r:
                rs2 = registers(instruct_[2])
                return opcode + "0" + rd +"0000"+rs2+"00000000000000"
            else :
                immediate = immediate_to_binary(instruct_[2],16)
                return  opcode + "1" + rd +"0000"+"00"+immediate
        elif s[:-1] in not_mov  :
            opcode = opcodes(s[:-1])
            rd     = registers(instruct_[1])
            immediate = immediate_to_binary(instruct_[2],16)
            if(s[-1]=="u"):
                return opcode + "1" +rd+"0000"+"01"+immediate
            elif (s[-1]=="h"):
                return opcode + "1" +rd+"0000"+"10"+immediate
        else :
            return "invalid_code"
    elif(len(instruct_))== 2:
        if instruct_[0] in branch :
            opcode  = opcodes(instruct_[0])    
            if instruct_[1] not in labels_dict:
                immediate = immediate_to_binary(instruct_[1],27)
            elif instruct_[1] in labels_dict : 
                immediate = immediate_to_binary((labels_dict[instruct_[1]]-program_counter)/4,27)
            return opcode + immediate
        else :
            print("invalid code")
    elif(len(instruct_))== 1:    
        if  instruct_[0] in nop_ret :
            opcode = opcodes(instruct_[0])
            return opcode + "000000000000000000000000000"
        else :
            return "invalid_code"
def labels(instruction_,address) :
    instruct_ = instruction_.replace(","," ").split()
    label_adress = address
     
    if len(instruct_) > 1 :
        if instruct_[1] == ":":
            labels_dict[instruct_[0]] = label_adress
        
def formatted_instruction(instruction_,program_counter) :
    instruct_ = instruction_.replace(","," ").split() 
    formatted_instruction = ""
    if len(instruct_) > 1 :
        if instruct_[1] == ":":
            formatted_instruction =  instruct_[2] + " " + ",".join(instruct_[3:])      
        else :
            formatted_instruction = instruction_
    else: 
        formatted_instruction = instruction_
    return assembly_instruction(formatted_instruction,program_counter)


# Button to convert assembly code to machine code
if st.button("Convert to Machine Code"):
    instruction_lines = assembly_code.strip().split("\n")
    address = 0
    program_counter =0
    binary_output = []
    
    # First pass: Record label addresses
    for line in instruction_lines: 
        labels(line.strip(),address)
        address += 4
    
    # Second pass: Convert instructions to machine code
    for line in instruction_lines:
        line = line.strip()
    
    # Ignore full-line comments
        if line.startswith("//") or line == "":
            continue
        clean_line = line.split("//")[0].strip()
        machine_code = formatted_instruction(clean_line,program_counter)
        binary_output.append(machine_code)
        program_counter += 4
        if machine_code == 'invalid_code':
            st.error(f"Invalid instruction: {line}")
            break

        
        

    # Display the converted machine code
    st.write("### Machine Code Output")
    st.code("\n".join(binary_output), language="plaintext")

