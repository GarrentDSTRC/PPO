import torch
a=torch.tensor([1,2])
b=torch.tensor(1)
c=torch.cat((a,b.unsqueeze(0)),0)
print(c.dim())
print(c)