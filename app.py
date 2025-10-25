import pandas as pd
from deep_translator import GoogleTranslator as Translator
from tqdm import tqdm
import argparse

def parse_args():
    p=argparse.ArgumentParser(description="translate given columns from source language to target language")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--src",required=True)
    p.add_argument("--tgt",required=True)
    return p.parse_args()

def batch_translate(trans,texts):
    final=[]
    for text in tqdm(texts,desc="Translating..", leave=False):
        try:
            tradus=trans.translate(text)
            final.append(tradus)
        except Exception as e:
            print(f"Error:{e}")
            final.append("")
    return final

if __name__=="__main__":
    args=parse_args()
    file=pd.read_csv(args.input)
    trans=Translator(source=args.src,target=args.tgt)

    translated_chunks=[]
    coloane=[int(x) for x in input("What column to translate? ").split()]
    col_names=[file.columns[i] for i in coloane]

    chunk_size=100
    for chunk in pd.read_csv(args.input,chunksize=chunk_size):
        for col in col_names:
            texts = chunk[col].fillna("").astype(str).tolist()
            tqdm.write(f"translating column '{col}'...")
            translated=batch_translate(trans,texts)
            chunk[col]=translated
        translated_chunks.append(chunk)
    final=pd.concat(translated_chunks)
    final.to_csv(args.output,index=False)
    print(final)