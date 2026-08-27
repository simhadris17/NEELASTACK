async def chunks(text,size=40):
    for i in range(0,len(text),size): yield text[i:i+size]
