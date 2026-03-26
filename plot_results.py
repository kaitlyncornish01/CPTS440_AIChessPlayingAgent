import matplotlib.pyplot as plt

# Data from your experiment output
depths = [1, 2, 3]
times = [0.1800, 1.5930, 93.0909]
nodes = [1912, 22282, 1045073]

# Graph 1: Runtime vs Depth
plt.figure()
plt.plot(depths, times, marker='o')
plt.xlabel("Search Depth")
plt.ylabel("Runtime (seconds)")
plt.title("Alpha-Beta Runtime vs Depth")
plt.xticks(depths)
plt.savefig("runtime_vs_depth.png")
plt.show()

# Graph 2: Nodes Expanded vs Depth
plt.figure()
plt.plot(depths, nodes, marker='o')
plt.xlabel("Search Depth")
plt.ylabel("Nodes Expanded")
plt.title("Alpha-Beta Nodes Expanded vs Depth")
plt.xticks(depths)
plt.savefig("nodes_vs_depth.png")
plt.show()