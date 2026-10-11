i = 1 
while i < 4:
    j = 1
    while j < 4:
        print(f"{i} x {j} = {i * j}")
        j += 1
    i += 1
print("Done!")

for i in range(1, 4):    
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")
print("Done!")