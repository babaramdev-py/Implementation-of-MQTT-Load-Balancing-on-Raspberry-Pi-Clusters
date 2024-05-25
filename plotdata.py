import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Number of Code Snippets": [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    "Three Child Nodes (s)": [0.3501551151, 0.5035293102, 0.6302037239, 0.8285336494, 0.9414403439, 1.778853655, 2.539807796, 4.139019489, 5.200880766, 5.79480505, 6.702409506, 7.865920305, 8.69685936, 10.44113159],
    "Two Child Nodes (s)": [0.3819887638, 0.5078246593, 0.848400116, 0.9410083294, 1.280457497, 2.427719116, 3.368513346, 5.283348083, 6.566186905, 7.638847351, 9.049158812, 10.78516746, 11.53465724, 13.89575458],
    "One Child Node(s)": [0.3313879967, 0.7005023956, 1.124480247, 1.492216825, 1.768997908, 3.716583729, 5.532233953, 8.997071743, 11.58589673, 12.50587344, 14.31433225, 17.3888607, 19.69860101, 23.05336523],
    "Simple Client Server (s)": [0.2046720982, 0.4184322357, 0.5987398148, 0.8823461533, 1.062407732, 2.262252331, 3.236248732, 5.632411718, 6.655472517, 7.627613068, 8.643219948, 10.39729571, 11.43959951, 15.08400583]
}

df = pd.DataFrame(data)

plt.figure(figsize=(30, 20))

plt.plot(df["Number of Code Snippets"], df["Three Child Nodes (s)"], label="Three Child Nodes")
plt.plot(df["Number of Code Snippets"], df["Two Child Nodes (s)"], label="Two Child Nodes")
plt.plot(df["Number of Code Snippets"], df["One Child Node(s)"], label="One Child Node")
plt.plot(df["Number of Code Snippets"], df["Simple Client Server (s)"], label="Simple Client Server")

plt.xlabel("Number of Code Snippets")
plt.ylabel("Time (s)")
plt.title("Execution Time vs Number of Code Snippets")
plt.legend()

plt.grid(True)
plt.show()
