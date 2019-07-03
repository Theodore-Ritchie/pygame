w=[['1','*','*','*','*','1','1'],['2','*','1','*','*','1','*'],['1','*','1','*','*','*','1']]
def row(iterable,x,x_,type):
	if x[0]!=x_[0] or x==x_:
		return False
	max=x if x[1]>x_[1] else x_[1]
	min=x if x[1]<x_[1] else x_[1]
#(1,3)	(1,5)
	for i in iterable[x[0]][min:max+1]:
		if str(i)!=type:
			return False
	return True
def col(iterable,y,y_,type):
	if y[1]!=y_[1] or y==y_:
		return False
	max=y[1] if y[1]>y[0] else y[0]
	min=y[1] if y[1]<y[0] else y[0]
	for i  in range(max-min):
		pass
print(str(row(w,(1,2),(1,4),'*')))
