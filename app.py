import pandas as pd
from dotenv import load_dotenv # type: ignore
from deep_translator import GoogleTranslator as Translator # type: ignore
from openai import OpenAI
from tqdm import tqdm # type: ignore
import argparse
import os

def parse_args():
    p=argparse.ArgumentParser(description="translate given columns from source language to target language")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--src",required=True)
    p.add_argument("--tgt",required=True)
    return p.parse_args()

def use_gt(df,col_names,args):
    trans=Translator(source=args.src,target=args.tgt)
    for col in col_names:
        texts=df[col].fillna("").astype(str).tolist()
        df[col]=gt_translate(trans,texts)
    df.to_csv(args.output,index=False)
    print(f"Done!")

def gt_translate(trans,texts):
    result=[]
    for text in tqdm(texts,desc="Translating..", leave=False,ncols=150):
        try:
            result.append(trans.translate(text))
        except Exception as e:
            print(f"Error:{e}")
            result.append("")
    return result

def openai_translate(client,texts,args,column_type="text"):
    result=[]
    if column_type == "title":
        system_prompt = (
            f"You are a professional translator specializing in e-commerce product titles. "
            f"Translate from {args.src} to {args.tgt}. "
            f"Maintain product terminology, brand names, and technical specifications. "
            f"Keep the translation concise and SEO-friendly. "
            f"Return ONLY the translated title, no explanations or extra text."
        )
    elif column_type == "description":
        system_prompt = (
            f"You are a professional translator specializing in e-commerce product descriptions. "
            f"Translate from {args.src} to {args.tgt}. "
            f"Maintain the persuasive tone, technical details, and formatting. "
            f"Keep brand names, model numbers, and technical specifications unchanged. "
            f"Return ONLY the translated description, no explanations or extra text."
        )
    else:
        system_prompt = (
            f"Translate from {args.src} to {args.tgt}. "
            f"Return only the translation, no explanations."
        )

    for text in tqdm(texts,desc="Translating {column_type}..", leave=False,ncols=150):
        try:
            response=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":text}
                    ],
                    temperature=0.3,
                    max_tokens=2000

            )
            translated = response.choices[0].message.content.strip()

            result.append(translated)
        except Exception as e:
            print(f"Error:{e}")
            result.append("")
    return result

def use_openai(df,col_names,args):
    load_dotenv()
    api_key=os.getenv("OPENAI_KEY")
    if not api_key:
        print("no api key in .env\n")
        return 
    
    client=OpenAI(api_key=api_key)
    column_types={}
    for col in col_names:
        col_type=input(f"Content type for column '{col}' [title/description/text]: ").strip()
        if col_type not in ['title', 'description', 'text']:
            col_type='text'
        column_types[col]=col_type

    for i, col in enumerate(col_names, 1):
        texts=df[col].fillna("").astype(str).tolist()
        df[col]=openai_translate(client,texts,args,column_types[col])
        df.to_csv(args.output,index=False)
    print(f"Done!")
    


if __name__=="__main__":
    args=parse_args()
    df=pd.read_csv(args.input)

    coloane=[int(x) for x in input("What column to translate? ").split()]
    col_names=[df.columns[i] for i in coloane]
    x=int(input("What to use? \n 1. GoogleTranslate\n 2. OpenAI\n"))
    if x==1:
        use_gt(df,col_names,args)
    else:
        use_openai(df,col_names,args)