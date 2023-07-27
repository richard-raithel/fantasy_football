import pandas as pd

df = pd.read_csv('/media/rraithel/extradrive1/pythonProjects/pythonProject1/fantasy_doc.csv', delimiter='$', header=None)
df = df.T.stack().reset_index(drop=True)
df2 = df.apply(lambda st: st[st.find("(")+1:st.find(")")])
frames = [df, df2]
result = pd.concat(frames, axis=1)
result[0] = result[0].apply(lambda x: "".join(x.split(" ", 2)[2:4]))
result[0] = result[0].apply(lambda x: "".join(x.split(",", 2)[:1]))
result.columns = ['Player', 'PosRank']
for i in range(80, 250):
    result.at[i, 'Player'] = "".join(str(result.at[i, 'Player']).split(" ", 2)[2:4])
result.drop(result.index[250:380], inplace=True)
result.reset_index(drop=True)
print(result.to_string())
result.to_csv('sorted', index=False)
