import streamlit as st

# Streamlit UI
st.title("Assembly to Machine Code Converter")
st.write("Enter your assembly code below:")

assembly_code = st.text_area("Assembly Code", height=200)

# Your existing code starts here
r =["r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11","r12","r13"]
arithmetic_logical = ["add","sub","mul","div","mod","and","or","lsl","lsr","asr"]
not_mov =["not","mov"]
ld_st =["ld","st"]
branch = ["b","call","bgt","beq"]
nop_ret = ["nop","ret","hlt"] 
labels_dict = {}

def opcodes(opcode):
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
    rg = {"r0": "0000", 
        "r1": "0001", "r2": "0010", "r3": "0011",
                "r4": "0100", "r5": "0101", "r6": "0110",
                "r7": "0111", "r8": "1000", "r9": "1001", "r10": "1010",
                "r11": "1011", "r12": "1100", "r13": "1101"}
    return rg.get(register,"Invalid_register")
    
def immediate_to_binary(imm,bits):
    imm = int(imm)
    imm_bin = bin(imm)[2:].zfill(bits)
    return imm_bin
    
def assembly_instruction(instruction):
    instruct_ = instruction.replace(","," ").split()
    if "[" in instruct_[-1] or "]" in instruct_[-1]:
        imm_part = instruct_[2].split("[") 
        imm_rs2 = imm_part[0]
        rs1_ = imm_part[1].replace("]"," ").strip()
        final_instruction = instruct_[0] +" "+ instruct_[1]+"," + imm_rs2 +"," + rs1_
        instruct_ = final_instruction.replace(","," ").split()    
    s = instruct_[0] 
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
        elif instruct_[0] in not_mov :
            opcode = opcodes(instruct_[0])
            rd     = registers(instruct_[1])
            if instruct_[2] in r:
                rs2 = registers(instruct_[2])
                return opcode + "0" + rd +"0000"+rs2+"00000000000000"
            else :
                immediate = immediate_to_binary(instruct_[2],16)
                return  opcode + "1" + rd +"0000"+"00"+immediate
        else :
            return "invalid_code"
    elif(len(instruct_))== 2:
        if instruct_[0] in branch :
            opcode  = opcodes(instruct_[0])    
            immediate = immediate_to_binary(instruct_[1],27)
            return opcode + immediate
        else :
            return "invalid_code"
    elif(len(instruct_))== 1:    
        if  instruct_[0] in nop_ret :
            opcode = opcodes(instruct_[0])
            return opcode + "000000000000000000000000000"
        else :
            return "invalid_code"

# Streamlit button to convert
if st.button("Convert to Machine Code"):
    instruction_lines = assembly_code.strip().split("\n")
    address = 0
    binary_output = []
    
    for line in instruction_lines:
        machine_code = assembly_instruction(line.strip())
        binary_output.append(machine_code)
        address += 4
        if machine_code == 'invalid_code':
            st.error(f"Invalid instruction: {line}")
            break

    # Display the converted machine code
    st.write("### Machine Code Output")
    st.code("\n".join(binary_output), language="plaintext")