#! /usr/bin/python3
from argparse import ArgumentParser

from lexer import Lexer
from parser import Parser
from ir_generator import IrGenerator
from code_gen import CodeGenerator

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("expr", type=str)
    args = parser.parse_args()
    return args


def prologue(asm):
    result = ""
    result += ".intel_syntax noprefix\n"
    result += ".global main\n"
    result += "main:\n"
    result += asm
    return result

if __name__ == "__main__":
    args = parse_args()
    expr = args.expr
    lexer = Lexer(expr)
    token_stream = lexer.tokenize()
    parser = Parser(token_stream)
    parsed_expr = parser.parser()
    ir_gen = IrGenerator()
    ir_seq = ir_gen.gen_ir(parsed_expr)
    code_gen = CodeGenerator()
    asm = code_gen.gen_code(ir_seq)
    result = prologue(asm)
    print(result)